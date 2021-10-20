from pathConfig import data_dir
import os
from utils.time_util import get_current_time
from utils.data_util import load_pickle, save_pickle
import gc
import sys
from utils.tfidf_util import build_tf_idf_vocab


def build_tag_vocab(qlist):
    print("Building vocab...", get_current_time())

    tag_vocab = set()

    sent_num = 0
    for q in qlist:

        # tags
        for t in q.tags:
            if t not in tag_vocab:
                tag_vocab.add(t)

        sent_num += 1
        if sent_num % 10000 == 0:
            print("Processing %s question..." % sent_num, get_current_time())

    print("Processed %s questions." % sent_num, get_current_time())
    return tag_vocab


def build_len_dict(qlist):
    print("Building vocab...", get_current_time())

    # leng_fpath
    title_len_list = list()
    desc_text_len_list = list()
    desc_code_len_list = list()

    sent_num = 0
    for q in qlist:
        title_len_list.append(len(q.title))
        desc_text_len_list.append(len(q.desc_text))
        desc_code_len_list.append(len(q.desc_code))

        sent_num += 1
        if sent_num % 10000 == 0:
            print("Processing %s question..." % sent_num, get_current_time())

    # len
    len_dict = dict()
    len_dict["max_title_len"] = max(title_len_list) if max(title_len_list) < 100 else 100
    len_dict["max_desc_text_len"] = max(desc_text_len_list) if max(desc_text_len_list) < 1000 else 1000
    len_dict["max_desc_code_len"] = max(desc_code_len_list) if max(desc_code_len_list) < 1000 else 1000

    print("Processed %s questions." % sent_num, get_current_time())
    return len_dict


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
    if not os.path.exists(vocab_dir):
        os.mkdir(vocab_dir)

    # use training data
    qlist = list()
    for f in sorted(os.listdir(train_dir)):
        fpath = os.path.join(train_dir, f)
        qlist += load_pickle(fpath)

    print("#qlist = %s" % len(qlist))

    # title vocab
    title_vocab_fpath = vocab_dir + os.sep + "title_vocab.pkl"
    title_word_vocab = build_tf_idf_vocab(["title"], qlist)
    save_pickle(title_word_vocab, title_vocab_fpath)
    title_word_vocab = None
    gc.collect()

    # desc_text vocab
    desc_text_vocab_fpath = vocab_dir + os.sep + "desc_text_vocab.pkl"
    desc_text_word_vocab = build_tf_idf_vocab(["desc_text"], qlist)
    save_pickle(desc_text_word_vocab, desc_text_vocab_fpath)
    desc_text_word_vocab = None
    gc.collect()

    # desc_code vocab
    desc_code_vocab_fpath = vocab_dir + os.sep + "desc_code_vocab.pkl"
    desc_code_word_vocab = build_tf_idf_vocab(["desc_code"], qlist)
    save_pickle(desc_code_word_vocab, desc_code_vocab_fpath)
    desc_code_word_vocab = None
    gc.collect()

    # title_desc_text vocab
    title_desc_text_vocab_fpath = vocab_dir + os.sep + "title_desc_text_vocab.pkl"
    title_desc_text_word_vocab = build_tf_idf_vocab(["title", "desc_text"], qlist)
    save_pickle(title_desc_text_word_vocab, title_desc_text_vocab_fpath)
    title_desc_text_word_vocab = None
    gc.collect()

    # tag vocab
    tag_vocab_fpath = vocab_dir + os.sep + "tag_vocab.pkl"
    tag_vocab = build_tag_vocab(qlist)
    save_pickle(tag_vocab, tag_vocab_fpath)
    tag_vocab = None
    gc.collect()

    # len dict
    len_fpath = vocab_dir + os.sep + "len.pkl"
    len_dict = build_len_dict(qlist)
    save_pickle(len_dict, len_fpath)
    len_dict = None
    gc.collect()

    sys.exit()
