# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     _2_remove_rare_tags_from_each_batch.py
   Input:           SO-all-clean-with-Raretag.csv
   Output:
   Description:     Exclude quetions with all rare tags.
   Author :       xubowen
   date：          2018/10/31 10:51 AM
-------------------------------------------------
"""
from pathConfig import data_dir
import os
from utils.time_util import get_current_time
import ast
from data_preparation.tag_rec._1_identify_rare_tags_foreach_ts import load_tags
from utils.data_util import save_pickle
from data_structure.question import Question


def build_corpus(all_fpath, rare_tags, corpus_fpath):
    import pandas as pd
    print("Building raw corpus and doing some pre processing...")
    cnt = 0
    filter_cnt = 0
    df = pd.read_csv(all_fpath)
    q_list = list()
    for idx, row in df.iterrows():
        try:
            qid = row['id']
            title = ast.literal_eval(row['title'])
            desc_text = ast.literal_eval(row['desc_text'])
            desc_code = ast.literal_eval(row['desc_code'])
            creation_date = row['creation_date']
            tags = ast.literal_eval(row['tags'])
            # remove rare tags
            clean_tags = list(set(tags) - set(rare_tags))

            if len(clean_tags) == 0:
                filter_cnt += 1
                continue
            try:
                q_list.append(Question(qid, title, desc_text, desc_code, creation_date, clean_tags))
                cnt += 1
            except Exception as e:
                print("Skip id=%s" % qid)
                print("Error msg: %s" % e)

            if cnt % 10000 == 0:
                print("Writing %d instances, filter %d instances..." % (cnt, filter_cnt), get_current_time())
        except Exception as e:
            print("Skip qid %s because %s" % (qid, e))
            filter_cnt += 1

    save_pickle(q_list, corpus_fpath)
    print("Write %s lines successfully." % cnt)
    print("Corpus building sucessfully! %s" % corpus_fpath, get_current_time() + '\n')


if __name__ == '__main__':
    task = 'tagRec'
    dataset = "SO-05-Sep-2018"
    dataset_dir = data_dir + os.sep + task + os.sep + dataset
    parallel_dir = dataset_dir + os.sep + "parallel"
    st_row_num = 16000000
    et_row_num = None
    # ts
    ts = 50
    ts_dir = dataset_dir + os.sep + "ts%s" % ts
    ts_corpus_dir = ts_dir + os.sep + "corpus"
    if not os.path.exists(ts_corpus_dir):
        os.mkdir(ts_corpus_dir)
    print("start line num = %s, end line num = %s" % (st_row_num, et_row_num))

    # Input:
    target_corpus_fpath = parallel_dir + os.sep + "_0_all-clean-with-Raretag-%s-%s.csv" % (st_row_num, et_row_num)
    rare_tags_fpath = ts_dir + os.sep + "_1_rareTags.csv"

    # Output:
    corpus_fpath = ts_corpus_dir + os.sep + "_2_corpus-without-Raretag-%s-%s.pkl" % (
        st_row_num, et_row_num)

    rare_tags = load_tags(rare_tags_fpath)
    build_corpus(target_corpus_fpath, rare_tags, corpus_fpath)

    print('Done.', get_current_time())
