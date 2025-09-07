# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:41

@author: Aidan
@project: HandGestureRecog
@filename: test_click_release
@description: 
- Python 
"""
import pyautogui
from pynput.mouse import Controller as MouseController, Button


def test_left_click():
    # pyautogui.mouseDown(button=pyautogui.RIGHT)
    MouseController().release(Button.right)
    MouseController().release(Button.right)
    pyautogui.click(x=1575, y=980)

def test_position():
    print(pyautogui.position())