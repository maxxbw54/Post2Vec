# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       _6_build_subset_test_data
   Description:
   Author:     bowen
   date:        2/11/19
-------------------------------------------------
"""

import os
from pathConfig import data_dir
from pyToolkit.lib.utils.pkl_util import load_pickle, save_pickle
import random

################################# data settings #################################
task = 'tagRec'
dataset = "SO-05-Sep-2018"
dataset_dir = data_dir + os.sep + task + os.sep + dataset
# ts dir
ts = 50
ts_dir = dataset_dir + os.sep + "ts%s" % ts
# simple_K dir
simple_K = "test100000"
simple_K_dir = ts_dir + os.sep + "data-%s" % simple_K

# basic path
print("Setting:\ntasks : %s\ndataset : %s\nts : %s\n" % (task, dataset, ts))
#################################################################################

# predict
test_dir = os.path.join(simple_K_dir, "test")
# get sample test data
sample_size = 20000
sample_cnt = 10
all_test_data = list()
sample_test_data_dir = os.path.join(simple_K_dir, "sample_test")

if not os.path.exists(sample_test_data_dir):
    os.mkdir(sample_test_data_dir)
elif len(os.listdir(sample_test_data_dir)) > 0:
    print("sample test data is not empty!")
    exit()

for f in sorted(os.listdir(test_dir)):
    test_data_fpath = os.path.join(test_dir, f)
    test_data = load_pickle(test_data_fpath)
    all_test_data += test_data

for i in range(sample_cnt):
    sample_test_data = random.sample(all_test_data, sample_size)

    sample_test_data_fpath = os.path.join(sample_test_data_dir, "%s_sampled_test_data_%s.pkl" % (i, sample_size))
    save_pickle(sample_test_data, sample_test_data_fpath)
    print("#sample test = %s" % len(sample_test_data))
