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
    def __init__(self, engine, rules, debouncer, cfg: RouterConfig = RouterConfig()):
        """
        engine: ActionEngine facade (actions/engine.py)
        rules:  module/object exposing axis_dominance, is_zoom_in, is_zoom_out, tab_flick
        debouncer: Debouncer instance
        """
        self.engine = engine
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
                self.engine.zoom_in()
            if self.rules.is_zoom_out(prev_gid, gid) and self.db.ok("zoom_out", self.cfg.debounce_s):
                self.engine.zoom_out()

        # release gesture (hard reset of buttons/modes)
        if gid == self.engine.GestureId.RELEASE:
            self.engine.release_all(clicks, modes)
            self._update_history(hist, event)
            return

        # continuous handlers
        if gid == self.engine.GestureId.MOVE:
            self.engine.pointer_move(event)

        elif gid == self.engine.GestureId.DRAG_SCROLL:
            # decide drag vs scroll
            decision = self.rules.axis_dominance(dx, dy, self.cfg.axis_ratio, self.cfg.motion_thresh)
            self.engine.drag_scroll(event, hist, decision, modes, clicks, self.db, self.cfg)

        elif gid == self.engine.GestureId.TAB_SHIFT:
            direction = self.rules.tab_flick(dx, self.cfg.tab_flick_thresh)
            if direction != 0 and self.db.ok(f"tab_{direction}", self.cfg.debounce_s):
                self.engine.tab_shift(direction)

        elif gid == self.engine.GestureId.LCLICK:
            self.engine.click_left_down(clicks)

        elif gid == self.engine.GestureId.RCLICK:
            self.engine.click_right_down(clicks)

        elif gid == self.engine.GestureId.HANDWRITE:
            if prev_gid != self.engine.GestureId.HANDWRITE:
                self.engine.handwriting_enter(modes, clicks)
            self.engine.handwriting_update(event)

        # mode exits
        if prev_gid == self.engine.GestureId.DRAG_SCROLL and gid != self.engine.GestureId.DRAG_SCROLL:
            self.engine.drag_scroll_exit(modes, clicks)

        if prev_gid == self.engine.GestureId.HANDWRITE and gid != self.engine.GestureId.HANDWRITE:
            self.engine.handwriting_exit(modes, clicks)

        # update history
        self._update_history(hist, event)

        return dx, dy

    @staticmethod
    def _update_history(hist, event):
        hist.prev_gesture = event.gesture
        hist.prev_pos = event.pos
        hist.prev_time = event.t
