# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:39

@author: Aidan
@project: HandGestureRecog
@filename: overlay
@description: On-screen diagnostics (gesture label, ACTIVE/IDLE, Δx/Δy bars)
- Python 
"""
from dataclasses import dataclass
import cv2
import time

@dataclass
class OverlayStyle:
    fg_ok: tuple = (60, 220, 60)     # green
    fg_warn: tuple = (60, 60, 220)   # red/blue-ish
    fg_text: tuple = (240, 240, 240)
    bar_bg: tuple = (50, 50, 50)
    bar_fg: tuple = (120, 200, 255)
    font: int = cv2.FONT_HERSHEY_SIMPLEX
    alpha: float = 0.7               # overall transparency for panel

class OverlayHUD:
    """
    Lightweight diagnostics overlay:
      - Gesture label
      - ACTIVE/IDLE state
      - dx/dy magnitude bars
      - FPS
    """
    def __init__(self, style: OverlayStyle = OverlayStyle()):
        self.s = style
        self._last_t = time.time()
        self._fps = 0.0

    def _update_fps(self):
        t = time.time()
        dt = t - self._last_t
        if dt > 0:
            # EMA for FPS to stabilize the number on screen
            self._fps = 0.85 * self._fps + 0.15 * (1.0 / dt) if self._fps > 0 else (1.0 / dt)
        self._last_t = t

    def draw(self, frame, gesture_label: str, active: bool, dx: float, dy: float):
        """
        Draw overlay onto the input BGR frame (OpenCV image).
        dx/dy are normalized deltas in [-1,1] (or any small range).
        """
        self._update_fps()
        h, w = frame.shape[:2]

        # Panel rectangle
        panel_w, panel_h = int(0.42 * w), int(0.16 * h)
        x0, y0 = 12, 12
        x1, y1 = x0 + panel_w, y0 + panel_h

        # translucent background
        panel = frame.copy()
        cv2.rectangle(panel, (x0, y0), (x1, y1), (35, 35, 35), thickness=-1)
        cv2.addWeighted(panel, self.s.alpha, frame, 1 - self.s.alpha, 0, frame)

        # Text lines
        line1 = f"Gesture: {gesture_label or '-'}"
        line2 = f"State:   {'ACTIVE' if active else 'IDLE'}"
        line3 = f"FPS:     {self._fps:4.1f}"

        col = self.s.fg_ok if active else self.s.fg_warn
        cv2.putText(frame, line1, (x0 + 14, y0 + 28), self.s.font, 0.7, self.s.fg_text, 2, cv2.LINE_AA)
        cv2.putText(frame, line2, (x0 + 14, y0 + 56), self.s.font, 0.7, col, 2, cv2.LINE_AA)
        cv2.putText(frame, line3, (x0 + 14, y0 + 84), self.s.font, 0.6, self.s.fg_text, 2, cv2.LINE_AA)

        # dx/dy bars
        bar_w = panel_w - 28
        bar_h = 12
        bx = x0 + 14
        by = y0 + 110

        def draw_bar(label, value, yoff):
            cv2.putText(frame, label, (bx, by + yoff - 4), self.s.font, 0.5, self.s.fg_text, 1, cv2.LINE_AA)
            # background
            cv2.rectangle(frame, (bx, by + yoff + 4), (bx + bar_w, by + yoff + 4 + bar_h), self.s.bar_bg, -1)
            # value (map [-0.1, 0.1] to [0..1] clamped)
            v = max(-0.1, min(0.1, value)) / 0.1
            mid = bx + bar_w // 2
            if v >= 0:
                endx = int(mid + v * (bar_w // 2))
                cv2.rectangle(frame, (mid, by + yoff + 4), (endx, by + yoff + 4 + bar_h), self.s.bar_fg, -1)
            else:
                endx = int(mid + v * (bar_w // 2))
                cv2.rectangle(frame, (endx, by + yoff + 4), (mid, by + yoff + 4 + bar_h), self.s.bar_fg, -1)
            # mid line
            cv2.line(frame, (mid, by + yoff + 4), (mid, by + yoff + 4 + bar_h), (80, 80, 80), 1)

        draw_bar("dx", dx, 0)
        draw_bar("dy", dy, 26)

        return frame 
