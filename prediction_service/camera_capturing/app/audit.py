# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\camera_capturing\app\audit.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd  
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

from dotenv import load_dotenv
from common.sql_to_dict import mssql_result2dict
import pyodbc
from common.exception_detections import get_error
import os
from config.global_variables import (
    YOUTUBE_VIDEO_AUDIT,
    YOUTUBE_VIDEO_AUDIT_TABLE,
    DB_NAME
)

load_dotenv()


def db_conn():
    dsn = os.getenv('DATABASE_URL')
    con = pyodbc.connect(dsn, autocommit=True)
    cursor = con.cursor()
    return cursor


while True:
    try:
        if YOUTUBE_VIDEO_AUDIT:
            db = db_conn()
            query = f'''
                        select 
                        vpt.main_file as Camera_ID, 
                        vpt.ID as vpt_ID, 
                        count(f.ID) as total , 
                        count( case when f.content = 1 then 0 end) as have_content , 
                        count( case when f.content = 0 then 1 end) as no_content
                        from [{DB_NAME}].[dbo].[frames]  as f
                        left join [{DB_NAME}].[dbo].[video_path_table] as vpt 
                        on vpt.ID = f.video_path_table_id
                        where f.video_path_table_id IN (
                        select ID
                        from [{DB_NAME}].[dbo].[video_path_table] as vpt 
                        where main_file NOT IN (
                        select DISTINCT afc.Camera_ID
                        from [{DB_NAME}].[dbo].[AUDIT_FRAMES_CALCULATION] as afc
                        left join [{DB_NAME}].[dbo].[LUCY_TO_PROCESS_CLAC] as ltpc ON afc.Camera_ID = ltpc.Camera_ID
                        where ltpc.processed_flag = 0
                        GROUP by afc.Camera_ID
                        )
                        )
                        GROUP by vpt.main_file, vpt.ID

                '''
            db.execute(query)

            data = mssql_result2dict(db)
            print(data)
            for dat in data:
                query = f'''
                    UPDATE [{DB_NAME}].[dbo].[AUDIT_FRAMES_CALCULATION]
                    SET have_content=?,no_content=? where Camera_ID = ?
                    
                
                '''
                print(dat['have_content'],dat['no_content'], dat['Camera_ID'])
                db.execute(query, dat['have_content'],dat['no_content'], dat['Camera_ID'])
                print('it has been processed')
        import time
        time.sleep(3)
    except Exception as e:
        error = get_error(e)
        print(error)
    else:
        pass
