"""
Author: Aidan Zhong
Date: 2025/7/22 05:04
Description:
"""
import os

import cv2
import mediapipe as mp
import numpy as np


# # Load image
# image = cv2.imread('../../docs/gesture_design/img.png')
# image = cv2.imread('../../scripts/auto_generator/ply2obj2img/01_01r.png')
# image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=True,
#                        max_num_hands=1)
#
# results = hands.process(image_rgb)
# mp_drawing = mp.solutions.drawing_utils
#
# if results.multi_hand_landmarks:
#     for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
#         mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
#         coordinates = []
#         for i, lm in enumerate(hand_landmarks.landmark):
#             h, w, _ = image.shape
#             x, y, z = int(lm.x * w), int(lm.y * h), lm.z
#             coordinates.append([x, y, z])
#             print(f"Landmark {i}: x={x}, y={y}, z={z:.4f}")
#         np.save(f'Hand_{idx}.npy', coordinates)
#
# cv2.imshow("Hand", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


def extract_feature(dir):
    files = set(os.listdir(dir))
    for f in os.listdir(dir):
        sub_path = os.path.join(dir, f)
        if not os.path.isdir(sub_path):
            # might be a file
            # if os.path.basename(sub_path) + '.npy' in files:
            #     continue
            if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png'):
                print(f'processing {sub_path}')
                get_mediapipe_preds(sub_path, True)
        else:
            # nested folder
            extract_feature(sub_path)


def get_mediapipe_preds(img_path, save=False):
    '''if save, it will not return'''
    try:
        image = cv2.imread(img_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=True,
                               max_num_hands=1)

        results = hands.process(image_rgb)
        hands = []
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                coordinates = []
                for i, lm in enumerate(hand_landmarks.landmark):
                    h, w, _ = image.shape
                    x, y, z = int(lm.x * w), int(lm.y * h), lm.z
                    coordinates.append([x, y])
                    # print(f"Landmark {i}: x={x}, y={y}, z={z:.4f}")
                if save:
                    np.save(f'{img_path}.npy', coordinates, allow_pickle=True)
                    del coordinates
                else:
                    hands.append(coordinates)
        else:
            print('Can\t recognize hands')
            # os.remove(img_path)
            return
        return hands
    except:
        print(img_path)


# if __name__ == '__main__':
#     dir = '../../data/data/dataset1/gesture1/s1'
#     extract_feature(dir)
