import os

from pathConfig import data_dir
from pyToolkit.lib.utils.file_util import read_file_into_line_list
from pyToolkit.lib.utils.pkl_util import load_pickle
from pyToolkit.lib.utils.time_util import get_current_time
from tasks.tag_rec.approaches.post2vec.post2vec_util import load_args, load_model
from utils.csv_util import write_row_to_csv, append_new_row
from utils.data_util import random_mini_batch
from utils.padding_and_indexing_util import padding_and_indexing_qlist
from utils.vocab_util import vocab_to_index_dict


# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

def get_computed_param(snapshot_fpath):
    str_list = read_file_into_line_list(snapshot_fpath, if_strip=True)
    param_list = list()
    for param in str_list[1:]:
        param_list.append(param.split(',')[0])
    return param_list


task = 'tagRec'
dataset = "SO-05-Sep-2018"
dataset_dir = data_dir + os.sep + task + os.sep + dataset
# ts dir
ts = 50
ts_dir = dataset_dir + os.sep + "ts%s" % ts
# sample_K dir
sample_K = "test100000"
sample_K_dir = ts_dir + os.sep + "data-%s" % sample_K
vocab_dir = os.path.join(sample_K_dir, "vocab")
app_dir = os.path.join(sample_K_dir, "approach", "post2vec")
snapshot_dir = os.path.join(app_dir, "snapshot-train")

# basic path
print("Setting:\ntasks : %s\ndataset : %s\nts : %s\n" % (task, dataset, ts))
#################################################################################

# load vocab
# initial
len_dict_fpath = os.path.join(vocab_dir, "len.pkl")
title_vocab_fpath = os.path.join(vocab_dir, "title_vocab.pkl")
desc_text_vocab_fpath = os.path.join(vocab_dir, "desc_text_vocab.pkl")
desc_code_vocab_fpath = os.path.join(vocab_dir, "desc_code_vocab.pkl")
tag_vocab_fpath = os.path.join(vocab_dir, "tag_vocab.pkl")

# title vocab
title_vocab = load_pickle(title_vocab_fpath)
title_vocab = vocab_to_index_dict(vocab=title_vocab, ifpad=True)

# desc_text vocab
desc_text_vocab = load_pickle(desc_text_vocab_fpath)
desc_text_vocab = vocab_to_index_dict(vocab=desc_text_vocab, ifpad=True)

# desc_code_vocab
desc_code_vocab = load_pickle(desc_code_vocab_fpath)
desc_code_vocab = vocab_to_index_dict(vocab=desc_code_vocab, ifpad=True)

# tag vocab
tag_vocab = load_pickle(tag_vocab_fpath)
tag_vocab = vocab_to_index_dict(vocab=tag_vocab, ifpad=False)

# load args from json file
# snapshot_dir_name = "separate_title_desctext_cnn#2020-10-19_07-23-04"
snapshot_dir_name = "separate_all_cnn#2020-10-17_16-29-38"
# snapshot_dir_name = "separate_title_desctext_bilstm#2020-10-19_07-25-42"
# snapshot_dir_name = "separate_all_bilstm#2020-10-17_16-28-12"
param_name = 'snapshot_steps_1291000.pt'

if "cnn" in snapshot_dir_name:
    param_dir = os.path.join(snapshot_dir, "cnn", snapshot_dir_name)
elif "lstm" in snapshot_dir_name:
    param_dir = os.path.join(snapshot_dir, "lstm", snapshot_dir_name)
args = load_args(param_dir)
param_fpath = os.path.join(param_dir, param_name)

# len
# len_dict = load_pickle(len_dict_fpath)
len_dict = dict()
len_dict["max_title_len"] = args.max_title_len
len_dict["max_desc_text_len"] = args.max_title_len
len_dict["max_desc_code_len"] = args.max_title_len

# EVAL_METRIC = 'ori'
# EVAL_METRIC = 'standard'
topk_list = [1, 2, 3, 4, 5]
# header = ['test_file', 'P1', 'P2', 'P3', 'P4', 'P5', 'R1', 'R2', 'R3', 'R4', 'R5', 'F1', 'F2', 'F3', 'F4', 'F5']

# EVAL_METRIC = 'topn'
# header = ['test_file', 'top1', 'top2', 'top3', 'top4', 'top5']

# EVAL_METRIC = 'map'
# header = ['test_file', 'map']

EVAL_METRIC = 'mrr'
header = ['test_file', 'mrr']

# EVAL_METRIC = 'auc'
# header = ['test_file', 'auc']

res_fpath = os.path.join(snapshot_dir, "{}-{}-{}-res.csv".format(snapshot_dir_name, param_name, EVAL_METRIC))
write_row_to_csv(header, res_fpath)

model = load_model(args, param_fpath)

# cnn
if args.model_selection == "separate_all_cnn":
    from tasks.tag_rec.approaches.post2vec.separate.cnn.models.model_all_separate_cnn import test_eval
elif args.model_selection == "separate_title_desctext_cnn":
    from tasks.tag_rec.approaches.post2vec.separate.cnn.models.model_title_desctext_separate_cnn import test_eval
# lstm
elif args.model_selection == "separate_all_bilstm":
    from tasks.tag_rec.approaches.post2vec.separate.lstm.models.model_all_separate_bilstm import test_eval
elif args.model_selection == "separate_title_desctext_bilstm":
    from tasks.tag_rec.approaches.post2vec.separate.lstm.models.model_title_desctext_separate_bilstm import test_eval
else:
    print("No such model!")
    exit(0)
print("Loading test data...")

# predict
test_data_dir = os.path.join(sample_K_dir, "test")
for f in os.listdir(test_data_dir):
    test_data_fpath = os.path.join(test_data_dir, f)
    test_data = load_pickle(test_data_fpath)
    print("#test data = %s loaded!" % len(test_data), get_current_time())

    processed_test_data = padding_and_indexing_qlist(test_data, len_dict, title_vocab, desc_text_vocab,
                                                     desc_code_vocab, tag_vocab)

    print("random mini batch", get_current_time())
    batches_test = random_mini_batch(processed_test_data, args.batch_size)

    res = test_eval(batches_test, model, args, topk_list, EVAL_METRIC)

    if EVAL_METRIC == 'ori' or EVAL_METRIC == 'standard':
        pre, rc, f1 = res[0], res[1], res[2]
        append_new_row([f] + pre + rc + f1, res_fpath)
        print("Precision\t\t%s" % ("\t".join(str(x) for x in pre)))
        print("Recall\t\t%s" % ("\t".join(str(x) for x in rc)))
        print("F1\t\t%s\n" % ("\t".join(str(x) for x in f1)))
    elif EVAL_METRIC == 'topn':
        topn = res[0]
        append_new_row([f] + topn, res_fpath)
        print("topn\t\t%s" % ("\t".join(str(x) for x in topn)))
    elif EVAL_METRIC == 'map':
        map = res[0]
        append_new_row([f, map], res_fpath)
        print("map:{}".format(map))
    elif EVAL_METRIC == 'mrr':
        mrr = res[0]
        append_new_row([f, mrr], res_fpath)
        print("mrr:{}".format(mrr))
    elif EVAL_METRIC == 'auc':
        auc = res[0]
        append_new_row([f, auc], res_fpath)
        print("auc:{}".format(auc))
