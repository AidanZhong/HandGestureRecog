"""
Author: Aidan Zhong
Date: 2025/7/28 20:05
Description:
"""
import trimesh
import numpy as np

ply_path = "handsOnly_REGISTRATIONS_r_lm___POSES/01_01r.ply"
mesh = trimesh.load(ply_path, process=False)

joints = np.array(mesh.vertices)  # shape: (21, 3)
np.savetxt("joints.csv", joints, delimiter=',', header='x,y,z', comments='')