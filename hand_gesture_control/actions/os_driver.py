# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:39

@author: Aidan
@project: HandGestureRecog
@filename: os_driver
@description: Thin abstraction over OS input (mouse/keyboard) per platform
- Python 
"""
from abc import abstractmethod, ABC
from typing import List


class OSDriver(ABC):
    @abstractmethod
    def move(self, px, py):
        pass

    @abstractmethod
    def press_left(self):
        pass

    @abstractmethod
    def press_right(self):
        pass

    @abstractmethod
    def release_left(self):
        pass

    @abstractmethod
    def release_right(self):
        pass

    @abstractmethod
    def scroll(self, ticks):
        pass

    @abstractmethod
    def key_combo(self, keys: List[str]):
        pass

    @abstractmethod
    def zoom_in(self, amount):
        pass

    @abstractmethod
    def zoom_out(self, amount):
        pass
