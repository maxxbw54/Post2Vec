# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     data_utils
   Description :
   Author :       xubowen
   date：          2018/10/31 10:55 AM
-------------------------------------------------
   Change Activity:
                   2018/10/31 10:55 AM
-------------------------------------------------
"""
from pyToolkit.lib.utils.time_util import get_current_time
import ast
from data_structure.question import Question
from utils.memory_util import track


def load_tags(tags_fpath):
    tag_dict = dict()
    import pandas as pd
    df = pd.read_csv(tags_fpath, keep_default_na=False)
    for idx, row in df.iterrows():
        tag_dict[str(row['tag'])] = idx
    print("# tags = %s" % len(tag_dict))
    return tag_dict


def separate_text_code(html_str):
    import re
    # regex: <pre(.*)><code>([\s\S]*?)</code></pre>
    regex_pattern = r'<pre(.*?)><code>([\s\S]*?)</code></pre>'
    code_list = []
    html_text = html_str
    for m in re.finditer(regex_pattern, html_str):
        # print("start %d end %d" % (m.start(), m.end()))
        raw_code = html_str[m.start():m.end()]
        clean_code = clean_html_tags(raw_code).replace('\n', ' ')
        code_list.append(clean_code)
        # remove code
        html_text = html_text.replace(raw_code, " ")
    clean_html_text = clean_html_tags(html_text)
    clean_html_text = remove_symbols(clean_html_text)
    if len(code_list) == 0:
        code_str = ''
    else:
        code_str = ' '.join(code_list)
    return clean_html_text, code_str


def clean_html_tags(raw_html):
    from bs4 import BeautifulSoup
    try:
        text = BeautifulSoup(raw_html, "html.parser").text
    except Exception as e:
        # UnboundLocalError
        text = clean_html_tags2(raw_html)
    finally:
        return text


def clean_html_tags2(raw_html):
    import re
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def remove_symbols(strtmp):
    return strtmp.replace('\n', ' ')


@track
def load_corpus_csv(corpus_fpath):
    """
    return SOQuestion list from corpus
    :param path_file:
    :return:
    """
    import pandas as pd

    print("Loading corpus %s" % corpus_fpath, get_current_time())
    data = list()
    line_count = 0
    for index, row in pd.read_csv(corpus_fpath).iterrows():
        # ["id","title","desc_text","desc_code","creation_date","tags"]
        qid = row["id"]
        title = ast.literal_eval(row["title"])
        desc_text = ast.literal_eval(row["desc_text"])
        desc_code = ast.literal_eval(row["desc_code"])
        creation_date = row["creation_date"]
        tags = ast.literal_eval(row["tags"])
        soq = Question(qid, title, desc_text, desc_code, creation_date, tags)
        data.append(soq)
        line_count += 1
        if line_count % 10000 == 0:
            print("Loaded %d instances..." % line_count, get_current_time())
    print('Processed {%s} lines.' % line_count, get_current_time())
    return data


def get_all_comp(data_list):
    id_list = []
    title_list = []
    desc_text_list = []
    desc_code_list = []
    creation_date_list = []
    tags_list = []
    for d in data_list:
        id_list.append(d.qid)
        title_list.append(d.title)
        desc_text_list.append(d.desc_text)
        desc_code_list.append(d.desc_code)
        creation_date_list.append(d.creation_date)
        tags_list.append(d.tags)
    return id_list, title_list, desc_text_list, desc_code_list, creation_date_list, tags_list


def build_vocab(text):
    print("Building vocabulary...", get_current_time())
    new_text = list()
    for t in text:
        new_text += t
    new_text = sorted(list(set(new_text)))
    dictionary = dict()
    for i in range(len(new_text)):
        dictionary[new_text[i]] = i
    dictionary['<PAD>'] = len(new_text)
    return dictionary


def build_tag_vacab(tag):
    print("Building vocabulary...", get_current_time())
    new_tags = list()
    for t in tag:
        new_tags += t
    new_tags = sorted(list(set(new_tags)))
    return new_tags


def build_tag(tag):
    new_tags = list()
    for t in tag:
        new_tags += t
    new_tags = sorted(list(set(new_tags)))
    return new_tags


if __name__ == '__main__':
    text_str = str(
        """"Check for changes to an SQL Server table?","<p>How can I monitor an SQL Server database for changes to a table without using triggers or modifying the structure of the database in any way? My preferred programming environment is <a href=\"http://en.wikipedia.org/wiki/.NET_Framework\" rel=\"nofollow noreferrer\">.NET</a> and C#.</p>&#xA;&#xA;<p>I'd like to be able to support any <a href=\"http://en.wikipedia.org/wiki/Microsoft_SQL_Server#Genesis\" rel=\"nofollow noreferrer\">SQL Server 2000</a> SP4 or newer. My application is a bolt-on data visualization for another company's product. Our customer base is in the thousands, so I don't want to have to put in requirements that we modify the third-party vendor's table at every installation.</p>&#xA;&#xA;<p>By <em>\"changes to a table\"</em> I mean changes to table data, not changes to table structure.</p>&#xA;&#xA;<p>Ultimately, I would like the change to trigger an event in my application, instead of having to check for changes at an interval.</p>&#xA;&#xA;<hr>&#xA;&#xA;<p>The best course of action given my requirements (no triggers or schema modification, SQL Server 2000 and 2005) seems to be to use the <code>BINARY_CHECKSUM</code> function in <a href=\"http://en.wikipedia.org/wiki/Transact-SQL\" rel=\"nofollow noreferrer\">T-SQL</a>. The way I plan to implement is this:</p>&#xA;&#xA;<p>Every X seconds run the following query:</p>&#xA;&#xA;<pre><code>SELECT CHECKSUM_AGG(BINARY_CHECKSUM(*))&#xA;FROM sample_table&#xA;WITH (NOLOCK);&#xA;</code></pre>&#xA;&#xA;<p>And compare that against the stored value. If the value has changed, go through the table row by row using the query:</p>&#xA;&#xA;<pre><code>SELECT row_id, BINARY_CHECKSUM(*)&#xA;FROM sample_table&#xA;WITH (NOLOCK);&#xA;</code></pre>&#xA;&#xA;<p>And compare the returned checksums against stored values.</p>&#xA;""")
    text, code = separate_text_code(text_str)
    text = clean_html_tags(text)
    print("text:\n%s\n" % text)
    print("code:\n%s\n" % code)
    # for c in code:
    #     print("c:\n%s" % c)
