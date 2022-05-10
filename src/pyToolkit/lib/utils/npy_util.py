# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       npy_util
   Description:
   Author:     bowen
   date:        2/19/19
-------------------------------------------------
"""

import numpy as np


def load_npy(fpath):
    return np.load(fpath)


def save_npy(data, fpath):
    np.save(fpath, data)
