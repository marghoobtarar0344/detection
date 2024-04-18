# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\scheduler\process_image.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

from common.sql_to_dict import mssql_result2dict
from common.exception_detections import get_error
import asyncio
from pathlib import Path
from predict.video_scoring_frame_scheduler import video_to_frame_analytics
from dotenv import load_dotenv
from config.global_variables import (
    RESIZING,
    RESIZING_VALUE,
    PADDING,
    ZOOM_IN,
    ZOOM_VALUE,
    ROTATION,
    ROTATION_VALUE,
    AI_VIDEO_PATH,
    FRAMES_CLAC_TABLE,
    CAMERAS_TABLE,
    LAST_MINUTES_IMAGE_GRAB_FOR_PREDICTION_TIME_ELAPSED
)
load_dotenv()

process_list = {}
lock = asyncio.Lock()
THREAD_RUNNING = False

async def read_clac_table(cursor):
    try:
        global process_list
        # if len(process_list) >= 0:
        
        from datetime import datetime, timedelta
        
        current_time = datetime.strptime(
            datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'
            )
        previous_time = current_time - timedelta(minutes=LAST_MINUTES_IMAGE_GRAB_FOR_PREDICTION_TIME_ELAPSED)
        
        query = f"""
                SELECT TOP(30) 
                lc.ID as lc_id,
                lc.Camera_ID, 
                lc.image_name,
                lc.image_path,
                c.camera_name, 
                vp.ID as vp_id,
                lc.current_datetime 
                FROM {FRAMES_CLAC_TABLE} as lc
                INNER JOIN
                {CAMERAS_TABLE} as c on lc.Camera_ID = c.ID
                INNER JOIN   
                {AI_VIDEO_PATH}  AS vp on vp.main_file=lc.Camera_ID            
                WHERE 
                lc.processed_flag = ? and 
                lc.current_datetime <= '{current_time}' and 
                lc.current_datetime>='{previous_time}'
                """
        cursor.execute(query, 0)
        data = mssql_result2dict(cursor)
        print(" read_clac_table, process_list is the latest image bucket ", len(data))
        update_list = []
        for dat in data:
            process_list[dat['lc_id']] = dat
            update_list.append(dat['lc_id'])

        if update_list:
            input_dynamic = '?,'*len(update_list)
            input_dynamic = input_dynamic[:-1]
            query = f"UPDATE {FRAMES_CLAC_TABLE} SET processed_flag = 100  WHERE ID IN ({input_dynamic}) "
            cursor.execute(query,  list(update_list))

    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)

def thread_run(db):
    try:
        pass
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(read_clac_table(db))
        loop.close()
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)

def predition(db):
    try:
       
        thread_run(db)
        data_extraction(db)

    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)

    else:
        return 'objects'


def data_extraction(db):
    try:
        global process_list
        range_iteration = list(process_list.keys())
        # print("pending list of images to process: ", len(range_iteration))
        for path in range_iteration:
            
            file_image_path = Path(
                process_list[path]['image_path'], process_list[path]['image_name'])
            if not Path.exists(file_image_path):
                query = f"DELETE {FRAMES_CLAC_TABLE} WHERE ID = {process_list[path]['lc_id']} "
                db.execute(query)
                del process_list[path]
                continue
            video_to_frame_analytics(
                process_list[path]['Camera_ID'],
                process_list[path]['camera_name'],
                'Camera detail not available',
                file_image_path,
                RESIZING,
                RESIZING_VALUE,
                ZOOM_IN,
                ZOOM_VALUE,
                ROTATION,
                ROTATION_VALUE,
                PADDING,
                process_list[path]['current_datetime'],
                process_list[path]['image_name'],
                0,
                process_list[path]['vp_id'],
                process_list[path]['lc_id'],
                db
            )

                
            del process_list[path]
            
    except Exception as e:
        process_list = {}
        error = get_error(e)
        raise RuntimeError(error)


