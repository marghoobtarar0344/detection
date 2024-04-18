
import os
from pathlib import Path


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    
    # for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
    #     if num < 1024.0:
    #         return num #"%3.1f %s" % (num, x)
    #     num /= 1024.0
    print('=====f sz',num)
    num /= 1024.0
    return num


def file_size(file_path):
    """
    this function will return the file size
    """
    if Path.exists(file_path):
        file_info = os.stat(str(file_path))
        return convert_bytes(file_info.st_size)
