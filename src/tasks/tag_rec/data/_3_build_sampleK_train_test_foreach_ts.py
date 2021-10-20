# -*- coding: utf-8 -*-
from pathConfig import data_dir
import os
from pyToolkit.lib.utils.pkl_util import save_pickle, load_pickle
import operator
from pyToolkit.lib.utils.time_util import get_current_time
from random import shuffle, sample
import gc
import sys

"""
Merge into 1 and sort by creation date
"""


def get_all_topk_qlist(corpus_dir):
    parallel_list = ["0-1000000", "1000000-2000000", "2000000-3000000", "3000000-4000000", "4000000-5000000",
                     "5000000-6000000", "6000000-7000000", "7000000-8000000", "8000000-9000000", "9000000-10000000",
                     "10000000-11000000", "11000000-12000000", "12000000-13000000", "13000000-14000000",
                     "14000000-15000000", "15000000-16000000", "16000000-None"]
    qlist = list()
    for p in parallel_list:
        target_corpus_fpath = corpus_dir + os.sep + "_2_corpus-without-Raretag-%s.pkl" % p
        for q in load_pickle(target_corpus_fpath):
            yy = int(q.creation_date.split('-')[0])
            if yy >= 2014:
                qlist.append(q)
    print("# all qlist = %s" % len(qlist), get_current_time())
    return qlist


def save_data(qlist, save_dir, item, batch_size):
    '''
    save data into many pieces
    :param qlist:
    :param data_dir:
    :param batch_size:
    :return:
    '''
    for i in range(0, len(qlist), batch_size):
        st = i
        et = i + batch_size
        if et > len(qlist):
            et = len(qlist)
        corpus_path = os.path.join(save_dir, "%s-%s-%s.pkl" % (item, st, et))
        save_pickle(qlist[st:et], corpus_path)


if __name__ == '__main__':
    task = 'tagRec'
    dataset = "SO-05-Sep-2018"
    dataset_dir = data_dir + os.sep + task + os.sep + dataset
    parallel_dir = dataset_dir + os.sep + "parallel"
    ts = 50
    ts_dir = dataset_dir + os.sep + "ts%s" % ts
    ts_corpus_dir = ts_dir + os.sep + "corpus"
    sample_k = "test100000"
    sample_k_dir = ts_dir + os.sep + "data-%s" % sample_k
    if not os.path.exists(sample_k_dir):
        os.mkdir(sample_k_dir)
    print("Setting:\ntasks : %s\ndataset : %s\nts : %s\nsample k : %s" % (task, dataset, ts, sample_k))

    all_qlist = get_all_topk_qlist(ts_corpus_dir)
    if sample_k == "all" or sample_k == "test100000":
        qlist = all_qlist
    else:
        qlist = sample(all_qlist, sample_k)

    print("Sorting...", get_current_time())
    sorted_qlist = sorted(qlist, key=operator.attrgetter('creation_date'))

    # training:test=X:100000
    size_of_test = 100000
    train_data = sorted_qlist[:int(len(sorted_qlist) - size_of_test)]
    test_data = sorted_qlist[int(len(sorted_qlist) - size_of_test):]

    print("#train = %s, #test = %s" % (len(train_data), len(test_data)))

    print("shuffling...", get_current_time())
    shuffle(train_data)
    shuffle(test_data)

    train_dir = sample_k_dir + os.sep + "train"
    if not os.path.exists(train_dir):
        os.mkdir(train_dir)
    test_dir = sample_k_dir + os.sep + "test"
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)

    batch_size = 20000

    save_data(train_data, train_dir, "train", batch_size)
    train_data = None

    save_data(test_data, test_dir, "test", batch_size)
    test_data = None
    gc.collect()

    sys.exit()
