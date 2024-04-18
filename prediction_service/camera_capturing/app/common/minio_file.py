# -------------------Point Duty Pty Ltd.--------------------
# Copyright (c) Point Duty Pty Ltd. All rights reserved. 
# file src\prediction_service\prediction\app\common\minio_file.py
# All code and supporting documentation is Copyright 2022 Point Duty Pty Ltd
# The information in this document is confidential and proprietary to Point Duty
# Pty Ltd, or its subsidiaries. This document is not to be reproduced or distributed
# outside Point Duty Pty Ltd or its subsidiaries unless by agreements with Point Duty Pty Ltd.
# Threat Hunter is the registered trademark of Point Duty Pty Ltd.
# -------------------Point Duty Pty Ltd.--------------------
from minio import Minio
from common.exception_detections import get_error
from minio.error import S3Error
from datetime import timedelta
from config.global_variables import (
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_URL,
    MINIO_BUCKET,
    MINIO_UNPROCESSED_FOLDER_NAME
)

import io
from PIL import Image
client = Minio(
    endpoint=MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)
found = client.bucket_exists(MINIO_BUCKET)
if not found:
    print('bucket not found')
    client.make_bucket(MINIO_BUCKET)
else:
    print(f"Bucket '{MINIO_BUCKET}' already exists")


def minio_put_obj(folder_name, image_name, img_data, is_byte=False):
    try:
        print('inside the bucket')

        if not is_byte:
            img_data = Image.fromarray(img_data, 'RGB')
        out_img = io.BytesIO()
        img_data.save(out_img, format='PNG')
        out_img.seek(0)

        size = len(out_img.getvalue())
        data = client.put_object(
            MINIO_BUCKET, f"{folder_name}/{image_name}", out_img, size, content_type='image'
        )
        url = client.presigned_get_object(
            MINIO_BUCKET, f"{folder_name}/{image_name}", expires=timedelta(days=7))

    except S3Error as e:

        error = get_error(e)

        raise RuntimeError(error)

    except Exception as e:
        error = get_error(e)

        raise RuntimeError(error)
    else:
        return True, url


def minio_get_obj_list(folder_name):
    try:

        objects = client.list_objects(
            f"{MINIO_BUCKET}",
            prefix=f"{folder_name}",
            recursive=True,
            include_user_meta=True
        )

    except S3Error as e:
        error = get_error(e)

        raise RuntimeError(error)
    except Exception as e:
        error = get_error(e)

        raise RuntimeError(error)
    else:
        return objects


def minio_get_obj(name_obj):
    try:
        print(name_obj)
        frame_name_path = name_obj
        response = client.get_object(MINIO_BUCKET, frame_name_path)

    except S3Error as e:
        error = get_error(e)

        raise RuntimeError(error)
    except Exception as e:
        error = get_error(e)

        raise RuntimeError(error)
    else:
        return response.data

