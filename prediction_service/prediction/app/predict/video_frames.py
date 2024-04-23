# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\predict\video_frames.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

from pathlib import Path
from common.exception_detections import get_error
from common.sql_to_dict import mssql_result2dict
from .resize_pad import resizeAndPadAndRotation
from .scoring import detect
from config.global_variables import (
    AI_FRAMES, FRAMES_CLAC_TABLE
)


def video_to_frames(
    db,
    camera_id,
    camera_name,
    camera_detail,
    frame,
    resizing,
    resizing_value,
    zoom_in,
    zoom_in_value,
    rotation,
    rotation_value,
    padding,
    occured_time,
    file_name,
    count,
    video_id,
    actual_file_path,
    process_calc_id
):
    try:
        """Function to extract frames from input video file
        and save them as separate frames in an output directory.
        Args:
            input_loc: Input video file.
            output_loc: Output directory to save the frames.
        Returns:
            None
        """
        
        resized_image = resizeAndPadAndRotation(
            frame, resizing, resizing_value, padding, rotation, rotation_value, zoom_in, zoom_in_value)
        
        frame_number = count
        
        
        detect(
            db,
            camera_id,
            camera_name,
            camera_detail,
            resized_image,
        
            video_id,
            file_name, 
            frame_number, 
            occured_time,
            actual_file_path,
            process_calc_id
        )

        # Path(actual_file_path).unlink()

    except Exception as e:
        

        error = get_error(e)
        raise RuntimeError(error)
