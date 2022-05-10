from pathConfig import data_dir
import os
from utils.data_util import load_pickle

task = 'tagRec'
dataset = 'CodeReview'
dataset_dir = data_dir + os.sep + task + os.sep + dataset
ts = 50
ts_dir = dataset_dir + os.sep + "ts%s" % ts
train_test_dir = ts_dir + os.sep + 'data'
print("Setting:\ntasks : %s\ndataset : %s\nts : %s\n" % (task, dataset, ts))

train_data_fpath = train_test_dir + os.sep + "train.pkl"
test_data_fpath = train_test_dir + os.sep + "test.pkl"

train = load_pickle(train_data_fpath)
test = load_pickle(test_data_fpath)

print("#train = %s\t#test = %s" % (len(train), len(test)))

# check duplicate id?
# ids_in_train = [x.qid for x in train]
# ids_in_test = [x.qid for x in test]
# print(set(ids_in_train).intersection(set(ids_in_test)))


# check question
cnt = 0
for x in train:
    print("id %s" % x.qid)
    print("#title %s" % len(x.title))
    print("#desc_text %s" % len(x.desc_text))
    print("#desc_code %s" % len(x.desc_code))
    cnt += 1
    if cnt > 2:
        break
