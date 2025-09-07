# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:41

@author: Aidan
@project: HandGestureRecog
@filename: test_click_release
@description: 
- Python 
"""
import pyautogui as pg
from pynput.mouse import Controller as MouseController, Button


def test_left_click():
    pg.mouseDown(button=pg.LEFT)
    pg.moveRel(100, 100)
    pg.mouseUp(button=pg.LEFT)
    pg.moveRel(-50, -50)

def test_position():
    print(pg.position())