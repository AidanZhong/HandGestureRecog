# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:31

@author: Aidan
@project: HandGestureRecog
@filename: rules
@description: Axis-dominance, sequence detectors, dwell logic
- Python 
"""
from hand_gesture_control.core.types import GestureId


def is_zoom_in(prev, cur)->bool:
    return prev == GestureId.ZOOM and cur == GestureId.RELEASE

def is_zoom_out(prev, cur)->bool:
    return prev == GestureId.RELEASE and cur == GestureId.ZOOM

def tab_flick(dx, threshold = 0.03):
    if abs(dx) < threshold:
        return
    if dx < 0:
        # todo previous tab
        pass
    else:
        # todo next tab
        pass