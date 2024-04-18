# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\scheduler_client.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

from config.global_variables import (
    BATCH_NRT_STATUS_TABLE,
    PARENT_PROCESS,
    PREDICTION_CHILD_PROCESS
)
from common.error_log_request import api_call_exception_log
from common.exception_detections import get_error
from common.sql_to_dict import mssql_result2dict
from common.db_connection import db_conn
# import downloading_model #dnt remove it
from scheduler.process_image import predition 

from config.global_variables import (
    DATABASE_URL
)


def get_batch_status(db):
    try:

        query = "SELECT * FROM {} WHERE parent_process_name = ? and child_process_name = ?".format(
            BATCH_NRT_STATUS_TABLE)
        db.execute(query, PARENT_PROCESS, PREDICTION_CHILD_PROCESS)
        batch_status = mssql_result2dict(db)
        # print("Lucy checked the status of prediction ",batch_status)
        if len(batch_status) > 0:
            batch_status = batch_status[0]['NRT_BATCH_STATUS']
            if batch_status == 'start':
                return True
            else:

                return False
        else:
            raise RuntimeError(f"""Please insert the entry for Camera capturing in the BATCH_STATUS TABLE  example (LUCY,
                                    camera,
                                    [AIHUMANPETROL],
                                    [dbo].[Cameras],
                                    {DATABASE_URL},
                                    current_status)""")
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)


db = db_conn()
while True:
    try:
        import time

        batch_status = get_batch_status(db)
        if batch_status:

            print('************** prediction is working ************')
            predition(db)
            time.sleep(0.1)
        else:
            print('************** prediction has been stopped *********')
            time.sleep(1)

    except Exception as e:
        error = get_error(e)
        data = {
            "parent_process": "LUCY",
            "child_process": "prediction",
            "status_is": "fail",
            "error_type": error['error_type'],
            'line_no': error['line_no'],
            "file_name": error['file_name'],
            "description": error['description']
        }
        print(error)
        api_call_exception_log(data)
        break
    finally:
        db.commit()
