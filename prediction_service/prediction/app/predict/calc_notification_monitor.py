# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\predict\calc_notification_monitor.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------
import datetime
import numpy as np
from common.sql_to_dict import mssql_result2dict
from common.exception_detections import get_error
from common.time_enable import time_eligibility
from config.global_variables import (
    DB_NAME,
    DB_NAME_BUSHFIRE,
    TIMEZONE,
    TIME_ELAPSED_NOTIFICATION,
    MIN_THRESHOLD_NOTIFICATION,
    MAX_THRESHOLD_NOTIFICATION,
    AREA_PERCENTAGE_THRESHOLD,
    MIN_AREA_PERCENTAGE_THRESHOLD

)


def get_iou(box1, box2):
    """ We assume that the box follows the format:
        box1 = [x1,y1,x2,y2], and box2 = [x3,y3,x4,y4],
        where (x1,y1) and (x3,y3) represent the top left coordinate,
        and (x2,y2) and (x4,y4) represent the bottom right coordinate """
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2
    x_inter1 = max(x1, x3)
    y_inter1 = max(y1, y3)
    x_inter2 = min(x2, x4)
    y_inter2 = min(y2, y4)
    width_inter = abs(x_inter2 - x_inter1)
    height_inter = abs(y_inter2 - y_inter1)
    print("width_inter,height_inter", width_inter, height_inter)
    area_inter = width_inter * height_inter
    width_box1 = abs(x2 - x1)
    height_box1 = abs(y2 - y1)
    width_box2 = abs(x4 - x3)
    height_box2 = abs(y4 - y3)
    area_box1 = width_box1 * height_box1
    area_box2 = width_box2 * height_box2
    print("area_box1,area_box2", area_box1, area_box2)
    area_union = area_box1 + area_box2 - area_inter
    iou = area_inter / area_union
    return iou


def valid_notification(xmin, ymin, xmax, ymax, detection_time, area, camera_id, db):
    try:
        if (
            abs(area) >= abs(AREA_PERCENTAGE_THRESHOLD) or
            abs(area) <= abs(MIN_AREA_PERCENTAGE_THRESHOLD)
        ):
            print("AREA condition did not meet:", "area_percentage", "area",
                  area, AREA_PERCENTAGE_THRESHOLD, MIN_AREA_PERCENTAGE_THRESHOLD)

            return 2, False

        # Get the current timestamp
        current_time = datetime.datetime.now()
        # Calculate the timestamp for five minutes ago
        time_elapsed_ago = current_time - datetime.timedelta(minutes=int(TIME_ELAPSED_NOTIFICATION))
 
        
        iou = 0
        time_in_mins = 0
        iou_list = False
        query_alarm = f"""
            select  top 1 FrameNumber,  DetectionTime  
            from  [{DB_NAME_BUSHFIRE}].[dbo].[BushfireDetection] 
            where CameraID = {camera_id} and DetectionTime>='{time_elapsed_ago}'
            order by DetectionTime desc;
        """
        
        db.execute(query_alarm)
        results_alarm = mssql_result2dict(db)
        print("results_alarm", results_alarm)
        time_eligible,rule = time_eligibility(TIMEZONE,camera_id)
        if not time_eligible:
            return rule, False
        if len(results_alarm):
            query_alarm_boxes = f"""SELECT 
                    [x_min]
                    ,[y_max]
                    ,[x_max]
                    ,[y_min]
                    FROM [{DB_NAME}].[dbo].[content_type] ct, 
                [{DB_NAME}].[dbo].frames fr where ct.frame_table_id=fr.ID and frame_table_id= ?;"""
            db.execute(query_alarm_boxes, results_alarm[0]['FrameNumber'])
            results_alarm_boxes = mssql_result2dict(db)
            print('result alarm boxes',
                  results_alarm[0]['FrameNumber'], results_alarm_boxes)
            # datetime.fromisoformat(str(results_alarm[0][1]))
            last_notification_time = datetime.datetime.strptime(str(results_alarm[0]['DetectionTime']), '%Y-%m-%d %H:%M:%S')
            
            time_diff = datetime.datetime.strptime(detection_time, '%Y-%m-%d %H:%M:%S') - last_notification_time
            time_in_mins = time_diff.total_seconds()/60
            if time_in_mins < TIME_ELAPSED_NOTIFICATION:
                    print('invalid_notification:time threshold does not matched time < time_elapsed_theshold')
                    return 7, False
            iou_list = []

            prediction_box = list([xmin, ymax, xmax, ymin])
            prediction_box = np.array(list(prediction_box), dtype=np.float32)
            for ground_tt_box in results_alarm_boxes:
                ground_tt_box = np.array(
                    list(ground_tt_box.values()), dtype=np.float32)
                iou = abs(get_iou(prediction_box, ground_tt_box))
                iou_list.append(iou)

                print('here are  the results', iou, MAX_THRESHOLD_NOTIFICATION,
                      time_in_mins, TIME_ELAPSED_NOTIFICATION)

                if (
                    iou >= MAX_THRESHOLD_NOTIFICATION and
                    time_in_mins >= TIME_ELAPSED_NOTIFICATION
                ):
                    print('valid_notification:threshold matched ', "iou", iou, "MAX_THRESHOLD_NOTIFICATION",
                          MAX_THRESHOLD_NOTIFICATION, "time_in_mins", time_in_mins, "iou_list", iou_list)

                    return 3, True
                elif (
                        iou >= MIN_THRESHOLD_NOTIFICATION and
                        abs(area) < abs(AREA_PERCENTAGE_THRESHOLD) and
                        abs(area) > abs(MIN_AREA_PERCENTAGE_THRESHOLD)
                ):

                    print('invalid_notification:threshold matched ', "iou", iou, "MIN_THRESHOLD_NOTIFICATION",
                          MIN_THRESHOLD_NOTIFICATION, "time_in_mins", time_in_mins, "iou_list", iou_list)
                    return 4, False
                else:
                    print('valid_notification:else part is working',
                          iou, time_in_mins, iou_list)

            print('valid_notification:notification has been generated ', iou_list)
            return 5, True

        else:
            print('no alarm in alarm table', iou, time_in_mins, iou_list)
            return 6, True

    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)
