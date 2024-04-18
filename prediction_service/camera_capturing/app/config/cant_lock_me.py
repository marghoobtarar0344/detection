# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\camera_capturing\app\config\cant_lock_me.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd  
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

import asyncio
async def request_by_many(func, *args,msg=None):
    key = False
    
    lock = asyncio.Lock()
    
    async with lock:
        print(msg)
        if key is False:
            func_value=await func(*args)
            return func_value