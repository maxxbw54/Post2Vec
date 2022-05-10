# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       stats
   Description:
   Author:     bowen
   date:        4/2/19
-------------------------------------------------
"""
from utils.data_util import load_pickle
import os
from utils.time_util import get_current_time
from pathConfig import data_dir


def num_of_post_in_corpus():
    sum = 0
    corpus_dir = '/data/bowen/Post2Vec/data/tagRec/SO-05-Sep-2018/ts50/data-test100000/train'
    for f in os.listdir(corpus_dir):
        if f.endswith('pkl'):
            print(f, get_current_time())
            target_corpus_fpath = os.path.join(corpus_dir, f)
            qlist = load_pickle(target_corpus_fpath)
            sum += len(qlist)
            print("len qlist %s" % len(qlist), get_current_time())
            print("num %s" % sum, get_current_time())
    print("# all qlist = %s" % sum, get_current_time())


def proportion_code():
    sum = 0
    code_sum = 0
    corpus_dir = '/data/bowen/Post2Vec/data/tagRec/SO-05-Sep-2018/ts50/corpus'
    for f in os.listdir(corpus_dir):
        if f.endswith('pkl'):
            print(f, get_current_time())
            target_corpus_fpath = os.path.join(corpus_dir, f)
            qlist = load_pickle(target_corpus_fpath)
            for q in qlist:
                if len(q.desc_code) != 0:
                    code_sum += 1
                sum += 1
            print("code num %s" % code_sum, get_current_time())
            print("num %s" % sum, get_current_time())
    print("code num %s" % code_sum, get_current_time())
    print("num %s" % sum, get_current_time())


def proportion_posts_with_out_tag():
    with_code_cnt = 0
    without_code_cnt = 0
    sum = 0

    task = 'tagRec'
    dataset = "SO-05-Sep-2018"
    dataset_dir = data_dir + os.sep + task + os.sep + dataset
    parallel_dir = dataset_dir + os.sep + "parallel"

    import pandas as pd
    import ast

    for f in os.listdir(parallel_dir):
        if f.endswith(".csv"):
            df = pd.read_csv(os.path.join(parallel_dir, f))
            for idx, row in df.iterrows():
                tags = ast.literal_eval(row['tags'])
                if len(set(tags)) == 0:
                    without_code_cnt += 1
                else:
                    with_code_cnt += 1

            print("with code {} without code {}".format(with_code_cnt, without_code_cnt), get_current_time())

    print("with code {} without code {}".format(with_code_cnt, without_code_cnt), get_current_time())


if __name__ == '__main__':
    proportion_posts_with_out_tag()
# num_of_post_in_corpus()
# proportion_code()
