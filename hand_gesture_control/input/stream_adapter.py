# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:28

@author: Aidan
@project: HandGestureRecog
@filename: stream_adapter
@description: adapts my detector outputs to Gesture event
- Python 
"""

from time import monotonic
from hand_gesture_control.core.types import Position2D, GestureEvent, GestureId
from dataclasses import dataclass
from time import monotonic


@dataclass
class AdapterConfig:
    expect_pixels: bool = False
    frame_width: int = 1280
    frame_height: int = 720
    mirror_x: bool = True
    roi: tuple = None
    min_hand_conf: float = 0.6
    id_map: dict = None


class StreamAdapter:
    def __init__(self, cfg: AdapterConfig):
        self.cfg = cfg

    def to_event(self, det_out) -> GestureEvent:
        """Convert detector output dict → GestureEvent"""
        hands = det_out.get("hands")

        x_raw, y_raw = hands

        # normalize coords
        if self.cfg.expect_pixels:
            u = x_raw / self.cfg.frame_width
            v = y_raw / self.cfg.frame_height
        else:
            u, v = float(x_raw), float(y_raw)

        if self.cfg.mirror_x:
            u = 1.0 - u

        # clamp
        u, v = max(0.0, min(1.0, u)), max(0.0, min(1.0, v))

        gid = det_out.get("gesture")

        # timestamp
        t = det_out.get("t", monotonic())

        return GestureEvent(gesture=GestureId(gid), pos=Position2D(u, v), t=t)
