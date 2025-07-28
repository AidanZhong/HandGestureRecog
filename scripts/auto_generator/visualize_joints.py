"""
Author: Aidan Zhong
Date: 2025/7/28 23:40
Description:
"""
import cv2
import pandas as pd
import numpy as np
import os

image_path = "ply2obj2img/01_01r.png"
joints_path = "ply2obj2img/01_01r_joints2d.csv"

mano_edges = [
    (0, 1), (1, 2), (2, 3), (3, 4),      # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),      # Index
    (0, 9), (9, 10), (10, 11), (11, 12), # Middle
    (0, 13), (13, 14), (14, 15)          # Ring
]

image = cv2.imread(image_path)
joints_df = pd.read_csv(joints_path)
joints = joints_df[["u", "v"]].values.astype(int)

for (x, y) in joints:
    cv2.circle(image, (x, y), radius=4, color=(0, 0, 255), thickness=-1)

for start, end in mano_edges:
    x1, y1 = joints[start]
    x2, y2 = joints[end]
    cv2.line(image, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

cv2.imshow("Joints", image)
cv2.waitKey(0)
cv2.destroyAllWindows()