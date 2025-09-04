# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:28

@author: Aidan
@project: HandGestureRecog
@filename: stream_adapter
@description: adapts my detector outputs to Gesture event
- Python 
"""
from time import monotonic

from hand_gesture_control.core.types import Position2D, GestureEvent, GestureId


def to_event(gesture:str, x, y, width, height):
    pos = Position2D(x/width, y/height)
    gid = GestureId(gesture)
    event = GestureEvent(gid, pos, monotonic())
    return event

