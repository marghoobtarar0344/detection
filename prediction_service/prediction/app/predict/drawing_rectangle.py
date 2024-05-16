from PIL import Image, ImageDraw as D
import numpy as np
from PIL import ImageFont
from matplotlib import font_manager
from pathlib import Path
from common.exception_detections import get_error
from config.global_variables import (
    RESIZING_VALUE, 
    BOX_PADDING_VALUE,
    MIN_THRESHOLD_DETECTION,
    MAX_BOX,
    BOX_COLOR,
    SCORE_BACKGROUND_COLOR,
    MINIO_HAVE_CONTENT_FOLDER_NAME,
    MINIO_STATIC_FOLDER_PATH
    )

def draw_rectangle(image_np_with_detections, scores,detection_supression_box,actual_file_path,image_name):
    try:
        iteration = 0
        draw_boxes = 0
        font = font_manager.FontProperties(family='sans-serif', weight='bold')
        file = font_manager.findfont(font)
        font = ImageFont.truetype(file, 12)
        i = Image.fromarray(image_np_with_detections.astype('uint8'), 'RGB')
        draw=D.Draw(i)
        
        for dat in scores:
            score = float("{:.2f}".format(dat))
            
            print('======DRAW THE BOXES ==== SCORE={}, MIN_THRESHOLD={}, MAX_BOX={} AND DRAW_BOX_COUNTER = {}'.format(score,MIN_THRESHOLD_DETECTION,MAX_BOX, draw_boxes))
            
            if score*100 >= MIN_THRESHOLD_DETECTION:
                detection_box = detection_supression_box[iteration]
                y_min = int(detection_box[1])
                x_min = int(detection_box[0])
                x_max = int(detection_box[2])
                y_max = int(detection_box[3])
                if draw_boxes < MAX_BOX:
                    if y_min<40:
                        y_min = 45
                    x_min = x_min - BOX_PADDING_VALUE if x_min -BOX_PADDING_VALUE >= 0  else x_min
                    y_min = y_min - BOX_PADDING_VALUE if y_min - BOX_PADDING_VALUE >= 0 else y_min + 45
                    x_max = x_max + BOX_PADDING_VALUE if x_max +BOX_PADDING_VALUE <= RESIZING_VALUE[0] else x_max
                    y_max = y_max + BOX_PADDING_VALUE if y_max + BOX_PADDING_VALUE <= RESIZING_VALUE[1] else y_max
                    text = str(str(score))
                    fluctuating_color = int((260*score*100)/100)
                    draw.rectangle([(x_min,y_min),(x_max,y_max)],outline=BOX_COLOR, width=2)
                    draw.rectangle([(x_min,y_min-40),(x_min+35,y_min-10)] ,fill=SCORE_BACKGROUND_COLOR)
                    draw.text((x_min+7, y_min-31), text, font=font, fill=(fluctuating_color ,0,0))
                    
                    draw_boxes+=1
            iteration += 1
    
        # minio_path = str(Path(MINIO_STATIC_FOLDER_PATH, MINIO_HAVE_CONTENT_FOLDER_NAME, image_name))
        # i.save(minio_path)
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error) 
    else:
        return np.array(i)