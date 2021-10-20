import os
import random

from pathConfig import data_dir
from pyToolkit.lib.utils.pkl_util import load_pickle, save_pickle
from pyToolkit.lib.utils.time_util import get_current_time

task = 'tagRec'
dataset = "SO-05-Sep-2018"
dataset_dir = data_dir + os.sep + task + os.sep + dataset
# ts dir
ts = 50
ts_dir = dataset_dir + os.sep + "ts%s" % ts
# sample_K dir
sample_K = "test100000"
sample_K_dir = ts_dir + os.sep + "data-%s" % sample_K

train_dir = sample_K_dir + os.sep + "train"
sample_train_dir = sample_K_dir + os.sep + "10_percent_train-new"
if os.path.exists(sample_train_dir):
    print("Pls remove {}".format(sample_train_dir))
    exit()
os.makedirs(sample_train_dir)

train_cnt = 0
train_data = []
for f in sorted(os.listdir(train_dir)):
    print("# train file = {}\t{}".format(train_cnt, get_current_time()))

    train_data_fpath = os.path.join(train_dir, f)
    train_data = train_data + load_pickle(train_data_fpath)

    train_cnt += 1

subset_train_data = random.Random(1024).sample(train_data, int(len(train_data) * 0.1))
random.Random(1024).shuffle(subset_train_data)
print("subset train data {}".format(len(subset_train_data)))

batch_size = 20000
for i in range(0, len(subset_train_data), batch_size):
    st_idx = i
    et_idx = i + batch_size if i + batch_size < len(subset_train_data) else len(subset_train_data)
    fpath = os.path.join(sample_train_dir, "sample_train_{}_{}.pkl".format(st_idx, et_idx))
    save_pickle(subset_train_data[i:i + batch_size], fpath)
