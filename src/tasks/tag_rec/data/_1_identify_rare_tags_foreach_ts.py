# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       _1_identify_rare_tags_foreach_ts
   Description:
   Author:     bowen
   date:        12/6/18
-------------------------------------------------
"""
from utils.csv_util import write_list_to_csv
from utils.time_util import get_current_time
import os
from pathConfig import data_dir
import csv


def load_tags(tags_fpath):
    tags = []
    import pandas as pd
    df = pd.read_csv(tags_fpath)
    for idx, row in df.iterrows():
        tags.append(row['tag'])
    print("# tags = %s" % len(tags))
    return tags


def identify_rare_tags(tag_dict, rare_tags_fpath, commom_tags_fpath, ts):
    """
    a tag to be rare if its number of appearances is less than or equal to a predefined threshold ts.
    :param tag_dict:
    :param ts:
    :return:
    """
    rare_tags = []
    common_tags = []
    for t in tag_dict:
        if tag_dict[t] <= ts:
            rare_tags.append(t)
        else:
            common_tags.append(t)
    header = ["tag"]
    write_list_to_csv(rare_tags, rare_tags_fpath, header)
    write_list_to_csv(common_tags, commom_tags_fpath, header)
    print("#rare tags : %s" % len(rare_tags), get_current_time() + '\n')


def load_tag_cnt(tag_cnt_dict_fpath):
    print("loading tag cnt dict...", get_current_time())
    tag_cnt_dict = {}
    with open(tag_cnt_dict_fpath) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        for row in reader:
            tag = row[0]
            cnt = row[1]
            tag_cnt_dict[tag] = int(cnt)
    return tag_cnt_dict


if __name__ == '__main__':
    ################### Path Setting ##########################
    task = 'tagRec'
    dataset = "SO-05-Sep-2018"
    dataset_dir = data_dir + os.sep + task + os.sep + dataset
    parallel_dir = dataset_dir + os.sep + "parallel"
    # ts
    ts = 50
    ts_dir = dataset_dir + os.sep + "ts%s" % ts
    ts_parallel_dir = ts_dir + os.sep + "parallel"

    if not os.path.exists(ts_dir):
        os.mkdir(ts_dir)
    if not os.path.exists(ts_parallel_dir):
        os.mkdir(ts_parallel_dir)

    # Input:
    tag_cnt_all_csv_fapth = dataset_dir + os.sep + "_0_tag-count-all.csv"

    # Output:
    rare_tags_fpath = ts_dir + os.sep + "_1_rareTags.csv"
    common_tags_fpath = ts_dir + os.sep + "_1_commonTags.csv"

    ################### Path Setting ##########################

    # <tag_cnt>
    tag_cnt = load_tag_cnt(tag_cnt_all_csv_fapth)

    # get rare tags [rare tags]
    identify_rare_tags(tag_cnt, rare_tags_fpath, common_tags_fpath, ts)
