# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\common\error_log_request.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

from messages.logging import logger
from config.global_variables import EXCEPTION_HOST
import requests


def api_call_exception_log(data):
    try:
        PARAMS = {
            **data
        }
        print('the param ', PARAMS)

        get_test_url = "{}/exception_handle_doctor".format(EXCEPTION_HOST)
        requests.post(
            url=get_test_url,
            params=PARAMS,

        )

    except Exception as e:
        # raise Exception(e)
        print('daa', data)
        logger.error("the error is: {}".format(repr(e)))
        return False
    else:
        # data = response.data
        return data
