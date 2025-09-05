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
from hand_gesture_control.input.device_probe import open_camera
from hand_gesture_control.input.stream_adapter import AdapterConfig, StreamAdapter
from mapping.router import GestureRouter, RouterConfig
import mapping.rules as rules
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
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                coordinates = []
                h, w, _ = frame.shape
                for idx, l in enumerate(hand_landmarks.landmark):
                    x, y = int(l.x * w), int(l.y * h)
                    coordinates.append((x, y))

                    # draw it on the image
                    cv2.circle(frame, (x, y), 5, (255, 0, 0), cv2.FILLED)
                    cv2.putText(frame, str(idx), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

                coordinates = np.array(coordinates)
                coordinates = coordinates.flatten()
                hands.append(coordinates)
        if not hands:
            return None

        preds = model.predict(np.array(hands))
        res = dict()
        res['hands'] = hands[0]
        res['gesture'] = preds[0]
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
    driver = OSDriver()  # make sure it exposes .GestureId enum

    # 2) Adapter config
    adapter_cfg = AdapterConfig(
        expect_pixels=False,
        mirror_x=True,
        roi=None,
        min_hand_conf=0.6
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
    router = GestureRouter(driver=driver, rules=rules, debouncer=debouncer, cfg=router_cfg)

    # 4) UI
    hud = OverlayHUD()

    # 5) States
    hist = History(prev_gesture=None, prev_pos=None, prev_time=monotonic())
    modes = ModeState(drag_mode=False, draw_mode=False, armed=False)
    clicks = ClickState(left_down=False, right_down=False)

    return driver, adapter, router, hud, hist, modes, clicks


def main():
    cfg = AppConfig()
    engine, adapter, router, hud, hist, modes, clicks = build_app()
    detector = Detector()

    try:
        while True:
            frame, det_out = detector.next_frame()
            if frame is None:
                break

            # Adapt detector output → GestureEvent (or None)
            event = adapter.to_event(det_out)

            # Route and act
            result = router.handle(event, hist, modes, clicks)
            dx, dy = (0.0, 0.0)
            if isinstance(result, tuple) and len(result) == 2:
                dx, dy = result

            # HUD
            if cfg.show_hud:
                gesture_label = str(event.gesture.name) if event else "-"
                frame = hud.draw(frame, gesture_label,
                                 active=modes.drag_mode or modes.draw_mode or clicks.left_down or clicks.right_down,
                                 dx=dx, dy=dy)

            cv2.imshow(cfg.window_name, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC to quit
                break

        # safety on exit, ensure all buttons released
        engine.release_all(clicks, modes)

    finally:
        detector.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
