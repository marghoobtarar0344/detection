
# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\predict\video_scoring_frame_scheduler.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

import numpy as np
from PIL import Image
from common.exception_detections import get_error
from .video_frames import video_to_frames
def video_to_frame_analytics(
    camera_id,
    camera_name,
    camera_detail,
    file_path,
    resizing,
    resizing_value,
    zoom_in,
    zoom_value,
    rotation,
    rotation_value,
    padding,
    occured_time,
    image_name,
    frame_number,
    video_id,
    process_calc_id,
    db
):
    try:
            
        file = Image.open(str(file_path))
        file = np.asarray(file)
        import time
        start = time.process_time()
        video_to_frames(
            db,
            camera_id,
            camera_name,
            camera_detail,
            file,
            resizing,
            resizing_value,
            zoom_in,
            zoom_value,
            rotation,
            rotation_value,
            padding,
            occured_time,
            image_name,
            frame_number,
            video_id,
            file_path,
            process_calc_id
        )
        print('total processing time for the video to frames table',time.process_time() - start)
            

    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)

    else:
        return True
