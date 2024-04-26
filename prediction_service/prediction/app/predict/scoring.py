# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\predict\scoring.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------
import datetime
import random
import string
import warnings
import os
from pathlib import Path

import tensorflow as tf
import numpy as np
from nms import perform_multiclass_nms
from common.sql_to_dict import mssql_result2dict

from common.exception_detections import get_error
import matplotlib.pyplot as plt
from object_detection.utils import label_map_util
from .calc_notification_monitor import valid_notification
from .drawing_rectangle import draw_rectangle
from common.minio_file import minio_put_obj
from common.classification_invoke_service import invoking_classification_service
from config.global_variables import (
    PATH_TO_SAVED_MODEL,
    MIN_THRESHOLD_DETECTION,
    AI_FRAMES,
    CONTENT_TYPE_DATA_TABLE,
    LABEL_MAP_PATH,
    RESIZING_VALUE,
    MAX_BOX,
    MINIO_HAVE_CONTENT_FOLDER_NAME,
    MINIO_NO_CONTENT_FOLDER_NAME,
    FIRE_SHAPE,
    FIRE_LOCATION,
    SEARCH_RADIUS,
    SUPRESSION_THRESHOLD,
    ENABLE_BOUNDARY_BOXES,
    COORDINATE_GDA,
    BEARING,
    GRID_REFERENCE,
    ALARM_THRESHOLD,
    DB_NAME,
    DB_NAME_BUSHFIRE,
    NOTIFICATION_RULES,
    MINIO_STATIC_FOLDER_PATH,
    FRAMES_CLAC_TABLE,
    CLASSES_TO_DETECT,
    SCORE_THRESHOLD,
    NMS_THRESHOLD

)

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        print('now it is entring the gpus')
        for gpu in gpus:
            tf.config.experimental.per_process_gpu_memory_fraction = 0.8
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")

    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)
try:
    print(tf.__version__)
    # Loading the saved_model
    warnings.filterwarnings('ignore')
    print('Loading model...', end='')
    # Load saved model and build the detection function
    detect_fn = tf.saved_model.load('/saved_model')
    detect_fn = detect_fn.signatures['serving_default']

    gpu_devices = tf.config.list_physical_devices('GPU')
    print('************ here are GPU devices=>', gpu_devices)
    if gpu_devices:
        details = tf.config.experimental.get_device_details(gpu_devices[0])
        print('************here is the detail=>', details)
    print('Model loading successfully Done!')
    # Loading the label_map
    # category_index = label_map_util.create_category_index_from_labelmap(
    #     LABEL_MAP_PATH, use_display_name=True)
except Exception as e:
    error = get_error(e)
    raise RuntimeError(error)


def get_random_string(length):
    try:
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)


