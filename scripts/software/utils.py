"""
Author: Aidan Zhong
Date: 2025/8/18 20:09
Description:
"""
import pyautogui as pg

all_keys_keyboard = ['left', 'right']
all_keys_mouse = ['command', 'ctrl', 'tab', 'shift']


def cursor_move(dx, dy):
    pg.moveRel(dx, dy)


def drag(dx, dy):
    pg.mouseDown(button='left')
    pg.moveRel(dx, dy)
    pg.mouseUp(button='left')


def scroll(amount):
    pg.scroll(amount)


def shift_next_tab():
    pg.hotkey('ctrl', 'tab')


def shift_prev_tabs():
    pg.hotkey('ctrl', 'shift', 'tab')


def left_click_down():
    pg.mouseDown(button='left')


def right_click_down():
    pg.mouseDown(button='right')


def release_click():
    try:
        for key in all_keys_mouse:
            pg.mouseUp(key)
        for key in all_keys_keyboard:
            pg.keyUp(key)
    except:
        pass


def zoom_in(amount):
    pg.keyDown('ctrl')
    pg.scroll(amount)
    pg.keyUp('ctrl')


def zoom_out(amount):
    pg.keyDown('ctrl')
    pg.scroll(-amount)
    pg.keyUp('ctrl')


def hand_write():
    # todo finish the hand write afterwards
    return
