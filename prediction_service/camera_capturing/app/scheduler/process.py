# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved.Ê
# file src\prediction_service\camera_capturing\app\scheduler\process.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

import datetime
import time
import cv2
import pafy
from pathlib import Path
from dotenv import load_dotenv
from common.sql_to_dict import mssql_result2dict
from common.calc_file_size import  file_size
from common.exception_detections import get_error
from common.error_log_request import api_call_exception_log
from common.db_connection import db_conn
from common.email_send import email_notification
from common.minio_file import minio_put_obj
from common.resize_pad import resizeAndPadAndRotation
from config.global_variables import (
    FILE_SAVE_PATH,
    FRAMES_TABLE,
    CAMERA_TIME_ELAPSED,
    DB_NAME,
    MIN_IMAGE_SIZE,
    BATCH_NRT_STATUS_TABLE,
    ENVIRONMENT,
    LOW_FILE_SIZE_ALERT_TIME_ELAPSED,
    DATABASE_URL,
    TCP_CONNECTION_TIME_ELAPSED,
    AI_VIDEO_PATH,
    MINIO_UNPROCESSED_FOLDER_NAME,
    RESIZING_VALUE
)
load_dotenv()

def get_batch_status(db):
    try:
        query = "SELECT * FROM {} where NRT_BATCH_STATUS = ? and  child_process_name != ?".format(
            BATCH_NRT_STATUS_TABLE)
        db.execute(query, 'error', 'va_kafka')
        batch_status = mssql_result2dict(db)
        if len(batch_status):

            return False
        else:

            return True

    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)

def error_email_file_size(file_size_analyze, org_data,MIN_IMAGE_SIZE, id):
    try:
        data = {
                    "parent_process": "LUCY",
                    "child_process": "Image Size Error",
                    "status_is": "fail",
                    "error_type": 'Camera Image Quality Status',
                    'line_no': 'undetermined',
                    "file_name": 'process.py',
                    "description": f"The image is below the current threshold and will not be processed by the Prediction Service .\nImage Size : {str(int(file_size_analyze))} KB.\n Threshold :{MIN_IMAGE_SIZE} KB.\nCamera Id : {id}.\nCamera Name: {org_data[0]['camera_name']} \nCamera Link : {org_data[0]['camera_link']}",
                    "camera_id":id
                }
        api_call_exception_log(data)
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)
    
def good_email_file_size(id, org_data, MIN_IMAGE_SIZE, file_size_analyze,ENVIRONMENT):
    try:
        subject = f"CAM {id} ({ENVIRONMENT}) Bushfire Error Update: Processing Restored."
                        
        data = f"\n\
                                Camera ID: {id}\n\
                                Camera URL: {org_data[0]['camera_link']}\n\
                                Camera Name: {org_data[0]['camera_name']}\n\
                                Camera Link: The Camera link {org_data[0]['camera_link']}\n\
                                Threshold: {MIN_IMAGE_SIZE}\n\
                                Image Size : {str(int(file_size_analyze))} KB\n\
                                Description: The Image Quality is fine, Prediction Service can process now."
                       
        email_notification( data, subject)
                       
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)

def tcp_error_email(id,org_data):
    try:
        print('///*****cap is not opened sending email******///')
        data = {
            "parent_process": "LUCY",
            "child_process": "Camera Connectivity",
            "status_is": "fail",
            "error_type": 'Camera connectivity',
            'line_no': 'undetermined',
            "file_name": 'process.py',
            "description": f"Unable to open the Cap session to connect with the camera \nCamera Id : {id}\nCamera Link : {org_data[0]['camera_link']}",
            "camera_id" :id
        }
        api_call_exception_log(data)
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)

def camera_logs(db,id,status,description):
    try:
        '''start inserting camera logs here '''
        camera_log_query=f'''INSERT INTO [{DB_NAME}].dbo.[camera_logs] 
        (camera_id,status,description) VALUES (?,?,?)'''
        db.execute(camera_log_query,id,status,description)
        '''end inserting camera logs here '''
        query = "SELECT CAST (@@IDENTITY AS int) AS id"
        db.execute(query)
        id = mssql_result2dict(db)            
        id = id[0]['id']
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)
    else:
        return id

