import os
from pathConfig import data_dir
from pyToolkit.lib.utils.pkl_util import load_pickle, save_pickle
from pyToolkit.lib.utils.time_util import get_current_time
from utils.padding_and_indexing_util import padding_and_indexing_qlist
from utils.vocab_util import vocab_to_index_dict

################################# data settings #################################
task = 'tagRec'
dataset = "SO-05-Sep-2018"
dataset_dir = data_dir + os.sep + task + os.sep + dataset
# ts dir
ts = 50
ts_dir = dataset_dir + os.sep + "ts%s" % ts
# sample_K dir
sample_K = "test100000"
sample_K_dir = ts_dir + os.sep + "data-%s" % sample_K
vocab_dir = os.path.join(sample_K_dir, "vocab1")

# input files
# len_dict_fpath = os.path.join(vocab_dir, "len.pkl")
title_vocab_fpath = os.path.join(vocab_dir, "title_vocab.pkl")
desc_text_vocab_fpath = os.path.join(vocab_dir, "desc_text_vocab.pkl")
desc_code_vocab_fpath = os.path.join(vocab_dir, "desc_code_vocab.pkl")
tag_vocab_fpath = os.path.join(vocab_dir, "tag_vocab.pkl")

# basic path
train_dirname = "train"
train_dir = sample_K_dir + os.sep + train_dirname
processed_train_dir = sample_K_dir + os.sep + "processed_" + train_dirname
os.makedirs(processed_train_dir)
print("Setting:\ntasks : %s\ndataset : %s\nts : %s\n" % (task, dataset, ts))
#################################################################################
# initial
# len
# len_dict = load_pickle(len_dict_fpath)
len_dict = dict()
len_dict["max_title_len"] = 100
len_dict["max_desc_text_len"] = 1000
len_dict["max_desc_code_len"] = 1000

# title vocab1
title_vocab = load_pickle(title_vocab_fpath)
title_vocab = vocab_to_index_dict(vocab=title_vocab, ifpad=True)

# desc_text vocab1
desc_text_vocab = load_pickle(desc_text_vocab_fpath)
desc_text_vocab = vocab_to_index_dict(vocab=desc_text_vocab, ifpad=True)

# desc_code_vocab
desc_code_vocab = load_pickle(desc_code_vocab_fpath)
desc_code_vocab = vocab_to_index_dict(vocab=desc_code_vocab, ifpad=True)

# tag vocab1
tag_vocab = load_pickle(tag_vocab_fpath)
tag_vocab = vocab_to_index_dict(vocab=tag_vocab, ifpad=False)

# multiple train file
train_cnt = 0
for f in sorted(os.listdir(train_dir)):
    print("\n\n# train file = %s" % train_cnt, get_current_time())
    train_data_fpath = os.path.join(train_dir, f)
    processed_train_data_fpath = os.path.join(processed_train_dir, f)
    train_data = load_pickle(train_data_fpath)
    print("padding and indexing train", get_current_time())
    processed_train_data = padding_and_indexing_qlist(train_data, len_dict, title_vocab, desc_text_vocab,
                                                      desc_code_vocab, tag_vocab)
    save_pickle(processed_train_data, processed_train_data_fpath)
    train_cnt += 1
