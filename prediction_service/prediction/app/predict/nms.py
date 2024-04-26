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
# from common.exception_detections import get_error
def calculate_iou(box, boxes):
    # Calculate intersection area
    x1 = np.maximum(box[0], boxes[:, 0])
    y1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[2], boxes[:, 2])
    y2 = np.minimum(box[3], boxes[:, 3])
    intersection_area = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
    # Calculate box and boxes areas
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    # Calculate IoU
    iou = intersection_area / (box_area + boxes_area - intersection_area)
    return iou

def nms(boxes, scores, threshold):
    # Sort boxes based on scores (descending order)
    sorted_indices = np.argsort(scores)[::-1]
    # print(sorted_indices)
    boxes = boxes[sorted_indices]
    scores = scores[sorted_indices]
    picked_indices = []
    while len(boxes) > 0:
        # Pick the box with the highest score
        picked_indices.append(sorted_indices[0])
        current_box = boxes[0]
        remaining_boxes = boxes[1:]
        # Calculate IoU (Intersection over Union) with remaining boxes
        ious = calculate_iou(current_box, remaining_boxes)
        # Filter out boxes with IoU greater than the threshold
        filtered_indices = np.where(ious <= threshold)[0]
        boxes = remaining_boxes[filtered_indices]
        sorted_indices = sorted_indices[filtered_indices + 1]
        scores = scores[filtered_indices]
    return picked_indices

def perform_multiclass_nms(scores,boxes,class_ids,threshold):
    
    filter_box = []
    filter_score = []
    filter_class = []
    # print(scores[np.array([False,  False, False,  True, False])])
    for class_id in np.unique(class_ids):
        class_boxes = boxes[class_ids == class_id]
        class_scores = scores[class_ids == class_id]
        classes = class_ids[class_ids == class_id]
        class_filtered_indices= nms( class_boxes, class_scores,threshold)
        print(class_boxes)
        print(class_scores)
        print(class_filtered_indices)
        filter_box.extend(class_boxes[class_filtered_indices])
        filter_score.extend(class_scores[class_filtered_indices])
        filter_class.extend(classes[class_filtered_indices])
    return filter_box,filter_score,filter_class
        
        