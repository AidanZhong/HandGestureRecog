# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 22:42

@author: Aidan
@project: HandGestureRecog
@filename: WindowsDriver
@description: 
- Python 
"""
import ctypes
import string
import time
from typing import List

import pyautogui as pg
from pynput.keyboard import Controller as KeyController, Key
from pynput.mouse import Controller as MouseController, Button
from win32con import MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP

from hand_gesture_control.actions.os_driver import OSDriver
from hand_gesture_control.config.constants import TAB_SHIFT_LEFT, TAB_SHIFT_RIGHT, SCROLL_SCALE


class WindowsDriver(OSDriver):
    def __init__(self):
        pg.FAILSAFE = False
        pass

    def move(self, px, py):
        pg.moveRel(px, py)

    def hard_left_click(self):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def press_left(self):
        print('press left')
        pg.mouseDown(button=pg.LEFT)

    def press_right(self):
        print('press right')
        pg.click(button=pg.RIGHT)

    def release_left(self):
        MouseController().release(button=Button.left)

    def release_right(self):
        MouseController().release(button=Button.right)

    def scroll(self, dx, dy):
        if abs(dx) > abs(dy):
            # scroll horizontally
            pg.hscroll(int(SCROLL_SCALE * dx))
        else:
            # vertical scroll
            pg.vscroll(int(SCROLL_SCALE * dy))

    def key_combo(self, keys: List[str]):
        pg.hotkey(*keys)

    def zoom_in(self, amount=100):
        pg.keyDown('ctrl')
        pg.scroll(amount)
        time.sleep(1)
        pg.keyUp('ctrl')

    def zoom_out(self, amount=100):
        pg.keyDown('ctrl')
        pg.scroll(-amount)
        time.sleep(1)
        pg.keyUp('ctrl')

    def release_all(self):
        """
        Release every possible key and mouse button.
        Useful as a panic reset so nothing stays 'stuck down'.
        """
        try:
            self.release_left()
        except Exception:
            pass
        try:
            self.release_right()
        except Exception:
            pass

    def tab_shift(self, direction):
        if direction == TAB_SHIFT_LEFT:
            self.key_combo(['alt', 'tab'])
        elif direction == TAB_SHIFT_RIGHT:
            self.key_combo(['alt', 'shift', 'tab'])
