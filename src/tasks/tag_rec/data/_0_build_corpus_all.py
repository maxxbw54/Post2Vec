from pathConfig import data_dir
from tasks.tag_rec.data.data_utils import clean_html_tags, separate_text_code
import csv
from pyToolkit.lib.utils.time_util import get_current_time
from nltk import word_tokenize
import os
from itertools import islice

'''
Input: read all-with-Raretag.csv <id, title, body, creation_date, tags>
Output: all-tokenized-with-Raretag.csv <id, title(tokenized), desc_text(tokenized), desc_code(tokenized), creation_date, tags>
for each instance, do,
1. separate desc_text and desc_code
2. tokenized title, desc_text and desc_code
'''

if __name__ == '__main__':
    task = 'tagRec'
    dataset = 'SO-05-Sep-2018'
    dataset_dir = data_dir + os.sep + task + os.sep + dataset
    parallel_dir = dataset_dir + os.sep + "parallel"
    if not os.path.exists(parallel_dir):
        os.mkdir(parallel_dir)
    print("Setting:\ntasks : %s\ndataset : %s\n" % (task, dataset))
    st_row_num = 13000000
    et_row_num = 14000000
    print("start line num = %s, end line num = %s" % (st_row_num, et_row_num))

    # input
    # "id", "title", "desc", "creation_date", "tags"
    all_raw_csv_fpath = dataset_dir + os.sep + 'all-with-Raretag.csv'

    # output
    # _0_all-clean-with-Raretag.csv
    # "id", "title", "desc_text", "desc_code", "creation_date", "tags"
    all_clean_csv_fpath = parallel_dir + os.sep + '_0_all-clean-with-Raretag-%s-%s.csv' % (st_row_num, et_row_num)

    print("Preprocessing corpus %s" % all_raw_csv_fpath, get_current_time())
    with open(all_raw_csv_fpath, 'r', encoding='utf-8', errors='surrogatepass') as all:
        rd = csv.reader(all, escapechar='\\')
        row_num = st_row_num
        cnt = 0
        corpus_header = ["id", "title", "desc_text", "desc_code", "creation_date", "tags"]
        with open(all_clean_csv_fpath, 'w') as out:
            wr = csv.writer(out)
            wr.writerow(corpus_header)
            for row in islice(rd, st_row_num, et_row_num):
                row_num += 1
                qid = row[0]
                title = row[1]
                desc = row[2]
                creation_date = row[3]
                tags = row[4].replace('<', ' ').replace('>', ' ').strip().split()

                # split desc_text and desc_code
                raw_desc_text, desc_code = separate_text_code(desc)
                clean_desc_text = clean_html_tags(raw_desc_text)

                # tokenization
                tokenized_title = word_tokenize(title.lower())
                tokenized_clean_desc_text = word_tokenize(clean_desc_text.lower())
                tokenized_desc_code = word_tokenize(desc_code.lower())

                try:
                    wr.writerow(
                        [qid, tokenized_title, tokenized_clean_desc_text, tokenized_desc_code, creation_date, tags])
                    cnt += 1
                except Exception as e:
                    print("Skip id=%s" % qid)
                    print("Error msg: %s" % e)
                if row_num % 10000 == 0:
                    print("Processing %s row..." % row_num, get_current_time())

    print('Processed {%s} lines. Success %s lines.' % (row_num, cnt), get_current_time())
