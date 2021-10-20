# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       calculate_util
   Description:
   Author:     bowen
   date:        12/18/18
-------------------------------------------------
"""
import math
from scipy.spatial.distance import cosine


def cosine_similarity(a, b, compress=False):
    if compress == True:
        up = 0.0
        for k in a:
            if k in b:
                up += (a[k] * b[k])
        down_a = 0.0
        for v in a.values():
            down_a += (v * v)
        down_b = 0.0
        for v in b.values():
            down_b += (v * v)
        if down_a == 0.0 or down_b == 0.0:
            sim = 0.0
        else:
            sim = up / (math.sqrt(down_a) * math.sqrt(down_b))
    else:
        sim = 1 - cosine(a, b)
    return sim
