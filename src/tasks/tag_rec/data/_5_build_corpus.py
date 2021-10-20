# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       build_corpus
   Description:
   Author:     bowen
   date:        12/11/18
-------------------------------------------------
"""

from utils.data_util import load_pickle
import os
from pathConfig import data_dir
from pyToolkit.lib.time_util import get_current_time


def build_corpus(qlist, comp_list, corpus_fpath):
    corpus_f = open(corpus_fpath, "w")
    skip_cnt = 0

    cnt = 0
    print("processing %s" % fpath, get_current_time())
    for q in qlist:
        try:
            for comp in comp_list:
                str_tmp = ' '.join(q.get_comp_by_name(comp)).strip()
                if str_tmp.strip() == '':
                    continue
                corpus_f.write(str_tmp + '\n')
            cnt += 1
            if cnt % 50000 == 0:
                print("Processed %s questions." % cnt, get_current_time())
        except Exception as e:
            skip_cnt += 1
            print("Skip %s because %s" % (skip_cnt, e))

    corpus_f.close()
    print("corpus %s building finished." % corpus_fpath)


if __name__ == '__main__':
    task = 'tagRec'
    dataset = "SO-05-Sep-2018"
    dataset_dir = data_dir + os.sep + task + os.sep + dataset
    parallel_dir = dataset_dir + os.sep + "parallel"
    ts = 50
    print("Setting:\ntasks : %s\ndataset : %s\nts : %s\n" % (task, dataset, ts))

    ts_dir = dataset_dir + os.sep + "ts%s" % ts
    ts_parallel_dir = ts_dir + os.sep + "parallel"

    sample_K = "test100000"
    sample_K_dir = ts_dir + os.sep + "data-%s" % sample_K
    sample_K_train_dir = sample_K_dir + os.sep + "train"

    corpus_dir = os.path.join(sample_K_dir, "corpus")
    if not os.path.exists(corpus_dir):
        os.mkdir(corpus_dir)

    # use training data
    qlist = list()
    for f in os.listdir(sample_K_train_dir):
        fpath = os.path.join(sample_K_train_dir, f)
        qlist += load_pickle(fpath)
        print("# qlist = %s" % len(qlist))

    title_corpus_fpath = os.path.join(corpus_dir, "title_corpus.txt")
    if not os.path.exists(title_corpus_fpath):
        build_corpus(qlist, ["title"], title_corpus_fpath)
    else:
        print("title Corpus already exist.")

    desc_text_corpus_fpath = os.path.join(corpus_dir, "desc_text_corpus.txt")
    if not os.path.exists(desc_text_corpus_fpath):
        build_corpus(qlist, ["desc_text"], desc_text_corpus_fpath)
    else:
        print("desc_text Corpus already exist.")

    desc_code_corpus_fpath = os.path.join(corpus_dir, "desc_code_corpus.txt")
    if not os.path.exists(desc_code_corpus_fpath):
        build_corpus(qlist, ["desc_code"], desc_code_corpus_fpath)
    else:
        print("desc_code Corpus already exist.")

    title_desc_code_corpus_fpath = os.path.join(corpus_dir, "title_desc_text_corpus.txt")
    if not os.path.exists(title_desc_code_corpus_fpath):
        build_corpus(qlist, ["title", "desc_text"], title_desc_code_corpus_fpath)
    else:
        print("title_desc_text Corpus already exist.")


