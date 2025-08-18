"""
Author: Aidan Zhong
Date: 2025/8/18 21:41
Description:
"""
import joblib

from scripts.software.classifier import get_gesture
from scripts.software.stream_controller import *


def test_stream():
    cap = open_camera()
    stream_preview(cap)


def test_all():
    cap = open_camera()
    model = joblib.load('../../classifier/logistic_regression.pkl')
    get_gesture(cap, model)
