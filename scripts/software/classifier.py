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
                    for idx, l in enumerate(hand_landmarks.landmark):
                        x, y = int(l.x * w), int(l.y * h)
                        coordinates.append((x, y))

                        # draw it on the image
                        cv2.circle(image, (x, y), 5, (255, 0, 0), cv2.FILLED)
                        cv2.putText(image, str(idx), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

                    coordinates = np.array(coordinates)
                    coordinates = coordinates.flatten()
                    hands.append(coordinates)

            if not hands:
                continue
            preds = model.predict(np.array(hands))
            for i in preds:
                pred_text += mapper[i]
            cv2.putText(image, pred_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)
            cv2.imshow('gesture_recognition', image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(e)
            continue