def camera_connection(link):
    try:
        if 'www.youtube' in link:

                video = pafy.new(link)
                best = video.getbest(preftype='mp4')
                cap = cv2.VideoCapture()
                cap.open(best.url)

        else:
            cap = cv2.VideoCapture(link)
        
    
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)
    else:
        return cap 
    
def tcp_error_retry_connection(cap,id,db,link,org_data):
    try:
        counter = 1
        query = f'UPDATE [{DB_NAME}].[dbo].[Cameras] SET error_status = 1, error_description = ? WHERE ID = ? and stop_it = 0;'
        db.execute(query, 'TCP Camera is not connected.', id)

        while True:
            tcp_error_email(id, org_data)
            print(f'************ wait for {TCP_CONNECTION_TIME_ELAPSED/60} minutes to retry connection === counter:{counter}===*******')
        
            import time
            time.sleep(TCP_CONNECTION_TIME_ELAPSED)
            cap =  camera_connection(link)
            if cap.isOpened():
                print(f'///******** cap opened from fault camera {id} after {counter} attempts *******/////')
                query = f'UPDATE [{DB_NAME}].[dbo].[Cameras] SET quality_status =0 ,error_status = 0, error_description = ? WHERE ID = ?  and stop_it = 0;'
                db.execute(query, 'TCP Camera got connected.', id)
                camera_logs(db,id,True,'Processing')
                return cap
            counter+=1
            
            '''stop trying reconnection if the user has stopped it intentionally'''
            query = f'select * from [{DB_NAME}].[dbo].[Cameras] where stop_it = 1 and ID = ? '
            db.execute(query, id)
            data = mssql_result2dict(db)
            if data:
                return cap


    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)

def save_frames(org_data,frame):
    try:
        frame_Time = str(datetime.datetime.now().strftime(
                        "%d-%m-%Y_%I-%M-%S_%p"))
        micro = str(datetime.datetime.now().microsecond)
        
        '''creating the folder and image path to save in directory'''
      
        
        file_save_path = Path(FILE_SAVE_PATH, str(org_data[0]['ID']))  
        
        if not Path.exists(file_save_path):
            file_save_path.mkdir(parents=True,exist_ok=True)
        
        
        image_name = str(
            org_data[0]['ID'])+"_image_"+ frame_Time + "_" + micro + ".jpg"
        file_path = Path(file_save_path, image_name)

        cv2.imwrite(str(file_path), frame)
    except Exception as e:
            # print(e)
        raise RuntimeError(e)
    else:
        return file_path, image_name, file_save_path

def low_quality_image_insertion(db,id,file_size_analyze,file_path,image_name,frame):
    try:
        camera_logs_id=camera_logs(db,id,False,f'Low Quality :{file_size_analyze},Min Quality Threshold {MIN_IMAGE_SIZE}')
        print('here is the camera log id',camera_logs_id,str(file_path))
        if file_path.exists():
            frame= resizeAndPadAndRotation(frame,RESIZING_VALUE)

            print('call minio to put low threshold image in non_processed folder')
            saved, presigned_url = minio_put_obj(
                MINIO_UNPROCESSED_FOLDER_NAME, image_name, frame)
            
            query = f'''INSERT INTO [{DB_NAME}].[dbo].[low_quality_images] 
                        (image_name,presigned_url,file_size,camera_logs_id) 
                        VALUES (?,?,?,?)'''
            db.execute(query,image_name,presigned_url,file_size_analyze,camera_logs_id)
            
            file_path.unlink()
        else:
            print('file does not exist')
    except Exception as e:
        error = get_error(e)
        print('here is an error during saving low quality frame',error)
        raise RuntimeError(e)
    else:
        return True
        
