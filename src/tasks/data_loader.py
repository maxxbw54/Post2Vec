# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       data_loader
   Description:
   Author:     bowen
   date:        12/30/18
-------------------------------------------------
"""
import os
from pathConfig import data_dir
from utils.data_util import load_pickle


def load_precompute_qdict_from_qidset(app_name, qidset):
    # path setting
    task = 'tagRec'
    dataset = "SO-05-Sep-2018"
    dataset_dir = os.path.join(data_dir, task, dataset)
    ts = 1
    ts_dir = os.path.join(dataset_dir, "ts%s" % ts)
    topk = "all"
    topk_dir = os.path.join(ts_dir, "data-%s" % topk)
    items = ["train", "test"]
    new_qlist = dict()
    for item in items:
        app_item_dir = os.path.join(topk_dir, "approach", app_name, item)
        for f in os.listdir(app_item_dir):
            fpath = os.path.join(app_item_dir, f)
            qlist = load_pickle(fpath)
            for q in qlist:
                if q.qid in qidset:
                    new_qlist[q.qid] = q
    if len(qidset) != len(new_qlist):
        print("Error #qidset %s != #new_qlist! %s" % (len(qidset), len(new_qlist)))
        # exit(0)
    return new_qlist
