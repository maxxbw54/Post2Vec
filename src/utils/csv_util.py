# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     csv_utils
   Description :
   Author :       xubowen
   date：          2018/10/31 11:39 AM
-------------------------------------------------
   Change Activity:
                   2018/10/31 11:39 AM
-------------------------------------------------
"""

from data_structure.question import Question
import csv


def write_Q_list_to_csv(q_list, csv_fpath, header):
    print("# q_list : %s" % len(q_list))
    with open(csv_fpath, 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(header)
        for q in q_list:
            wr.writerow([q.qid, q.title, q.desc_text, q.desc_code, q.tags])
    print("Write %s successfully!" % csv_fpath)


def read_csv_to_dict(csv_fpath):
    import pandas as pd
    return pd.Series.from_csv(csv_fpath, header=0).to_dict()


def read_csv_to_list(csv_fpath):
    import pandas as pd
    # keep_default_na=False to address null and nan!
    df = pd.read_csv(csv_fpath, keep_default_na=False)
    return [x[0] for x in df.values.tolist()]


def write_dict_to_csv(dict_tmp, csv_fpath, header=None):
    with open(csv_fpath, 'w') as myfile:
        wr = csv.writer(myfile)
        if header:
            wr.writerow(header)
        for k in dict_tmp:
            try:
                wr.writerow([k, dict_tmp[k]])
            except Exception as e:
                print("Error %s" % e)
    print("Write %s successfully!" % csv_fpath)


def write_list_to_csv(list_tmp, csv_fpath, header):
    if type(list_tmp) == set:
        list_tmp = list(list_tmp)
    with open(csv_fpath, 'w') as myfile:
        wr = csv.writer(myfile)
        if header:
            wr.writerow(header)
        for x in list_tmp:
            try:
                if type(x) == str:
                    x = [x]
                wr.writerow(x)
            except Exception as e:
                print("Error %s" % e)
    print("Write %s successfully!" % csv_fpath)


def load_q_list_from_csv(csv_fpath):
    q_list = list()
    with open(csv_fpath) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            q_list.append(Question(row[0], row[1], row[2], row[3], row[4]))
    return q_list


def load_csv2dict(csv_fpath):
    mydict = {}
    with open(csv_fpath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for rows in reader:
            k = rows[0]
            v = rows[1]
            mydict[k] = v
    return mydict


def load_vocab_from_csv(vocab_fpath):
    mydict = {}
    print("loading vocab1 %s" % vocab_fpath)
    with open(vocab_fpath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for rows in reader:
            k = rows[0]
            v = rows[1]
            mydict[k] = v
    return mydict


def load_tag_vocab_from_csv(tag_vocab_fpath):
    tags = []
    print("loading tag vocab1 %s" % tag_vocab_fpath)
    with open(tag_vocab_fpath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for rows in reader:
            tags.append(rows[0])
    return tags


def write_row_to_csv(row, fpath):
    import csv
    with open(fpath, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def write_rows_to_csv(rows, fpath):
    for row in rows:
        write_row_to_csv(row, fpath)


def append_new_row(row, fpath):
    import csv
    with open(fpath, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def read_csv_with_header(csv_fpath):
    import csv
    with open(csv_fpath) as f:
        csv_data = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    return csv_data


def append_new_rows(rows, fpath):
    for row in rows:
        append_new_row(row, fpath)
