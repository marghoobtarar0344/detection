# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\camera_capturing\app\common\resize_pad.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

from common.exception_detections import get_error
import numpy as np
import cv2

from datetime import datetime
start = datetime.now()


def zoom(img, zoom_factor):
    try:
        return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)
    except Exception as e:
        error = get_error(e)

        raise RuntimeError(error)


def resizeAndPadAndRotation(img,  size):
    try:
        h, w = img.shape[:2]
        print(h, w)
        sh, sw = size

        # interpolation method
        if h > sh or w > sw:  # shrinking image
            interp = cv2.INTER_AREA
        else:  # stretching image
            interp = cv2.INTER_CUBIC

        img = cv2.resize(img, (sw, sh), interpolation=interp)
        
        return img

    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)