def stream_to_frame(id):
    try:
        query = f'SELECT TOP(1) * from [{DB_NAME}].[dbo].[Cameras] where ID = ?'
        db = db_conn(DATABASE_URL)
        db.execute(query, id)
        org_data = mssql_result2dict(db)
        
        query = f'''
                    SELECT * FROM
                        {AI_VIDEO_PATH}  WHERE main_file=? and folder_path=?
                                
                    '''
        db.execute(query, str(org_data[0]['ID']), str(Path(FILE_SAVE_PATH, str(org_data[0]['ID']))))
        id_exist_data = mssql_result2dict(db)
        
        if not len(id_exist_data):
            
            query = f'''
                        INSERT INTO {AI_VIDEO_PATH} 
                        (main_file,folder_path)
                        VALUES
                        (?,?)
                        '''
            db.execute(query, str(org_data[0]['ID']), str(Path(FILE_SAVE_PATH, str(org_data[0]['ID']))))
        
        
        
        
        '''
        we are declaring file_size_alert_current_time= false value because we wanted to send the notification 
        when the camera is up and it faces the error
        '''
        file_size_alert_current_time = False
        
        ''' it means that we haven't send the error/good quality image's email yet'''
        IMAGE_QUALITY_FLAG = 0
        if org_data:
            id = org_data[0]['ID']
            IMAGE_QUALITY_FLAG = 1 if org_data[0]['quality_status'] == 1 else 0
            # print('******** ID ******', id)
            link = org_data[0]['camera_link']
            

            cap =  camera_connection(link)
            
            #loop header may be a deadlock
            if not cap.isOpened():
                camera_logs(db,id,False,'Camera not available')
                cap =  tcp_error_retry_connection(cap,id,db,link,org_data)
                
            
            cur_time = time.time()  # Get current time
            # start_time_1min measures 10 sec
            # Subtract 3 seconds for start grabbing first frame after one second (instead of waiting a 10 sec for the first frame).
            start_time_1min = cur_time + CAMERA_TIME_ELAPSED
            
            '''updating the error status if '''
            query = f'UPDATE [{DB_NAME}].[dbo].[Cameras] SET error_status = 0, error_description = ? WHERE ID = ? and stop_it = 0'
            db.execute(query, 'TCP Camera got connected.', id)
            
            while cap.isOpened():
                
                '''********* stop the camera is user has stopped it without any processing ********'''
                query = f'SELECT TOP(1) * from [{DB_NAME}].[dbo].[Cameras] where ID = ? and stop_it = 1'
                db.execute(query, id)
                data = mssql_result2dict(db)
                if data:
                    break

                if not get_batch_status(db):
                    time.sleep(10)
                    continue
                
                '''' time elapsed block starts here CAMERA_TIME_ELAPSED '''
                

                cur_time = time.time()  # Get current time
                # Time elapsed from previous image saving.
                elapsed_time_1min = cur_time - start_time_1min
            
                # If 60 seconds were passed, reset timer, and store image.

                ret, frame = cap.read()
                if elapsed_time_1min >= 0:

                    if (ret != True):
                        break
                    # Reset the timer that is used for measuring 60 seconds
                    start_time_1min = cur_time + CAMERA_TIME_ELAPSED
                    
                    
                    '''time elapsed block ends here CAMERA_TIME_ELAPSED'''
                    ''' saving the images '''
                    
                    file_path, image_name, file_save_path =  save_frames(org_data, frame)
                    
                    file_size_analyze = file_size(file_path)
                    # file_size_analyze = 1
                    if file_size_analyze is None or file_size_analyze <= MIN_IMAGE_SIZE :
                        '''
                        it will save the detail of low_file_size in table low_quality_images 
                        and will delete the frame from the server
                        and will put the frame on the minio server unprocessed folder
                        '''
                        print('here is the file size==>',file_size_analyze)
                        
                        low_quality_image_insertion(db,id,file_size_analyze,file_path,image_name,frame)
                        
                        
                        
                        '''
                        THIS LOGIC HAS BEEN PLACED TO SEND THE NOTIFICATION IF THERE WAS AN ERROR AND AFTER SOME TIME
                        THE IMAGE SIZE COULDN'T FIXED AND WE WILL SEND THE ERROR AGAIN THATS WHY WE ARE REVERTING THE STATE.
                        '''
                        if file_size_alert_current_time:
                            time_alert = time.time() - file_size_alert_current_time
                            if time_alert >= LOW_FILE_SIZE_ALERT_TIME_ELAPSED and IMAGE_QUALITY_FLAG == 1:
                                IMAGE_QUALITY_FLAG = 0
                                
                        '''
                        we are going to send the error image after configured time interval                         
                        if  IMAGE_QUALITY_FLAG != 1: it will tell us either the email has been sent or not
                        
                        '''
                                                    
                        if  IMAGE_QUALITY_FLAG != 1:
                            query_status = f'UPDATE [{DB_NAME}].[dbo].[Cameras] SET quality_status = 1 WHERE ID = ?;'
                            db.execute(query_status, id)
                            if file_size_alert_current_time is False:
                                error_email_file_size(file_size_analyze, org_data,MIN_IMAGE_SIZE, id)
                                print('******* file size is not good email send time elapsed ********',file_size_alert_current_time)
                        
                                file_size_alert_current_time = time.time()
                                IMAGE_QUALITY_FLAG = 1
                            
                            else:
                                time_alert = time.time() - file_size_alert_current_time
                                print('******* file size is not good email send time elapsed ********',time_alert)                            
                                if time_alert >= LOW_FILE_SIZE_ALERT_TIME_ELAPSED:
                                    error_email_file_size(file_size_analyze, org_data,MIN_IMAGE_SIZE, id)
                                    file_size_alert_current_time = time.time()
                                    IMAGE_QUALITY_FLAG = 1
                        
                        
                        continue
                    '''
                    here we will tell the client now we are getting perfect images
                    if IMAGE_QUALITY_FLAG == 1: it will tell us either the email sent or not
                    '''
                    if IMAGE_QUALITY_FLAG == 1:
                        print(f"image quality is as expected== {file_size_analyze}, email sent ={IMAGE_QUALITY_FLAG} , Camera Id = {id}")
                        query_status = f'UPDATE [{DB_NAME}].[dbo].[Cameras] SET quality_status = 0 WHERE ID = ?;'
                        db.execute(query_status, id)
                        
                        
                        camera_logs(db,id,True,f'Processing')
                        
                        
                        if file_size_alert_current_time is False:
                            file_size_alert_current_time = time.time()
                            print('******* file size is good no email send ********',file_size_alert_current_time)
                            
                        else:
                            time_alert = time.time() - file_size_alert_current_time
                            print('******* file size is good email send time elapsed ********',time_alert)
                        
                            if time_alert >= LOW_FILE_SIZE_ALERT_TIME_ELAPSED:
                                file_size_alert_current_time = time.time()
                                # print(f"4 GOOD***** time alert =={time_alert} ********")
                            
                                
                                good_email_file_size(id,org_data, MIN_IMAGE_SIZE, file_size_analyze, ENVIRONMENT)
                        IMAGE_QUALITY_FLAG = 0
                    
                    daTe = datetime.datetime.now(datetime.timezone.utc)
                    Create_DateTime = daTe.strftime(
                        "%Y-%m-%dT%H:%M:%S")  # formateÊ
                    # if file_size_analyze > MIN_IMAGE_SIZE:
                    # try:
                    query = f'INSERT INTO {FRAMES_TABLE} \
                        (Camera_ID,image_name, image_path,processed_flag,current_datetime) \
                        VALUES (?,?,?,?,?);'
                    db.execute(query, org_data[0]['ID'], str(
                        image_name), str(file_save_path), 0, Create_DateTime)
                    
                       
                    # except Exception as e:
                    #     print(e)

            cap.release()
            print("Done! for the link,", id, " conditions to check if the camera to re-evaluate",
                  MIN_IMAGE_SIZE, link)

            if 'rtsp' in link:

                query = f'UPDATE [{DB_NAME}].[dbo].[Cameras] SET current_status = 0,quality_status =0 WHERE ID = ? and stop_it = 0;'
                db.execute(query, id)

            db.commit()
            db.close()

    except Exception as e:
        error = get_error(e)
        
        try:
            data = {
                "parent_process": "LUCY",
                "child_process": "camera",
                "status_is": "fail",
                "error_type": error['error_type'],
                'line_no': error['line_no'],
                "file_name": error['file_name'],
                "description": f"\n\
                    {str(error['description'])}\n\
                    Camera Id:{id}\n\
                    Camera Name: {org_data[0]['camera_name']}\n\
                    Camera Link : {org_data[0]['camera_link']}",
                "camera_id":id
            }
        except Exception as e:
            print(e)
            error = get_error(e)
            data = {
                "parent_process": "LUCY",
                "child_process": "camera",
                "status_is": "fail",
                "error_type": error['error_type'],
                'line_no': error['line_no'],
                "file_name": error['file_name'],
                "description": f"\n\
                    {str(error['description'])}\
                    \nCamera Id:{id}",
                "camera_id":id
            }
        
        print('error in stream_to_frame ==>', data)
        raise RuntimeError(data)

      #  api_call_exception_log(data)
    else:
        return 'objects'
