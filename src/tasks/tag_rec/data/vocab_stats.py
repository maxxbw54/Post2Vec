from pathConfig import data_dir
import os
from utils.data_util import load_pickle


def cnt_tf_vocab(comp_list, qlist):
    min_count = len(qlist) / 100000
    if min_count > 50:
        min_count = 50
    print("comp list %s, min count %s" % (comp_list, min_count))
    word_dict = dict()
    sent_num = 0
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
            print("Processed %s questions component %s." % (sent_num, comp_list))

    remove_cnt = 0
    cnt = 0
    for w in word_dict.copy().keys():
        if word_dict[w]["tf"] < min_count:
            remove_cnt += 1
        cnt += 1
    print("# total {} removed {}".format(cnt, remove_cnt))


if __name__ == '__main__':
    task = 'tagRec'
    dataset = "SO-05-Sep-2018"
    dataset_dir = data_dir + os.sep + task + os.sep + dataset
    parallel_dir = dataset_dir + os.sep + "parallel"
    ts = 50
    ts_dir = dataset_dir + os.sep + "ts%s" % ts
    ts_parallel_dir = ts_dir + os.sep + "parallel"
    ts_corpus_dir = ts_parallel_dir + os.sep + "corpus"

    sample_k = "test100000"
    sample_k_dir = ts_dir + os.sep + "data-%s" % sample_k
    print("Setting:\ntasks : %s\ndataset : %s\nts : %s\nsample_k : %s" % (task, dataset, ts, sample_k))

    train_dir = sample_k_dir + os.sep + "train"
    vocab_dir = sample_k_dir + os.sep + "vocab"

    # use training data
    qlist = list()
    for f in sorted(os.listdir(train_dir)):

        fpath = os.path.join(train_dir, f)
        qlist += load_pickle(fpath)

    print("#qlist = %s" % len(qlist))

    # title vocab
    print("title")
    cnt_tf_vocab(["title"], qlist)

    # desc_text vocab
    print("desc")
    cnt_tf_vocab(["desc_text"], qlist)

    # desc_code vocab
    print("desc code")
    cnt_tf_vocab(["desc_code"], qlist)
