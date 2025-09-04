"""
Author: Aidan Zhong
Date: 2025/8/18 21:16
Description:
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


def get_frame(cap, rgb=True):
    ok, frame = cap.read()
    if not ok:
        return None
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if rgb else frame


def frame_stream(cap, rgb=True):
    while True:
        frame = get_frame(cap, rgb)
        if not frame:
            break
        yield frame


def stream_preview(cap, rgb=True):
    while True:
        frame = get_frame(cap, rgb)
        cv2.imshow('Live cam', frame)
        # Exit on 'q' or ESC
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