def detect(
        db,
        camera_id,
        camera_name,
        camera_detail,
        image_np,

        video_id,
        image_name,
        frame_number,
        occured_time,
        actual_file_path,
        process_calc_id
):
    try:

        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image_np)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        detections = detect_fn(input_tensor)
        print(detections)
        tensor = detections['detections:0']
        
        score_threshold = SCORE_THRESHOLD
        specific_classes = CLASSES_TO_DETECT
        numpy_array = tensor.numpy()
        numpy_array = numpy_array[0]
        numpy_array = np.array(numpy_array)
        indices = np.where(numpy_array[:, 5] > score_threshold)
        numpy_array = numpy_array[indices]
        mask = np.isin(numpy_array[:,6].astype(int), specific_classes)
        # Filter the array using the mask
        numpy_array = numpy_array[mask]
        boxes = numpy_array[:,1:5]
        class_ids = numpy_array[:,6].astype(int)
        scores = numpy_array[:,5]
        
        filtered_boxes,filtered_scores,filtered_classes = perform_multiclass_nms(scores,boxes,class_ids,NMS_THRESHOLD)
        


        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        # num_detections = int(detections.pop('num_detections'))
        # detections = {key: value[0, :num_detections].numpy()
        #               for key, value in detections.items()}
        # detections['num_detections'] = num_detections
        # # detection_classes should be ints.
        # detections['detection_classes'] = detections['detection_classes'].astype(
        #     np.int64)

        # iteration = 0
        # image_saved = False
        # detection_time = datetime.datetime.now(datetime.timezone.utc).strftime(
        #     "%Y-%m-%d %H:%M:%S")  # + datetime.timedelta(hours=int(10))  # exat australia time 
        # any_detection = False
        # detection_alarm = False

        # ''' ************* block start *****************'''
        # ''' removing those rows whose score is less than the given threshold need code optimization '''
        # detection_box = []
        # detection_score = []
        # detections_class = []
        # print(detections)
        # print(detections['detection_classes'])
        # print(detections['detection_boxes'])
        # print(detections['detection_scores'])

        # for i in range(0, len(detections['detection_boxes'])):
        #     # converting scores into percentage
        #     if float(detections['detection_scores'][i])*100 >= MIN_THRESHOLD_DETECTION:
        #         detection_box.append(detections['detection_boxes'][i])
        #         detection_score.append(detections['detection_scores'][i])
        #         detections_class.append(detections['detection_classes'][i])

        # detections['detection_scores'], detections['detection_boxes'], detections['detection_classes'] = np.array(
        #     detection_score), np.array(detection_box), np.array(detections_class)
        # ''' ************** block end ****************** '''

        # # print("BEFORE NMS:",detections['detection_scores'], detections['detection_boxes'], detections['detection_classes'])
        # detection_supression_box, indexes, scores = NMS(
        #     detections['detection_scores'], detections['detection_boxes']*RESIZING_VALUE[0], SUPRESSION_THRESHOLD)
        # presigned_url = ''

        # if ENABLE_BOUNDARY_BOXES:
        #     image_np = draw_rectangle(
        #         image_np,
        #         scores,
        #         indexes,
        #         detection_supression_box,
        #         actual_file_path,
        #         image_name
        #     )

        # iteration = 0
        # area = 0
        # for dat in indexes:
        #     score = "{:.2f}".format(scores[dat])
        #     # if float(score)*100 >= MIN_THRESHOLD_DETECTION: #converting score into percentage
        #     any_detection = True
        #     detection_box = detection_supression_box[iteration]
        #     ymin = detection_box[0]
        #     xmin = detection_box[1]
        #     xmax = detection_box[3]
        #     ymax = detection_box[2]
        #     area = (xmax-xmin)*(ymax-ymin)*100/(640*640)

        #     if not image_saved:
        #         saved, presigned_url = minio_put_obj(
        #             MINIO_HAVE_CONTENT_FOLDER_NAME, image_name, image_np)

        #         image_saved = True
        #         '''update the data to check if the content exist'''
        #         query = f'''
        #         INSERT INTO {AI_FRAMES}
        #         (video_path_table_id,image_name,frame_number,time_in_sec,content ,  detection_datetime ,presigned_url)
        #         VALUES
        #         (?,?,?,?,?,?,?)
        #         '''
        #         db.execute(query, video_id,
        #                    image_name, frame_number, occured_time, 1, detection_time, presigned_url)

        #         query = "SELECT CAST (@@IDENTITY AS int) AS id"
        #         db.execute(query)
        #         id = mssql_result2dict(db)

        #         id = id[0]['id']


        #     category = category_index[detections['detection_classes'][dat]]['name']
        #     query = f'INSERT INTO {CONTENT_TYPE_DATA_TABLE} (frame_table_id,score, category,x_min,y_min,x_max,y_max,area) VALUES(?,?,?,?,?,?,?,?)'
        #     db.execute(
        #         query,
        #         id,
        #         float(score),
        #         category,
        #         int(xmin),
        #         int(ymin),
        #         int(xmax),
        #         int(ymax),
        #         float(area)
        #     )
            
            # rule, alarm_beep = valid_notification(
            #     xmin, ymin, xmax, ymax, detection_time, area, camera_id, db)
            # print('beep result ,notification reason', alarm_beep,
            #       NOTIFICATION_RULES[rule]['generate_alarm'])
            # classification_rule = rule
            # generate_alarm = NOTIFICATION_RULES[rule]['generate_alarm']
            # notification_reasons =  NOTIFICATION_RULES[rule]['detail_reason']
            # if generate_alarm:
            #     # check the output from the classification model
            #     response = invoking_classification_service(
            #         actual_file_path, int(xmin), int(xmax), int(ymin), int(ymax))
            #     response = response['data']
            #     if len(response):
                    
            #         if response[0]:
            #             classification_rule = 9
            #         else:
            #             classification_rule = 8
                        
            #         generate_alarm  = NOTIFICATION_RULES[classification_rule]['generate_alarm']
            #         notification_reasons =  NOTIFICATION_RULES[classification_rule]['detail_reason']+','+ NOTIFICATION_RULES[rule]['detail_reason']
                
                    
            #     print('===>here is the response for classification invoking the service!',response)
            #     pass
               
            # query = f'''
            #         INSERT INTO [{DB_NAME}].[dbo].[notification_reasoning]
            #         (
            #             frame_number,
            #             generate_alarm,
            #             reason
            #         )
            #         VALUES(
            #             ?,?,?
            #         )
            #         '''

            # db.execute(
            #     query, id, generate_alarm, notification_reasons)

            # if float(scores[dat]) >= float(ALARM_THRESHOLD) and not detection_alarm:
            #     detection_alarm = True
            #     query = f'''INSERT INTO [{DB_NAME}].[dbo].[alert]
            #                         (
            #                             AlertUrl,
            #                             FireLocation ,  
            #                             DetectionTime ,     
            #                             CameraID, 
            #                             CameraName,
            #                             CameraDetails,
            #                             GDA94Coordinates,
            #                             ConfidenceScore,
            #                             DetectionImageUrl,
            #                             Bearing,
            #                             FireShape,
            #                             SearchAreaRadius,
            #                             GridReference,
            #                             FrameNumber
                                        
            #                         )
            #                         VALUES 
            #                             (
            #                                 ?,?,?,?,?,?,?,?,?,?,?,?,?,?
            #                             )
            #                         '''

            #     db.execute(
                #     query,
                #     get_random_string(
                #         10),
                #     FIRE_LOCATION,
                #     detection_time,
                #     camera_id,
                #     camera_name,
                #     camera_detail,
                #     COORDINATE_GDA,
                #     score,
                #     presigned_url,
                #     BEARING,
                #     FIRE_SHAPE,
                #     SEARCH_RADIUS,
                #     GRID_REFERENCE,
                #     id  # it is the frame number in frame table
                # )

            # ''' ********** insert ********** '''

            # if generate_alarm:
            #     # print('here is the alarm_beep', alarm_beep)
            #     query = f'''INSERT INTO [{DB_NAME_BUSHFIRE}].[dbo].[BushfireDetection]
            #                     (
            #                         AlertUrl,
            #                         FireLocation ,  
            #                         DetectionTime ,     
            #                         CameraID, 
            #                         CameraName,
            #                         CameraDetails,
            #                         GDA94Coordinates,
            #                         ConfidenceScore,
            #                         DetectionImageUrl,
            #                         Bearing,
            #                         FireShape,
            #                         SearchAreaRadius,
            #                         GridReference,
            #                         FrameNumber
            #                     )
            #                     VALUES 
            #                         (
            #                             ?,?,?,?,?,?,?,?,?,?,?,?,?,?
            #                         )
            #                     '''

            #     db.execute(
            #         query,
            #         get_random_string(
            #             10),
            #         FIRE_LOCATION,
            #         detection_time,
            #         camera_id,
            #         camera_name,
            #         camera_detail,
            #         COORDINATE_GDA,
            #         score,
            #         presigned_url,
            #         BEARING,
            #         FIRE_SHAPE,
            #         SEARCH_RADIUS,
            #         GRID_REFERENCE,
            #         id  # it is the frame number in frame table
            #     )

        #     iteration += 1

        # if not any_detection:
            # '''update the data to check if the content exist'''
            # with CodeTimer('scoring.py move file from drive to minio'):
            #     shutil.move(actual_file_path, str(
            #         Path(MINIO_STATIC_FOLDER_PATH, MINIO_NO_CONTENT_FOLDER_NAME, image_name)))

            # saved, presigned_url = minio_put_obj(
            #     MINIO_NO_CONTENT_FOLDER_NAME, image_name, image_np)
            # query = f'''
            # INSERT INTO {AI_FRAMES}
            #     (video_path_table_id,image_name,frame_number,time_in_sec,content,  detection_datetime ,presigned_url)
            #     VALUES
            #     (?,?,?,?,?,?,?)
            # '''
            # db.execute(query, video_id,
            #            image_name, frame_number, occured_time, 0, detection_time, presigned_url)

    except Exception as e:
        error = get_error(e)
        print('0', error)
        try:
            '''this is to delete the entry from frames table because of an error
            (remember we have no need to revert this entry from lucy to process calc table
            as the entry is already in cache to process again)
            '''
            sql = f'''DELETE FROM {AI_FRAMES} WHERE  presigned_url IS NULL'''
            db.execute(sql)
            # sql = f'''UPDATE {FRAMES_CLAC_TABLE} SET processed_flag=0 WHERE ID=?'''
            # db.execute(sql, process_calc_id)
        except Exception as e:
            error = get_error(e)
            print(error)

            raise RuntimeError(error)
        error = get_error(e)

        raise RuntimeError(error)
