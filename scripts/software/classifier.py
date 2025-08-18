"""
Author: Aidan Zhong
Date: 2025/8/18 22:56
Description:
"""
import cv2
import mediapipe as mp
import numpy as np

mapper = {
    0: 'gesture1',
    1: 'gesture2',
    2: 'gesture3',
    3: 'gesture4',
    4: 'gesture5',
    5: 'gesture6',
    6: 'gesture7',
    7: 'gesture8'
}


def get_gesture(cap, model):
    mp_hands = mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8
    )

    while cap.isOpened():
        try:
            flag, image = cap.read()
            if not flag:
                continue

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = mp_hands.process(image_rgb)

            pred_text = ''
            hands = []
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    coordinates = []
                    h, w, _ = image.shape
                    for l in hand_landmarks.landmark:
                        x, y = int(l.x * w), int(l.y * h)
                        coordinates.append((x, y))
                    coordinates = np.array(coordinates)
                    coordinates = coordinates.flatten()
                    hands.append(coordinates)
            preds = model.predict(np.array(hands))
            for i in preds:
                pred_text += mapper[i]
            cv2.putText(image, pred_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)
            cv2.imshow('gesture_recognition', image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        except:
            continue
