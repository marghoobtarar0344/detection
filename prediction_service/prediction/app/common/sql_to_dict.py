# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\common\sql_to_dict.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

import pyodbc
def mssql_result2dict(cursor):
    try: 
        result = []
        columns = [column[0] for column in cursor.description]
        for row in  cursor.fetchall():
            result.append(dict(zip(columns,row)))
        if len(result) > 0:
            ret = result
        else:
            ret =  []
    except pyodbc.Error as e:
        raise Exception(str(e))
    else:
        return ret