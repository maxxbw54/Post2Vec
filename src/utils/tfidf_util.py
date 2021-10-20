# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       compute_tf_idf
   Description:
   Author:     bowen
   date:        12/11/18
-------------------------------------------------
"""
import os
from pathConfig import data_dir
from utils.time_util import get_current_time
import math


def build_tf_idf_vocab(comp_list, qlist):
    min_count = len(qlist) / 100000
    if min_count > 50:
        min_count = 50
    print("comp list %s, min count %s" % (comp_list, min_count))
    word_dict = dict()
    sent_num = 0
    print("Computing tf-idf...", get_current_time())
    for q in qlist:
        sent_num += 1
        cur_word_set = set()
        comp_word_list = list()
        for comp in comp_list:
            comp_word_list += q.get_comp_by_name(comp)
        for w in comp_word_list:
            if w not in cur_word_set:
                cur_word_set.add(w)
                if w not in word_dict:
                    word_dict[w] = {"tf": 1, "idf": 1}
                else:
                    word_dict[w]["tf"] += 1
                    word_dict[w]["idf"] += 1
            else:
                word_dict[w]["tf"] += 1
        if sent_num % 10000 == 0:
            print("Processed %s questions component %s." % (sent_num, comp_list), get_current_time())

    for w in word_dict.copy().keys():
        if word_dict[w]["tf"] >= min_count:
            tf = word_dict[w]["tf"]
            word_dict[w]["idf"] = math.log(sent_num / float(word_dict[w]["idf"]))
            idf = word_dict[w]["idf"]
            word_dict[w]["tfidf"] = tf * idf
        else:
            word_dict.pop(w)

    print("# %s dict = %s" % (comp_list, len(word_dict)))
    return word_dict


if __name__ == '__main__':
    task = 'tagRec'
    dataset = "SO-05-Sep-2018"
    dataset_dir = data_dir + os.sep + task + os.sep + dataset
    parallel_dir = dataset_dir + os.sep + "parallel"
    ts = 1
    print("Setting:\ntasks : %s\ndataset : %s\nts : %s\n" % (task, dataset, ts))

    ts_dir = dataset_dir + os.sep + "ts%s" % ts
    ts_parallel_dir = ts_dir + os.sep + "parallel"
    ts_corpus_dir = ts_parallel_dir + os.sep + "corpus"

    build_tf_idf_vocab(ts_corpus_dir)
