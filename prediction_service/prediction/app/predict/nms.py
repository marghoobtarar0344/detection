# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\predict\nms.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------

import numpy as np
from common.exception_detections import get_error
def NMS(scores, boxes, threshold=0.3):
    try:
        scores = scores
        # print('actual socres',scores)
        # act_score = scores
        # Return an empty list, if no boxes given
        if len(boxes) == 0:
            return [], [], []
        x1 = boxes[:, 1]  # x coordinate of the top-left corner
        y1 = boxes[:, 0]  # y coordinate of the top-left corner
        x2 = boxes[:, 3]  # x coordinate of the bottom-right corner
        y2 = boxes[:, 2]  # y coordinate of the bottom-right corner
        # print('here is the x1',x1)
        # Compute the area of the bounding boxes and sort the bounding
        # Boxes by the bottom-right y-coordinate of the bounding box
        # We add 1, because the pixel at the start as well as at the end counts
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        # The indices of all boxes at start. We will redundant indices one by one.
        indices = np.arange(len(x1))
        break_index = 0
        area=0
        for i, box in enumerate(boxes):
            # Create temporary indices
            temp_indices = indices[indices != i]

            # Find out the coordinates of the intersection box
            xx1 = np.maximum(box[1], boxes[temp_indices, 1])
            yy1 = np.maximum(box[0], boxes[temp_indices, 0])
            xx2 = np.minimum(box[3], boxes[temp_indices, 3])
            yy2 = np.minimum(box[2], boxes[temp_indices, 2])

            # Find out the width and the height of the intersection box
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)
            
            #print("box size:",w,h)
            # compute the ratio of overlap
            overlap = (w * h) / areas[temp_indices]
            # if the actual boungding box has an overlap bigger than treshold with any other box, remove it's index
            if np.any(overlap) > threshold:
                indices = indices[indices != i]
            else:
                temp = scores[break_index]
                for lop in range(break_index, i):
                    if temp < scores[lop+1]:
                        temp = scores[lop+1]
                    

                scores[i] = temp
                break_index = i+1
        # return only the boxes at the remaining indices
        # print('we got indices', indices, scores)
        return boxes[indices].astype(int), indices, scores
    except Exception as e:
        error = get_error(e)
        
        raise RuntimeError(error)
