# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\config\global_variables.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------
import hydra
import os
from pathlib import Path
from dotenv import load_dotenv
from omegaconf import DictConfig
from common.exception_detections import get_error


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
DB_NAME = os.getenv('DB_NAME')
DB_NAME_BUSHFIRE = os.getenv('DB_NAME_BUSHFIRE')
DOCTOR_DB = os.getenv('DOCTOR_DB')
DOCTOR_PORT = os.getenv('DOCTOR_PORT')
PARENT_PROCESS =  os.getenv('PARENT_PROCESS')
PREDICTION_CHILD_PROCESS =  os.getenv('PREDICTION_CHILD_PROCESS')


'''*********************** EXCEPTION HOST *******************'''
EXCEPTION_HOST = os.getenv('EXCEPTION_HOST')+':'+str(DOCTOR_PORT)#'http://localhost:8000'
RESIZING = True
RESIZING_VALUE = (640, 640)
ZOOM_IN = False
ZOOM_VALUE = 0
ROTATION = False
ROTATION_VALUE = 0
PADDING = False
BOX_PADDING_VALUE = int(os.getenv('BOX_PADDING_VALUE'))
FILE_SAVE_PATH = '/video_path'

AI_FRAMES = f'[{DB_NAME}].[dbo].[frames]'
AI_VIDEO_PATH = f'[{DB_NAME}].[dbo].[video_path_table]'
FRAMES_CLAC_TABLE = f'[{DB_NAME}].[dbo].[LUCY_TO_PROCESS_CLAC]'
CAMERAS_TABLE = f'[{DB_NAME}].[dbo].[Cameras]'

BATCH_NRT_STATUS_TABLE                  = f"[{DOCTOR_DB}].[dbo].[BatchStatus]"
AUDIT_LOG_TABLE                         = f"[{DOCTOR_DB}].[dbo].[AuditLog]"


COORDINATE_GDA = "POINT(10 -20 4120)"
GRID_REFERENCE = 'grid reference'
FIRE_SHAPE =  "POLYGON ((24.950899 60.169158, 24.953492 60.169158, 24.95351 60.170104, 24.950958 60.16999, 24.950899 60.169158))"

PATH_TO_SAVED_MODEL =  str(Path('saved_model').resolve())
LABEL_MAP_PATH = str(Path('app', 'label_map.pbtxt').resolve())
MIN_THRESHOLD_DETECTION = float(os.getenv('MIN_THRESHOLD_DETECTION'))*100
ALARM_THRESHOLD = float(os.getenv('ALARM_THRESHOLD'))
SUPRESSION_THRESHOLD = float(os.getenv('SUPRESSION_THRESHOLD'))
MAX_BOX = int(os.getenv('MAX_BOX'))
CONTENT_TYPE_DATA_TABLE = f'[{DB_NAME}].[dbo].[content_type]'
ENABLE_BOUNDARY_BOXES=True

'''********************* TIME ELIGIBILITY **************************'''
TIMEZONE='Australia/Melbourne'
START_HR=18
END_HR=6

'''********* MINIO ******'''
MINIO_URL =os.getenv('MINIO_URL') 
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY') 
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_STATIC_FOLDER_PATH = '/minio/petrolpump'
BUCKET_NAME_MODEL = 'models'
BASE_PATH_SAVE_MODEL= str(Path('app', 'new_pb_model').resolve())
MINIO_BUCKET = 'petrolpump'
MINIO_IS_SECURE = False
MINIO_HAVE_CONTENT_FOLDER_NAME = 'havecontent'
MINIO_NO_CONTENT_FOLDER_NAME = 'nocontent'


FIRE_LOCATION = "POINT(10 -20 4120)"
SEARCH_RADIUS = 23
GRID_REFERECNCE = 'GRID REFERENCE'
BEARING = 10

MINIO_UNPROCESS_FOLDER_NAME = 'unprocessed'
MINIO_PROCESSED_FOLDER_NAME = 'processed'



TIME_ELAPSED_NOTIFICATION = int(os.getenv('TIME_ELAPSED_IN_MINUTES'))
MIN_THRESHOLD_NOTIFICATION = float(os.getenv('MIN_THRESHOLD_NO_TIME_ELAPSED'))
MAX_THRESHOLD_NOTIFICATION = float(os.getenv('MAX_THRESHOLD_WITH_TIME_ELAPSED'))
AREA_PERCENTAGE_THRESHOLD  = float(os.getenv('AREA_PERCENTAGE_THRESHOLD'))
MIN_AREA_PERCENTAGE_THRESHOLD = float(os.getenv('MIN_AREA_PERCENTAGE_THRESHOLD'))

LAST_MINUTES_IMAGE_GRAB_FOR_PREDICTION_TIME_ELAPSED = int(os.getenv('LAST_MINUTES_IMAGE_GRAB_FOR_PREDICTION_TIME_ELAPSED'))
SCORE_BACKGROUND_COLOR = '#92D050'
BOX_COLOR = '#92D050'
CLASSIFICATION_INVOKE_SERVICE='http://192.168.50.193:3500' #os.getenv('CLASSIFICATION_INVOKE_SERVICE')#
NOTIFICATION_RULES={}


# *************************** petrol pump ****************
CLASSES_TO_DETECT = [3,4,6,8]
CLASSES_DETECT_NAME = {3:"car",4: "motorcycle",6: "bus",8: "truck"} #CHECK BELOW REFERENCE
# https://gist.github.com/iitzco/3b2ee634a12f154be6e840308abfcab5
SCORE_THRESHOLD = 0.3
NMS_THRESHOLD=0.5






_HYDRA_PARAMS = {
    "version_base": "1.3",
    "config_path": "/",
    "config_name": "notification_rule",
}

@hydra.main(**_HYDRA_PARAMS)
def main(cfg: DictConfig) -> None:
    try:
        """
        params
        :cfg hydra omgconfig type
        
        return:
        dictionary
        
        """
        global NOTIFICATION_RULES
        NOTIFICATION_RULES = cfg['notification_rules']
        
    except Exception as e:
        error = get_error(e)
        print(error)
        raise RuntimeError(error)
    else:
        return cfg['notification_rules']
        
main()
print('GLOBAL FILE',NOTIFICATION_RULES)
    