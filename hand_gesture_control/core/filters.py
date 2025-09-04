# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:25

@author: Aidan
@project: HandGestureRecog
@filename: filters
@description: EMA, dead-zone, velocity calculation
- Python 
"""


class EMA:
    def __init__(self, alpha: float):
        self.alpha = alpha
        self.smoothed_x = None
        self.smoothed_y = None
        self.initialized = False

    def step(self, x, y):
        '''low-pass filter for pointer smoothing'''
        if not self.initialized:
            self.smoothed_x = x
            self.smoothed_y = y
            self.initialized = True
        else:
            self.smoothed_x = self.alpha * x + (1 - self.alpha) * self.smoothed_x
            self.smoothed_y = self.alpha * y + (1 - self.alpha) * self.smoothed_y

        return self.smoothed_x, self.smoothed_y

    def reset(self):
        self.smoothed_x = None
        self.smoothed_y = None
        self.initialized = False


def apply_deadzone(dx, dy, deadzone_eps):
    '''ignore micro-jitter'''
    movement_2 = dx * dx + dy * dy
    deadzone_eps_2 = deadzone_eps * deadzone_eps

    if movement_2 < deadzone_eps_2:
        return 0.0, 0.0
    return dx, dy
