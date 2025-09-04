# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:29

@author: Aidan
@project: HandGestureRecog
@filename: router
@description: Dispatches GestureEvent to controllers based on mapping rules
- Python 
"""
from hand_gesture_control.core.state import History, ModeState
from hand_gesture_control.core.types import GestureEvent


class GestureRouter:
    def __init__(self, engine, cfg, debouncer):
        self.engine = engine
        self.cfg = cfg
        self.debouncer = debouncer

    def handle(self, event: GestureEvent, hist: History, modes: ModeState):
        '''
            Orchestrate order of operations per frame
            1. check sequences
            2. handle release
            3. run continuous controller based on gestures
            4. handle mode exits
            5. update history
        '''
        # todo
