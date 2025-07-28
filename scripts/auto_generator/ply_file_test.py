"""
Author: Aidan Zhong
Date: 2025/7/28 17:55
Description:
"""
import os

import trimesh

mesh = trimesh.load('handsOnly_REGISTRATIONS_r_lm___POSES/01_01r.ply')
print(mesh.vertices.shape)
print(mesh.faces.shape)

ply_dir = 'handsOnly_REGISTRATIONS_r_lm___POSES'
obj_dir = 'ply2obj'
os.makedirs(obj_dir, exist_ok=True)

for filename in os.listdir(ply_dir):
    if filename.endswith('.ply'):
        mesh = trimesh.load(os.path.join(ply_dir, filename))
        out = os.path.join(obj_dir, filename.replace('.ply', '.obj'))
        mesh.export(out)