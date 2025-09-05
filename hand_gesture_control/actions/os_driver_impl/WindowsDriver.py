# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 22:42

@author: Aidan
@project: HandGestureRecog
@filename: WindowsDriver
@description: 
- Python 
"""
from typing import List

import pyautogui as pg

from hand_gesture_control.actions.os_driver import OSDriver


class WindowsDriver(OSDriver):
    def __init__(self):
        pass

    def move(self, px, py):
        pg.moveRel(px, py)

    def press_left(self):
        pg.mouseDown(button=pg.LEFT)

    def press_right(self):
        pg.mouseDown(button=pg.RIGHT)

    def release_left(self):
        pg.mouseUp(button=pg.LEFT)

    def release_right(self):
        pg.mouseUp(button=pg.RIGHT)

    def scroll(self, ticks):
        pg.scroll(ticks)

    def key_combo(self, keys: List[str]):
        pg.hotkey(*keys)

    def zoom_in(self, amount):
        pg.keyDown('ctrl')
        pg.scroll(amount)
        pg.keyUp('ctrl')

    def zoom_out(self, amount):
        pg.keyDown('ctrl')
        pg.scroll(-amount)
        pg.keyUp('ctrl')