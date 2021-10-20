import argparse
import datetime
import os

import torch

from pathConfig import data_dir
from pyToolkit.lib.utils.file_util import write_str2file
from pyToolkit.lib.utils.pkl_util import load_pickle
from pyToolkit.lib.utils.time_util import get_current_time, Timer
from tasks.tag_rec.approaches.post2vec.post2vec_util import save_args
from utils.data_util import random_mini_batch
from utils.vocab_util import vocab_to_index_dict
from utils.padding_and_indexing_util import padding_and_indexing_qlist

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"

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
vocab_dir = os.path.join(sample_K_dir, "vocab")

# input files
# len_dict_fpath = os.path.join(vocab_dir, "len.pkl")
title_vocab_fpath = os.path.join(vocab_dir, "title_vocab.pkl")
desc_text_vocab_fpath = os.path.join(vocab_dir, "desc_text_vocab.pkl")
desc_code_vocab_fpath = os.path.join(vocab_dir, "desc_code_vocab.pkl")
tag_vocab_fpath = os.path.join(vocab_dir, "tag_vocab.pkl")

# basic path
train_dir = sample_K_dir + os.sep + "train"
test_dir = sample_K_dir + os.sep + "test"
print("Setting:\ntasks : %s\ndataset : %s\nts : %s\n" % (task, dataset, ts))
#################################################################################


############################ model arguments settings ############################
parser = argparse.ArgumentParser(description='Multi-label Classifier based on Multi-component')
# basic settings
parser.add_argument('-batch-size', type=int, default=128, help='batch size for training [default: 128]')
parser.add_argument('-epochs', type=int, default=16, help='number of epochs for train [default: 24]')
parser.add_argument('-log-interval', type=int, default=10,
                    help='how many steps to wait before logging [default: 10]')
parser.add_argument('-dev-ratio', type=float, default=0.0, help='ratio of development set')
parser.add_argument('-dev-interval', type=int, default=500,
                    help='how many steps to wait before testing [default: 1000]')
parser.add_argument('-dev-metric', type=str, default='ori', help='evaluation metric for development set')
parser.add_argument('-dev-metric-topk', type=list, default=[1, 2, 3, 4, 5], help='topk for development set')
parser.add_argument('-test-interval', type=int, default=1000,
                    help='how many steps to wait before testing [default: 1000]')
parser.add_argument('-early-stop', type=int, default=1000,
                    help='iteration numbers to stop without performance increasing')
parser.add_argument('-save-interval', type=int, default=1000,
                    help='how many steps to wait before saving [default:1000]')
parser.add_argument('-save-dir', type=str, default='snapshot', help='where to save the snapshot')
parser.add_argument('-save-best', type=bool, default=True, help='whether to save when get best performance')
# data
parser.add_argument('-shuffle', action='store_true', default=False, help='shuffle the data every epoch')
# model
parser.add_argument('-static', action='store_true', default=False, help='fix the embedding')
# device
parser.add_argument('-device', type=int, default=-1,
                    help='device to use for iterate data, -1 mean cpu [default: -1]')
parser.add_argument('-no-cuda', action='store_true', default=False, help='disable the gpu')
# option
parser.add_argument('-snapshot', type=str, default=None, help='filename of model snapshot [default: None]')

############################# default parameter #############################
parser.add_argument('-title-kernel-num', type=int, default=100, help='number of each kind of kernel')  # 100
parser.add_argument('-desc-text-kernel-num', type=int, default=100, help='number of each kind of kernel')  # 100
parser.add_argument('-desc-code-kernel-num', type=int, default=100, help='number of each kind of kernel')  # 100
parser.add_argument('-title-kernel-sizes', type=list, default=[1, 2, 3],
                    help='comma-separated kernel size to use for convolution')
parser.add_argument('-desc-text-kernel-sizes', type=list, default=[1, 2, 3],  # 1,2,3 or 2,3,4 or 3,4,5
                    help='comma-separated kernel size to use for convolution')
parser.add_argument('-desc-code-kernel-sizes', type=list, default=[2, 3, 4],  # 1,2,3 or 2,3,4 or 3,4,5
                    help='comma-separated kernel size to use for convolution')
############################################################################

############################# tuned parameter #############################
parser.add_argument('-model-selection', type=str, default='separate_all_cnn',
                    help='model selection [default: separate_all_cnn]')  # separate_title_desctext_cnn
parser.add_argument('-lr', type=float, default=0.0001, help='initial learning rate [default: 0.001]')
parser.add_argument('-dropout', type=float, default=0.5, help='the probability for dropout [default: 0.5]')
parser.add_argument('-embed-dim', type=int, default=128,
                    help='number of embedding dimension [default: 128]')
