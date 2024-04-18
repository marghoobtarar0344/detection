# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\two_step_verification.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

import os
# from twilio.rest import Client
import random
from minio import Minio
import pyodbc
import zipfile
import shutil
import os
import shutil
from common.db_connection import db_conn
from common.exception_detections import get_error
from common.error_log_request import api_call_exception_log
from pathlib import Path

from config.global_variables import (
    BUCKET_NAME_MODEL,

    MINIO_URL,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    BASE_PATH_SAVE_MODEL,
    DATABASE_URL
)
client_minio = Minio(
    endpoint=MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def download_model():
    try:

        print('✔✔✔✔✔✔✔✔ Congratulation your model will be downloaded.✔✔✔✔✔✔✔✔')
        shutil.rmtree(BASE_PATH_SAVE_MODEL)
        os.mkdir(BASE_PATH_SAVE_MODEL)
        

        for item in client_minio.list_objects(BUCKET_NAME_MODEL):
            minio_file_path = Path(BASE_PATH_SAVE_MODEL, item.object_name)

            client_minio.fget_object(
                BUCKET_NAME_MODEL, item.object_name, str(minio_file_path))
            print('unzipping the model')
            

            with zipfile.ZipFile(str(minio_file_path), 'r') as zip_ref:
                zip_ref.extractall(BASE_PATH_SAVE_MODEL)
            minio_file_path.unlink()

    except Exception as e:
        error = get_error(e)

        data = {
            "parent_process": "LUCY",
            "child_process": "prediction",
            "status_is": "fail",
            "error_type": error['error_type'],
            'line_no': error['line_no'],
            "file_name": error['file_name'],
            "description": 'model downloading'+' '+error['description']
        }
        print(error)
        api_call_exception_log(data)


download_model()
