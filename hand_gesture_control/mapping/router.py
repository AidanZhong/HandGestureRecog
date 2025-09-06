# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:29

@author: Aidan
@project: HandGestureRecog
@filename: router
@description: Dispatches GestureEvent to controllers based on mapping rules
- Python 
"""
from dataclasses import dataclass
from typing import Optional

from hand_gesture_control.actions.os_driver import OSDriver
from hand_gesture_control.config.constants import DEADZONE_EPS, FRAME_WIDTH, FRAME_HEIGHT, MOVING_SCALE
from hand_gesture_control.core.filters import apply_deadzone
from hand_gesture_control.core.state import History
from hand_gesture_control.core.types import GestureId, GestureEvent
from hand_gesture_control.mapping.rules import Rules


@dataclass
class RouterConfig:
    tab_flick_thresh: float = 0.03
    motion_thresh: float = 0.02
    axis_ratio: float = 1.3
    debounce_s: float = 0.35


class GestureRouter:
    """
    Orchestrates per-frame decisions in the exact order we specified:
      1) sequence checks (zoom)
      2) release gesture
      3) continuous handlers (move/drag/scroll/tab/handwrite)
      4) mode exits
      5) update history
    """

    def __init__(self, driver: OSDriver, debouncer, cfg: RouterConfig = RouterConfig()):
        """
        driver: Action driver facade (actions/driver.py)
        rules:  module/object exposing axis_dominance, is_zoom_in, is_zoom_out, tab_flick
        debouncer: Debouncer instance
        """
        self.driver = driver
        self.db = debouncer
        self.cfg = cfg

    def handle(self, event: GestureEvent, hist: History, modes, clicks, ema):
        """
        event: GestureEvent
        hist:  History
        modes: ModeState
        clicks: ClickState
        """
        if event is None:
            return  # drop frame quietly

        gid = event.gesture
        prev_gid = getattr(hist, "prev_gesture", None)

        # Compute motion deltas in normalized space
        dx = dy = 0.0
        if hist.prev_pos is not None:
            dx = event.pos.x - hist.prev_pos.x
            dy = event.pos.y - hist.prev_pos.y

        # sequence checks: zoom in/out
        if prev_gid is not None:
            if Rules.is_zoom_in(prev_gid, gid) and self.db.ok("zoom_in", self.cfg.debounce_s):
                self.driver.zoom_in()
            if Rules.is_zoom_out(prev_gid, gid) and self.db.ok("zoom_out", self.cfg.debounce_s):
                self.driver.zoom_out()

        # release gesture (hard reset of buttons/modes)
        if gid == GestureId.RELEASE:
            self.driver.release_all()
            self._update_history(hist, event)
            return

        # continuous handlers
        if gid == GestureId.MOVE:
            if hist.prev_pos is not None:
                # calculate the dx and dy
                dx, dy = event.pos.delta(hist.prev_pos)
                dx, dy = apply_deadzone(dx, dy, DEADZONE_EPS)
                if not dx == dy == 0.0:
                    smoothed_dx, smoothed_dy = ema.step(
                        dx * FRAME_WIDTH * MOVING_SCALE,
                        dy * FRAME_HEIGHT * MOVING_SCALE)
                    self.driver.move(smoothed_dx, smoothed_dy)
                    print('----------------')
                    print(dx, dy)
                    print(event.pos.x * FRAME_WIDTH * MOVING_SCALE, event.pos.y * FRAME_HEIGHT * MOVING_SCALE)
                    print(smoothed_dx, smoothed_dy)

        elif gid == GestureId.DRAG_SCROLL:
            if hist.prev_pos is not None:
                dx, dy = event.pos.delta(hist.prev_pos)
                self.driver.scroll(dx, dy)

        elif gid == GestureId.TAB_SHIFT:
            direction = Rules.tab_flick(dx, self.cfg.tab_flick_thresh)
            if direction != 0 and self.db.ok(f"tab_{direction}", self.cfg.debounce_s):
                self.driver.tab_shift(direction)

        elif gid == GestureId.LCLICK:
            self.driver.press_left()

        elif gid == GestureId.RCLICK:
            self.driver.press_right()

        elif gid == GestureId.HANDWRITE:
            pass
            # if prev_gid != GestureId.HANDWRITE:
            #     self.driver.handwriting_enter(modes, clicks)
            # self.driver.handwriting_update(event)

        # update history
        self._update_history(hist, event)

        return dx, dy

    @staticmethod
    def _update_history(hist, event):
        hist.prev_gesture = event.gesture
        hist.prev_pos = event.pos
        hist.prev_time = event.t