parser.add_argument('-hidden-dim', type=int, default=512,
                    help='number of hidden dimension of fully connected layer [default: 512]')
############################################################################


args = parser.parse_args()

# initial
# len
# len_dict = load_pickle(len_dict_fpath)
len_dict = dict()
len_dict["max_title_len"] = 100
len_dict["max_desc_text_len"] = 1000
len_dict["max_desc_code_len"] = 1000
args.max_title_len = len_dict["max_title_len"]
args.max_desc_text_len = len_dict["max_desc_text_len"]
args.max_desc_code_len = len_dict["max_desc_code_len"]
# title vocab
title_vocab = load_pickle(title_vocab_fpath)
title_vocab = vocab_to_index_dict(vocab=title_vocab, ifpad=True)
args.title_embed_num = len(title_vocab)

# desc_text vocab
desc_text_vocab = load_pickle(desc_text_vocab_fpath)
desc_text_vocab = vocab_to_index_dict(vocab=desc_text_vocab, ifpad=True)
args.desc_text_embed_num = len(desc_text_vocab)

# desc_code_vocab
desc_code_vocab = load_pickle(desc_code_vocab_fpath)
desc_code_vocab = vocab_to_index_dict(vocab=desc_code_vocab, ifpad=True)
args.desc_code_embed_num = len(desc_code_vocab)

# tag vocab
tag_vocab = load_pickle(tag_vocab_fpath)
tag_vocab = vocab_to_index_dict(vocab=tag_vocab, ifpad=False)
args.class_num = len(tag_vocab)

# Device configuration
args.cuda = (not args.no_cuda) and torch.cuda.is_available()
del args.no_cuda

snap_shot_dir = os.path.join(sample_K_dir, "approach", "post2vec", "snapshot-train", "cnn")
if not os.path.exists(snap_shot_dir):
    os.makedirs(snap_shot_dir)
args.save_dir = os.path.join(snap_shot_dir,
                             args.model_selection + "#" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

# model selection
if args.model_selection == 'separate_all_cnn':
    from tasks.tag_rec.approaches.post2vec.separate.cnn.models.model_all_separate_cnn import MultiComp, train

    model = MultiComp(args=args)
elif args.model_selection == 'separate_title_desctext_cnn':
    from tasks.tag_rec.approaches.post2vec.separate.cnn.models.model_title_desctext_separate_cnn import MultiComp, train

    model = MultiComp(args=args)

else:
    print("No such model!")
    exit()

print("Training {} model...".format(args.model_selection), get_current_time())

if args.snapshot is not None:
    print('\nLoading parameter from {}...'.format(args.snapshot))
    model.load_state_dict(torch.load(args.snapshot))

if args.cuda:
    torch.cuda.set_device(args.device)
    model = model.cuda()

args.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

save_args(args)
#################################################################################

timer = Timer()
timer.set_start_time()

try:
    global_train_step = 0
    train_cnt = 0
    best_acc = 0
    # multiple train file
    for f in sorted(os.listdir(train_dir)):
        print("\nTraining {} model...".format(args.model_selection), get_current_time())
        print("\n\n# train file = %s" % train_cnt, get_current_time())
        train_cnt += 1
        train_data_fpath = os.path.join(train_dir, f)
        train_data = load_pickle(train_data_fpath)
        print("random mini batch train", get_current_time())
        processed_train_data = padding_and_indexing_qlist(train_data, len_dict, title_vocab, desc_text_vocab,
                                                          desc_code_vocab, tag_vocab)
        # split to train and dev data
        processed_train_set = train_data[:int(len(processed_train_data) * (1 - args.dev_ratio))]
        processed_dev_set = train_data[int(len(processed_train_data) * (1 - args.dev_ratio)):]
        batches_train = random_mini_batch(processed_train_set, args.batch_size)
        batches_dev = random_mini_batch(processed_dev_set, args.batch_size)
        print("Start train %s..." % f, get_current_time())
        model, global_train_step, best_acc = train(train_iter=batches_train, dev_iter=batches_dev, model=model,
                                                   args=args,
                                                   global_train_step=global_train_step, best_acc=best_acc)

except KeyboardInterrupt:
    print('\n' + '-' * 89)
    print('Exiting from training early')

print("\n", args)

# time cost record
timer.set_end_time()
print("\nTime cost {} seconds.".format(timer.get_time_diff_in_seconds()))
time_cost_fpath = os.path.join(args.save_dir, 'time_record.txt')
time_cost_str = "start time {}\nend time {}\ntime cost{} seconds.".format(timer.start_time, timer.end_time,
                                                                          timer.get_time_diff_in_seconds())
write_str2file(time_cost_str, time_cost_fpath)
