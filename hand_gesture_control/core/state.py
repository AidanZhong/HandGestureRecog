# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:26

@author: Aidan
@project: HandGestureRecog
@filename: state
@description: all the state, such as x,y, gesture, mode
- Python 
"""
from typing import Optional

from hand_gesture_control.core.types import GestureId, Position2D


class PointerState:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.smoothed_x = 0.0
        self.smoothed_y = 0.0


class ClickState:
    def __init__(self, left_down: bool, right_down: bool):
        self.left_down = left_down
        self.right_down = right_down


class ModeState:
    def __init__(self, drag_mode: bool, draw_mode: bool, armed: bool):
        self.drag_mode = drag_mode
        self.draw_mode = draw_mode
        self.armed = armed


class History:
    def __init__(self, prev_gesture: Optional[GestureId], prev_pos: Optional[Position2D], prev_time: Optional[float]):
        self.prev_gesture = prev_gesture
        self.prev_pos = prev_pos
        self.prev_time = prev_time
