from utils.csv_util import write_dict_to_csv
from pathConfig import data_dir
import os
from utils.time_util import get_current_time
import csv

task = 'tagRec'
dataset = 'SO-05-Sep-2018'
dataset_dir = data_dir + os.sep + task + os.sep + dataset
parallel_dir = dataset_dir + os.sep + "parallel"
print("Setting:\ntasks : %s\ndataset : %s\n" % (task, dataset))

# input
# "id", "tags"
# id-tags-all.csv
id_tags_csv_fpath = dataset_dir + os.sep + "id-tags-all.csv"

# output
# _0_tag-count-all.csv
# "tag", "count"
tag_cnt_all_csv_fapth = dataset_dir + os.sep + "_0_tag-count-all.csv"
tag_cnt_dict = {}
tag_cnt_header = ["tag", "count"]

# tag cnt
row_num = 0
with open(id_tags_csv_fpath, 'r') as id_tags_file:
    rd = csv.reader(id_tags_file, escapechar='\\')
    for row in rd:
        tags = row[1].replace('<', ' ').replace('>', ' ').strip().split()
        row_num += 1
        for t in tags:
            if t in tag_cnt_dict:
                tag_cnt_dict[t] += 1
            else:
                tag_cnt_dict[t] = 1
        if row_num % 10000 == 0:
            print("Processing line %s" % row_num, get_current_time())

write_dict_to_csv(tag_cnt_dict, tag_cnt_all_csv_fapth, tag_cnt_header)
print("# Tags = %s" % len(tag_cnt_dict))
