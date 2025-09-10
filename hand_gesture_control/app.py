# -*- coding: utf-8 -*-
"""
Created on 2025/9/4 12:19

@author: Aidan
@project: HandGestureRecog
@filename: app
@description: 
- Python 
"""
from time import monotonic

import cv2
from dataclasses import dataclass

import joblib
import numpy as np

from core.timing import Debouncer
from core.state import PointerState, ClickState, ModeState, History
from hand_gesture_control.actions.os_driver import OSDriver
from hand_gesture_control.actions.os_driver_impl.WindowsDriver import WindowsDriver
from hand_gesture_control.config.constants import EMA_ALPHA
from hand_gesture_control.core.filters import EMA
from hand_gesture_control.input.device_probe import open_camera
from hand_gesture_control.input.stream_adapter import AdapterConfig, StreamAdapter
from mapping.router import GestureRouter, RouterConfig
import mediapipe as mp
from ui.overlay import OverlayHUD


class Detector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )
        self.cap = open_camera()

    def next_frame(self):
        ok, frame = self.cap.read()
        if not ok:
            return None, None
        frame = cv2.flip(frame, 1)
        det_out = self._run_gesture_model(frame)
        return frame, det_out

    def _run_gesture_model(self, frame):
        model = joblib.load('../scripts/classifier/logistic_regression.pkl')
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.mp_hands.process(image_rgb)

        hands = []
        wrist_pos = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                coordinates = []
                h, w, _ = frame.shape
                for idx, l in enumerate(hand_landmarks.landmark):
                    x, y = int(l.x * w), int(l.y * h)
                    coordinates.append((x, y))

                    # draw it on the image
                    if idx == 0:
                        # applying wrist as the position of the hand
                        wrist_pos = [x, y]
                    cv2.circle(frame, (x, y), 5, (255, 0, 0), cv2.FILLED)
                    cv2.putText(frame, str(idx), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

                coordinates = np.array(coordinates)
                coordinates = coordinates.flatten()
                hands.append(coordinates)
        if not hands:
            return None

        preds = model.predict(np.array(hands))
        res = dict()
        res['hands'] = wrist_pos
        res['gesture'] = preds[0] + 1
        res['t'] = monotonic()

        return res

    def release(self):
        self.cap.release()


@dataclass
class AppConfig:
    show_hud: bool = True
    window_name: str = "Hand Control"


def build_app():
    # 1) Actions driver (with OS driver & controllers inside)
    driver = WindowsDriver()

    # 2) Adapter config
    adapter_cfg = AdapterConfig(
        expect_pixels=True,
        mirror_x=False
    )
    adapter = StreamAdapter(adapter_cfg)

    # 3) Router + debouncer
    router_cfg = RouterConfig(
        tab_flick_thresh=0.03,
        motion_thresh=0.02,
        axis_ratio=1.3,
        debounce_s=0.35
    )
    debouncer = Debouncer()
    router = GestureRouter(driver=driver, debouncer=debouncer, cfg=router_cfg)

    # 4) UI
    hud = OverlayHUD()

    # 5) States
    hist = History(prev_gesture=None, prev_pos=None, prev_time=monotonic())
    modes = ModeState(drag_mode=False, draw_mode=False, armed=False)
    clicks = ClickState(left_down=False, right_down=False)

    # 6) EMA
    ema = EMA(EMA_ALPHA)

    return driver, adapter, router, hud, hist, modes, clicks, ema


def main():
    cfg = AppConfig()
    driver, adapter, router, hud, hist, modes, clicks, ema = build_app()
    detector = Detector()
    cv2.namedWindow(cfg.window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(cfg.window_name, cv2.WND_PROP_TOPMOST, 1)

    try:
        while True:
            start_time_stamp = monotonic()
            frame, det_out = detector.next_frame()
            if frame is None or det_out is None:
                continue

            # Adapt detector output → GestureEvent (or None)
            event = adapter.to_event(det_out)

            # Route and act
            result = router.handle(event, hist, modes, clicks, ema)
            dx, dy = (0.0, 0.0)
            if isinstance(result, tuple) and len(result) == 2:
                dx, dy = result

            # HUD
            if cfg.show_hud:
                gesture_label = str(event.gesture.name) if event else "-"
                frame = hud.draw(frame, gesture_label,
                                 active=modes.drag_mode or modes.draw_mode or clicks.left_down or clicks.right_down,
                                 dx=dx, dy=dy)
            cv2.setWindowProperty(cfg.window_name, cv2.WND_PROP_TOPMOST, 1)
            cv2.imshow(cfg.window_name, frame)
            end_time_stamp = monotonic()

            print(f'gesture: {event.gesture.name} used {end_time_stamp - start_time_stamp} seconds')

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC to quit
                break

        # safety on exit, ensure all buttons released
        driver.release_all()

    finally:
        detector.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
