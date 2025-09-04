# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:29

@author: Aidan
@project: HandGestureRecog
@filename: device_probe
@description: camera backend selection
- Python 
"""
import sys

import cv2


def open_camera(index=0, width=512, height=512):
    if sys.platform == 'darwin':
        cap = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)
    else:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    if not cap.isOpened():
        raise IOError("Cannot open camera")
    return cap
