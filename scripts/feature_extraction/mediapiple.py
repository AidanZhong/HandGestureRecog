"""
Author: Aidan Zhong
Date: 2025/7/22 05:04
Description:
"""
import cv2
import mediapipe as mp
import numpy as np

# Load image
image = cv2.imread('../../docs/gesture_design/img.png')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True,
                       max_num_hands=2,
                       min_detection_confidence=0.5)

results = hands.process(image_rgb)
mp_drawing = mp.solutions.drawing_utils

if results.multi_hand_landmarks:
    for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        coordinates = []
        for i, lm in enumerate(hand_landmarks.landmark):
            h, w, _ = image.shape
            x, y, z = int(lm.x * w), int(lm.y * h), lm.z
            coordinates.append([x, y, z])
            print(f"Landmark {i}: x={x}, y={y}, z={z:.4f}")
        np.save(f'Hand_{idx}.npy', coordinates)

cv2.imshow("Hand", image)
cv2.waitKey(0)
cv2.destroyAllWindows()