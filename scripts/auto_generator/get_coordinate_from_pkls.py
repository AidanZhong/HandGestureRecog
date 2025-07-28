"""
Author: Aidan Zhong
Date: 2025/7/28 22:56
Description:
"""
import os
import pickle

import numpy as np

pkl_dir = 'handsOnly_REGISTRATIONS_r_lm___POSES'
coor_dir = 'joint_coordinates'
os.makedirs(coor_dir, exist_ok=True)

for f in os.listdir(pkl_dir):
    if f.endswith('.pkl'):
        with open(os.path.join(pkl_dir, f), 'rb') as f:
            data = pickle.load(f, encoding='latin1')
        joints = data['J_transformed']

        f_n = f.name.split('/')[-1].rstrip('.pkl')
        np.save(os.path.join(coor_dir, f'{f_n}.npy'), joints)
        np.savetxt(os.path.join(coor_dir, f'{f_n}.csv'), joints, delimiter=',', header='x,y,z')
