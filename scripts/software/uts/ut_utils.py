"""
Author: Aidan Zhong
Date: 2025/8/18 20:41
Description:
"""
import pyautogui as pg

from scripts.software import utils


def test_cursor_move():
    utils.cursor_move(200, 200)


def test_drag():
    utils.drag(200, 200)


def test_scroll():
    utils.scroll(20)


def test_shift_next_tab():
    utils.shift_next_tab()


def test_shift_prev_tab():
    utils.shift_prev_tabs()


def test_right_click():
    utils.right_click_down()
    pg.sleep(0.1)
    utils.release_click()


def test_left_click():
    utils.left_click_down()
    pg.sleep(0.1)
    utils.release_click()


def test_zoom_in():
    utils.zoom_in(10)


def test_zoom_out():
    utils.zoom_out(10)
