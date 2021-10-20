# -*- coding: utf-8 -*-

import os

from pathConfig import data_dir
from pyToolkit.lib.utils.pkl_util import load_pickle
from pyToolkit.lib.utils.time_util import get_current_time
from tasks.tag_rec.approaches.post2vec.post2vec_util import load_model, load_args
from utils.vocab_util import vocab_to_index_dict


def get_post_vec(raw_qlist):
    from utils.padding_and_indexing_util import padding_and_indexing_qlist_without_tag
    import copy

    model, len_dict, title_vocab, desc_text_vocab, desc_code_vocab = load_p2v_model_and_vocab()

    # get corresponding vector
    print("Get corresponding vector...", get_current_time())
    raw_qlist = copy.deepcopy(raw_qlist)

    # processed qlist
    qlist = padding_and_indexing_qlist_without_tag(raw_qlist, len_dict, title_vocab, desc_text_vocab, desc_code_vocab)
    qvec = model.get_output_vector(qlist=qlist)

    print("qvec size %s" % len(qvec))

    q_dict = dict()
    for q in qvec:
        q_dict[q.qid] = q

    return q_dict


def load_p2v_model_and_vocab():
    # path setting
    task = 'tagRec'
    dataset = "SO-05-Sep-2018"
    dataset_dir = os.path.join(data_dir, task, dataset)
    ts = 50
    ts_dir = os.path.join(dataset_dir, "ts%s" % ts)
    sample_K = "test100000"
    sample_K_dir = os.path.join(ts_dir, "data-%s" % sample_K)
    vocab_dir = os.path.join(sample_K_dir, "vocab")

    # approach setting
    app_name = "post2vec"
    # load param
    app_dir = os.path.join(sample_K_dir, "approach", app_name)
    snapshot_dirname = "separate_all_cnn#2020-10-17_16-29-38"
    app_type = "cnn" if "cnn" in snapshot_dirname else "lstm"
    snapshot_dir = os.path.join(app_dir, "snapshot-train", app_type, snapshot_dirname)
    param_name = "snapshot_steps_%s.pt" % "1291000"
    ############################## setting end #########################################

    # load vocab
    # initial
    len_dict_fpath = os.path.join(vocab_dir, "len.pkl")
    title_vocab_fpath = os.path.join(vocab_dir, "title_vocab.pkl")
    desc_text_vocab_fpath = os.path.join(vocab_dir, "desc_text_vocab.pkl")
    desc_code_vocab_fpath = os.path.join(vocab_dir, "desc_code_vocab.pkl")

    # len
    len_dict = load_pickle(len_dict_fpath)

    # title vocab
    title_vocab = load_pickle(title_vocab_fpath)
    title_vocab = vocab_to_index_dict(vocab=title_vocab, ifpad=True)

    # desc_text vocab
    desc_text_vocab = load_pickle(desc_text_vocab_fpath)
    desc_text_vocab = vocab_to_index_dict(vocab=desc_text_vocab, ifpad=True)

    # desc_code_vocab
    desc_code_vocab = load_pickle(desc_code_vocab_fpath)
    desc_code_vocab = vocab_to_index_dict(vocab=desc_code_vocab, ifpad=True)

    print("Processing %s" % param_name)
    best_param_fpath = os.path.join(snapshot_dir, param_name)

    # load approach
    print("Load args and model...", get_current_time())
    args = load_args(snapshot_dir)
    model = load_model(args, best_param_fpath)

    return model, len_dict, title_vocab, desc_text_vocab, desc_code_vocab

