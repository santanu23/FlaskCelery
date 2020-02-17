# -*- coding: utf-8 -*-
"""Module contains the common image operations
"""

import os
import cv2
import string
from celery import Celery
from typing import List

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://rabbitmq:rabbitmq@rabbit:5672/')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task(name='tasks.add')
def add(x: int, y: int) -> int:
    return x + y

@celery.task(name='tasks.histogram_eualization')
def hist_equalize(image_path: str, *args, **kwargs) -> str:
    """
    Use's cv2's equalizeHist() on all images in the deepest leaves of the tree.
    Update the tree nodes accordingly with the new images.
    """
    grey_img = cv2.imread(image_path, 0)
    assert grey_img is not None

    eq = cv2.equalizeHist(grey_img)

    file_name, extension = os.path.splitext(image_path)
    res_path = f'{file_name}_heq{extension}'

    cv2.imwrite(res_path, eq)
    print(eq)
    return res_path

@celery.task(name='tasks.increase_brightness')
def increase_brightness(image_path: str, value: int, *args, **kwargs) -> str:
    """
    Increases the brightness of an image by a given value through changing the v
    in hsv values of the image.
    """
    img = cv2.imread(image_path)
    assert img is not None

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    brighter_img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    file_name, extension = os.path.splitext(image_path)
    res_path = f'{file_name}_brighter{extension}'

    cv2.imwrite(res_path, brighter_img)

    return res_path

@celery.task(name='tasks.decrease_brightness')
def decrease_brightness(image_path: str, value: int, *args, **kwargs) -> str:
    """
    Increases the brightness of an image by a given value through changing the v
    in hsv values of the image.
    """
    img = cv2.imread(image_path)
    assert img is not None

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = value
    v[v < lim] = 0
    v[v >= lim] -= value

    final_hsv = cv2.merge((h, s, v))
    darker_img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    
    file_name, extension = os.path.splitext(image_path)
    res_path = f'{file_name}_darker{extension}'

    cv2.imwrite(res_path, darker_img)

    return res_path

@celery.task(name='tasks.horizontal_stitch')
def horizontal_stitch(image_paths: List[str], *args, **kwargs) -> str:
    """
    This function stitches together two images horizontally
    """
    img1 = cv2.imread(image_paths[0])
    img2 = cv2.imread(image_paths[1])

    assert img1 is not None
    assert img2 is not None

    stitched_image = cv2.hconcat([img1, img2])
    
    file_name, extension = os.path.splitext(image_paths[0])
    res_path = f'{file_name}_stitched{extension}'

    cv2.imwrite(res_path, stitched_image)

    return res_path