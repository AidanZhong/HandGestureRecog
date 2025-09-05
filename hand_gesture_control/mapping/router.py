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
    def __init__(self, driver, rules, debouncer, cfg: RouterConfig = RouterConfig()):
        """
        driver: Action driver facade (actions/driver.py)
        rules:  module/object exposing axis_dominance, is_zoom_in, is_zoom_out, tab_flick
        debouncer: Debouncer instance
        """
        self.driver = driver
        self.rules = rules
        self.db = debouncer
        self.cfg = cfg

    def handle(self, event, hist, modes, clicks):
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
        if hist.prev_pose is not None:
            dx = event.pos.x - hist.prev_pose.x
            dy = event.pos.y - hist.prev_pose.y

        # sequence checks: zoom in/out
        if prev_gid is not None:
            if self.rules.is_zoom_in(prev_gid, gid) and self.db.ok("zoom_in", self.cfg.debounce_s):
                self.driver.zoom_in()
            if self.rules.is_zoom_out(prev_gid, gid) and self.db.ok("zoom_out", self.cfg.debounce_s):
                self.driver.zoom_out()

        # release gesture (hard reset of buttons/modes)
        if gid == self.driver.GestureId.RELEASE:
            self.driver.release_all(clicks, modes)
            self._update_history(hist, event)
            return

        # continuous handlers
        if gid == self.driver.GestureId.MOVE:
            self.driver.pointer_move(event)

        elif gid == self.driver.GestureId.DRAG_SCROLL:
            # decide drag vs scroll
            decision = self.rules.axis_dominance(dx, dy, self.cfg.axis_ratio, self.cfg.motion_thresh)
            self.driver.drag_scroll(event, hist, decision, modes, clicks, self.db, self.cfg)

        elif gid == self.driver.GestureId.TAB_SHIFT:
            direction = self.rules.tab_flick(dx, self.cfg.tab_flick_thresh)
            if direction != 0 and self.db.ok(f"tab_{direction}", self.cfg.debounce_s):
                self.driver.tab_shift(direction)

        elif gid == self.driver.GestureId.LCLICK:
            self.driver.click_left_down(clicks)

        elif gid == self.driver.GestureId.RCLICK:
            self.driver.click_right_down(clicks)

        elif gid == self.driver.GestureId.HANDWRITE:
            if prev_gid != self.driver.GestureId.HANDWRITE:
                self.driver.handwriting_enter(modes, clicks)
            self.driver.handwriting_update(event)

        # mode exits
        if prev_gid == self.driver.GestureId.DRAG_SCROLL and gid != self.driver.GestureId.DRAG_SCROLL:
            self.driver.drag_scroll_exit(modes, clicks)

        if prev_gid == self.driver.GestureId.HANDWRITE and gid != self.driver.GestureId.HANDWRITE:
            self.driver.handwriting_exit(modes, clicks)

        # update history
        self._update_history(hist, event)

        return dx, dy

    @staticmethod
    def _update_history(hist, event):
        hist.prev_gesture = event.gesture
        hist.prev_pos = event.pos
        hist.prev_time = event.t
