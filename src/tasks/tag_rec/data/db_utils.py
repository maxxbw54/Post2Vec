import pymysql as mdb
from data_structure.question import Question
from data_preparation.tag_rec.data_utils import clean_html_tags, separate_text_code
from utils.time_util import get_current_time

db_name = "May-2016-SO"


def extract_by_id_list(id_list, table_name, rare_tags):
    q_list = list()
    con = mdb.connect('localhost', 'root', 'root', db_name)
    cur = con.cursor()
    batch_size = 500
    total_batch = int(len(id_list) / batch_size) + 1
    count = 0
    for batch_idx in range(total_batch):
        if count % 10000 == 0:
            print('reading %s question from Table %s' % (count, table_name), get_current_time())
        count += batch_size

        batch_sql = "SELECT * FROM %s WHERE PostTypeId = 1 AND Id IN(" % (table_name)
        if batch_idx < total_batch - 1:
            for i in range(batch_size):
                idx = batch_idx * batch_size + i
                batch_sql += ('%s,' % id_list[idx])
        elif batch_idx == total_batch - 1:
            for idx in range(batch_idx * batch_size, len(id_list)):
                batch_sql += ('%s,' % id_list[idx])
        # -1 because need to remove symbol ","
        batch_sql = batch_sql[:-1] + ')'
        try:
            cur.execute(batch_sql)
            results = cur.fetchall()
            for row in results:
                # id,title,body
                id = row[0]
                title = row[11]
                desc = row[6]
                tags = row[12].replace('<', ' ').replace('>', ' ').strip().split()
                clean_tags = list(set(tags) - set(rare_tags))

                raw_desc_text, desc_code = separate_text_code(desc)
                clean_desc_text = clean_html_tags(raw_desc_text)

                q = Question(id=id, title=title, desc_text=clean_desc_text, desc_code=desc_code, tags=clean_tags)
                q_list.append(q)
        except Exception as e:
            print(e)
    cur.close()
    con.close()
    return q_list
