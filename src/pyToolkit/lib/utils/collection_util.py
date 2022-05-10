# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       collection_util
   Description:
   Author:     bowen
   date:        7/25/19
-------------------------------------------------
"""

import operator


def get_topk_from_dict(dict_tmp, topk):
    new_dict = dict()
    topk_list = sorted(dict_tmp.items(), key=operator.itemgetter(1), reverse=True)[:topk]
    for (k, v) in topk_list:
        new_dict[k] = v
    return new_dict
