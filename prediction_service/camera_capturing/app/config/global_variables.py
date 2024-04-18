# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\camera_capturing\app\config\global_variables.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd  
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


DOCTOR_PORT = os.getenv('DOCTOR_PORT')
EXCEPTION_HOST = os.getenv('EXCEPTION_HOST')+':'+str(DOCTOR_PORT)
DOCTOR_DB = os.getenv('DOCTOR_DB')
DB_NAME = os.getenv('DB_NAME')
DATABASE_URL = os.getenv('DATABASE_URL')
PARENT_PROCESS = os.getenv('PARENT_PROCESS')
CAMERA_CHILD_PROCESS = os.getenv('CAMERA_CHILD_PROCESS')
BATCH_NRT_STATUS_TABLE                  = f"[{DOCTOR_DB}].[dbo].[BatchStatus]"
AUDIT_LOG_TABLE                         = f"[{DOCTOR_DB}].[dbo].[AuditLog]"

FILE_SAVE_PATH ='/video_path' 
FRAMES_TABLE = f'[{DB_NAME}].[dbo].[LUCY_TO_PROCESS_CLAC]'
CAMERA_TIME_ELAPSED = int(os.getenv('CAMERA_TIME_ELAPSED'))
MIN_IMAGE_SIZE= int(os.getenv('MIN_IMAGE_SIZE'))
LOW_FILE_SIZE_ALERT_TIME_ELAPSED=int(os.getenv('LOW_FILE_SIZE_ALERT_TIME_ELAPSED')) 
TCP_CONNECTION_TIME_ELAPSED = int(os.getenv('TCP_CONNECTION_TIME_ELAPSED'))
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECIEVER_EMAIL = os.getenv('RECIEVER_EMAIL')
EMAIL_ACCOUNT_PASSWORD = os.getenv('EMAIL_ACCOUNT_PASSWORD')
ENVIRONMENT = os.getenv('ENVIRONMENT')
PATH_TO_FILE = str(Path('app', 'scheduler_client.py').resolve())
RESIZING_VALUE = (640, 640)



AI_VIDEO_PATH = f'[{DB_NAME}].[dbo].[video_path_table]'


'''minio details'''

MINIO_URL =os.getenv('MINIO_URL') 
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY') 
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET = 'fireai'
MINIO_IS_SECURE = False
MINIO_UNPROCESSED_FOLDER_NAME = 'unprocessed'

