# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       check_distribution
   Description:
   Author:     bowen
   date:        2/25/19
-------------------------------------------------
"""

from pathConfig import data_dir
import os
from utils.data_util import load_pickle
import sys
from utils.file_util import write_str_to_file


def compute_distribution(corpus_dir):
    parallel_list = ["0-1000000", "1000000-2000000", "2000000-3000000", "3000000-4000000", "4000000-5000000",
                     "5000000-6000000", "6000000-7000000", "7000000-8000000", "8000000-9000000", "9000000-10000000",
                     "10000000-11000000", "11000000-12000000", "12000000-13000000", "13000000-14000000",
                     "14000000-15000000", "15000000-16000000", "16000000-None"]
    time_dis = {}
    for p in parallel_list:
        target_corpus_fpath = corpus_dir + os.sep + "_2_corpus-without-Raretag-%s.pkl" % p
        for q in load_pickle(target_corpus_fpath):
            creation_date = q.creation_date
            yy = creation_date.split('-')[0]
            mm = creation_date.split('-')[1]
            ym = "%s-%s" % (yy, mm)
            if ym in time_dis:
                time_dis[ym] += 1
            else:
                time_dis[ym] = 1
    return time_dis


if __name__ == '__main__':
    task = 'tagRec'
    dataset = "SO-05-Sep-2018"
    dataset_dir = data_dir + os.sep + task + os.sep + dataset
    parallel_dir = dataset_dir + os.sep + "parallel"
    ts = 50
    ts_dir = dataset_dir + os.sep + "ts%s" % ts
    ts_corpus_dir = ts_dir + os.sep + "corpus"

    time_dis = compute_distribution(ts_corpus_dir)

    str_tmp = ""
    for k in sorted(time_dis):
        print("%s: %s" % (k, time_dis[k]))
        str_tmp += ("%s,%s\n" % (k, time_dis[k]))

    write_str_to_file(str_tmp, "time_distribution.csv")
    sys.exit()
