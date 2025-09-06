# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:31

@author: Aidan
@project: HandGestureRecog
@filename: rules
@description: Axis-dominance, sequence detectors, dwell logic
- Python 
"""
from hand_gesture_control.config.constants import TAB_SHIFT_LEFT, TAB_SHIFT_RIGHT
from hand_gesture_control.core.types import GestureId


class Rules:
    def is_zoom_in(self, prev, cur) -> bool:
        return prev == GestureId.ZOOM and cur == GestureId.RELEASE

    def is_zoom_out(self, prev, cur) -> bool:
        return prev == GestureId.RELEASE and cur == GestureId.ZOOM

    def tab_flick(self, dx, threshold=0.03):
        if abs(dx) < threshold:
            return
        if dx < 0:
            return TAB_SHIFT_LEFT
        else:
            return TAB_SHIFT_RIGHT
