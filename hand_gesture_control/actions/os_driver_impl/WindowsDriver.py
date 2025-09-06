# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 22:42

@author: Aidan
@project: HandGestureRecog
@filename: WindowsDriver
@description: 
- Python 
"""
import string
from typing import List

import pyautogui as pg
from pynput import keyboard, mouse
from pynput.keyboard import Controller as KeyController, Key
from pynput.mouse import Controller as MouseController, Button
from hand_gesture_control.actions.os_driver import OSDriver
from hand_gesture_control.config.constants import TAB_SHIFT_LEFT, TAB_SHIFT_RIGHT, SCROLL_SCALE


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

    def scroll(self, dx, dy):
        if abs(dx) > abs(dy):
            # scroll horizontally
            pg.hscroll(int(SCROLL_SCALE * dx))
        else:
            # vertical scroll
            pg.vscroll(int(SCROLL_SCALE * dy))

    def key_combo(self, keys: List[str]):
        pg.hotkey(*keys)

    def zoom_in(self, amount=10):
        pg.keyDown('ctrl')
        pg.scroll(amount)
        pg.keyUp('ctrl')

    def zoom_out(self, amount=10):
        pg.keyDown('ctrl')
        pg.scroll(-amount)
        pg.keyUp('ctrl')

    def release_all(self):
        """
        Release every possible key and mouse button.
        Useful as a panic reset so nothing stays 'stuck down'.
        """
        # --- Keyboard ---
        keys_to_release = []

        # All modifier keys
        keys_to_release.extend([
            Key.alt, Key.alt_l, Key.alt_r,
            Key.ctrl, Key.ctrl_l, Key.ctrl_r,
            Key.shift, Key.shift_l, Key.shift_r,
            Key.cmd, Key.cmd_l, Key.cmd_r,
            Key.caps_lock, Key.tab, Key.esc,
        ])

        # Function keys
        keys_to_release.extend([getattr(Key, f"f{i}") for i in range(1, 13)])

        # Arrow keys & specials
        keys_to_release.extend([
            Key.up, Key.down, Key.left, Key.right,
            Key.page_up, Key.page_down,
            Key.home, Key.end, Key.insert, Key.delete,
            Key.backspace, Key.space, Key.enter
        ])

        # All printable characters (letters, digits, punctuation)
        keys_to_release.extend(list(string.printable))

        # Try to release all
        for k in keys_to_release:
            try:
                pg.keyUp(k)
            except Exception:
                pass  # Some keys may not be supported on all OS

        # --- Mouse ---
        try:
            self.release_left()
        except Exception:
            pass
        try:
            self.release_right()
        except Exception:
            pass
        try:
            pg.mouseUp(button=pg.MIDDLE)
        except Exception:
            pass

    def tab_shift(self, direction):
        if direction == TAB_SHIFT_LEFT:
            self.key_combo(['alt', 'tab'])
        elif direction == TAB_SHIFT_RIGHT:
            self.key_combo(['alt', 'shift', 'tab'])
