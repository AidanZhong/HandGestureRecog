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

image = cv2.imread(image_path)
joints_df = pd.read_csv(joints_path)
joints = joints_df[["u", "v"]].values.astype(int)

for (x, y) in joints:
    cv2.circle(image, (x, y), radius=4, color=(0, 0, 255), thickness=-1)

cv2.imshow("Joints", image)
cv2.waitKey(0)
cv2.destroyAllWindows()