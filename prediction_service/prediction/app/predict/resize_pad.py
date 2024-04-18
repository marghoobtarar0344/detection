# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\predict\resize_pad.py
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


def resizeAndPadAndRotation(img, resizing, size, padding, rotation, rotation_value, zoom_in, zoom_value):
    try:
        padColor = 1
        h, w = img.shape[:2]
        print(h, w)
        sh, sw = size

        # interpolation method
        if h > sh or w > sw:  # shrinking image
            interp = cv2.INTER_AREA
        else:  # stretching image
            interp = cv2.INTER_CUBIC

        # aspect ratio of image
        # if on Python 2, you might need to cast as a float: float(w)/h
        aspect = w/h

        # compute scaling and pad sizing
        if aspect > 1:  # horizontal image
            new_w = sw
            # print('new_height(height/aspect)= {0}, original heigh ={1}, aspect ratio = {2}'.format(
            #     new_w/aspect, new_w, aspect))
            new_h = np.round(new_w/aspect).astype(int)
            pad_vert = (sh-new_h)/2
            pad_top, pad_bot = np.floor(pad_vert).astype(
                int), np.ceil(pad_vert).astype(int)
            pad_left, pad_right = 0, 0
        elif aspect < 1:  # vertical image
            new_h = sh

            new_w = np.round(new_h*aspect).astype(int)
            pad_horz = (sw-new_w)/2
            pad_left, pad_right = np.floor(pad_horz).astype(
                int), np.ceil(pad_horz).astype(int)
            pad_top, pad_bot = 0, 0
        else:  # square image
            new_h, new_w = sh, sw
            pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

        # set pad color
        # color image but only one color provided
        if len(img.shape) == 3 and not isinstance(padColor, (list, tuple, np.ndarray)):
            padColor = [padColor]*3

        # scale and pad
        if zoom_in:

            img = zoom(img, zoom_value)

        if resizing:
            img = cv2.resize(img, (sw, sh), interpolation=interp)
        if padding:
            img = cv2.copyMakeBorder(
                img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT)

        if rotation:
            rows, cols, channels = img.shape
            M = cv2.getRotationMatrix2D((cols/2, rows/2), rotation_value, 1)

            img = cv2.warpAffine(img, M, (cols, rows))

        return img

    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)
