# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\camera_capturing\app\run_multiple_scheduler_client.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

from common.sql_to_dict import mssql_result2dict
from common.exception_detections import get_error
from common.log_request import api_call_exception_log
from common.db_connection import db_conn
import os
import subprocess
import asyncio
from threading import Thread
from pathlib import Path
from config.global_variables import (
    DB_NAME,
    BATCH_NRT_STATUS_TABLE,
    PARENT_PROCESS,
    CAMERA_CHILD_PROCESS,
    DATABASE_URL,
    PATH_TO_FILE
)
loop = asyncio.get_event_loop()
os.environ['PYTHONINSPECT'] = 'True'



def get_batch_status(db):
    try:

        query = "SELECT * FROM {} where parent_process_name = ? and child_process_name=?".format(
            BATCH_NRT_STATUS_TABLE)
        db.execute(query, PARENT_PROCESS, CAMERA_CHILD_PROCESS)
        batch_status = mssql_result2dict(db)
        if len(batch_status):
            batch_status = batch_status[0]['NRT_BATCH_STATUS']
            if batch_status == 'start':
                return True
            else:
                return False
        else:
            raise RuntimeError(f"""Please insert the entry for Camera capturing in the BATCH_STATUS TABLE  example (LUCY,
                                    camera,
                                    [AIHUMAN],
                                    [dbo].[Cameras],
                                    {DATABASE_URL},
                                    current_status)""")
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)


def run_scheduler(id):
    try:
        
        subprocess.call(['python3', PATH_TO_FILE, str(id)])
        # subprocess.run(path, check=True)
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)


counter = 0
while True:
    try:
        with  db_conn() as db:
            if get_batch_status(db):
                print('******** Camera is working *******')
                query = f'SELECT ID from [{DB_NAME}].[dbo].[Cameras] where stop_it = 0 and current_status=0;'
                db.execute(query)
                data = mssql_result2dict(db)
                print("We will proceed with the given camera - ",
                    len(data) > 0, "picked up camera id -", len(data))
                for dat in data:
            
                    query = f'UPDATE [{DB_NAME}].[dbo].[Cameras] SET current_status = 1 WHERE ID = ?'
                    db.execute(query, dat['ID'])
                    Thread(target=run_scheduler, args=(
                        str(dat['ID']),)).start()
                    
                    counter += 1
                    print("****number of camera processed****", counter)
            db.commit()
        import time
        time.sleep(10)

    except Exception as e:

        error = get_error(e)

        data = {
            "parent_process": "LUCY",
            "child_process": "camera",
            "status_is": "fail",
            "error_type": error['error_type'],
            'line_no': error['line_no'],
            "file_name": error['file_name'],
            "description": error['description']
        }
        print(error)
        api_call_exception_log(data)
