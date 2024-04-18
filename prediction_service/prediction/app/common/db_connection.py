# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\common\db_connection.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

import pyodbc 
from config.global_variables import (
    DATABASE_URL
)
from common.exception_detections import get_error

def db_conn(dsn = DATABASE_URL):
    try:
        con = pyodbc.connect(dsn, autocommit=True)
        cursor = con.cursor()
        return cursor
    except Exception as e:
        error = get_error(e)

        raise RuntimeError(error)
