# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:37

@author: Aidan
@project: HandGestureRecog
@filename: pointer
@description: Move/drag/scroll logic
- Python 
"""
from hand_gesture_control.actions.os_driver import OSDriver


class PointerController:
    def __init__(self, driver:OSDriver, width, height, ema, deadzone_eps, move_gain):
        self.driver = driver
        self.width = width
        self.height = height
        self.ema = ema
        self.deadzone_eps = deadzone_eps
        self.move_gain = move_gain
