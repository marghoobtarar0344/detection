# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\camera_capturing\app\scheduler_client.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd  
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

import sys
import os
# import asyncio
from scheduler.process import stream_to_frame
# from concurrent.futures import ProcessPoolExecutor
from common.error_log_request import api_call_exception_log
# from threading import Thread

# loop = asyncio.get_event_loop()
from common.exception_detections import get_error
os.environ['PYTHONINSPECT'] = 'True'

import sys

print('cmd entry:', sys.argv)
arguments = sys.argv

try:
    print("Individual scheduler will be called for ",int(arguments[1]))
    stream_to_frame(int(arguments[1]))
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