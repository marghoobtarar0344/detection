# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\common\exception_detections.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

import os, sys
def exception_detection(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    error_data = {
        
        "error_type": str(exc_type),
        'line_no': str(exc_tb.tb_lineno),
        "file_name": str(fname),
        "description": str(exc_obj)
        }
    # logger.error("{}".format(error_data))
    return error_data
def get_error(e):
    error = e.args[0]
            
    if type(error) is  dict and 'file_name' not in error.keys():
        error = exception_detection(e)
        
    elif type(error) is not dict:
        error = exception_detection(e)
    return error