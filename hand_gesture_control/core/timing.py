# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:25

@author: Aidan
@project: HandGestureRecog
@filename: timing
@description: debouncer, stopwatch and timing utilities
- Python 
"""
import time
from collections import defaultdict
from typing import Optional


class Debouncer:
    def __init__(self):
        self.last_called_times = defaultdict(float)

    def ok(self, key: str, min_dt: float):
        current_time = time.time()
        if key not in self.last_called_times or (current_time - self.last_called_times[key]) >= min_dt:
            self.last_called_times[key] = current_time
            return True
        return False

    def reset(self):
        self.last_called_times = defaultdict(float)


class Stopwatch:
    def __init__(self):
        """Initialize stopwatch in reset state"""
        self.start_time: Optional[float] = None
        self.paused: bool = False
        self.pause_time: Optional[float] = None
        self.total_paused_time: float = 0.0

    def reset(self):
        """
        Reset the stopwatch to zero and start timing immediately.
        """
        self.start_time = time.time()
        self.paused = False
        self.pause_time = None
        self.total_paused_time = 0.0

    def elapsed(self) -> float:
        """
        Get elapsed time in seconds since last reset.

        Returns:
            float: Elapsed time in seconds, excluding paused periods
        """
        if self.start_time is None:
            return 0.0

        if self.paused:
            # Return time elapsed before pause
            return self.pause_time - self.start_time - self.total_paused_time
        else:
            # Return current time minus start time, minus any paused time
            return time.time() - self.start_time - self.total_paused_time

    def pause(self):
        """Pause the stopwatch"""
        if not self.paused and self.start_time is not None:
            self.pause_time = time.time()
            self.paused = True

    def resume(self):
        """Resume the stopwatch after pausing"""
        if self.paused and self.pause_time is not None:
            # Add the current pause duration to total paused time
            self.total_paused_time += time.time() - self.pause_time
            self.paused = False
            self.pause_time = None

    def is_paused(self) -> bool:
        """Check if stopwatch is paused"""
        return self.paused

    def is_running(self) -> bool:
        """Check if stopwatch is running (started and not paused)"""
        return self.start_time is not None and not self.paused
