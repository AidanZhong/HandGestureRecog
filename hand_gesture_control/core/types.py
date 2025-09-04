# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:24

@author: Aidan
@project: HandGestureRecog
@filename: types
@description: Data models (Gesture event, pose, enums)
- Python 
"""
import enum


class GestureId(enum.Enum):
    MOVE = 1
    DRAG_SCROLL = 2
    TAB_SHIFT = 3
    LCLICK = 5
    RCLICK = 4
    RELEASE = 6
    ZOOM = 7
    HANDWRITE = 8


class Position2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def delta(self, other):
        delta_x = self.x - other.x
        delta_y = self.y - other.y
        return delta_x, delta_y


class GestureEvent:
    def __init__(self, gesture: GestureId, pos: Position2D, t: float):
        '''

        :param gesture:
        :param pos:
        :param t: monotonic time
        '''
        self.gesture = gesture
        self.pos = pos
        self.t = t
