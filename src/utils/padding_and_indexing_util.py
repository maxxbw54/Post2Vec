import math

import numpy as np

from data_structure.question import Question


def indexing_label(label, label_vocab):
    embedd_zero = [0 for i in range(len(label_vocab))]
    for l in label:
        if l in label_vocab:
            embedd_zero[label_vocab[l]] = 1
    return np.array(embedd_zero)


def padding_and_indexing_sent(sent, length, vocab):
    new = []
    for w in sent:
        if w in vocab:
            new.append(vocab[w])
            if len(new) == length:
                return np.array(new)
    add = length - len(new)
    for a in range(0, add):
        new.append(vocab['<PAD>'])
    return np.array(new)


def padding_and_indexing_q(q, len_dict, title_vocab, desc_text_vocab, desc_code_vocab, tag_vocab):
    # pre processing, padding and indexing
    q.title = padding_and_indexing_sent(sent=q.title, length=len_dict["max_title_len"], vocab=title_vocab)
    q.desc_text = padding_and_indexing_sent(sent=q.desc_text, length=len_dict["max_desc_text_len"],
                                            vocab=desc_text_vocab)

    q.desc_code = padding_and_indexing_sent(sent=q.desc_code, length=len_dict["max_desc_code_len"],
                                            vocab=desc_code_vocab)

    q.tags = indexing_label(label=q.tags, label_vocab=tag_vocab)
    if sum(q.tags) != 0:
        return q
    return None


def padding_and_indexing_q_combine(q, len_dict, all_vocab, tag_vocab):
    # pre processing, padding and indexing
    combine_q = Question(None, None, None, None, None, None)
    combine_q.qid = q.qid
    combine_q.title = q.title if len(q.title) < len_dict["max_title_len"] else q.title[:len_dict["max_title_len"]]
    combine_q.desc_text = q.desc_text if len(q.title) < len_dict["max_desc_text_len"] else q.desc_text[:len_dict[
        "max_desc_text_len"]]
    combine_q.desc_code = q.desc_code if len(q.title) < len_dict["max_desc_code_len"] else q.desc_code[:len_dict[
        "max_desc_code_len"]]
    combine_q.creation_date = q.creation_date

    # to match specific component, see build_combine_vocab.py
    q.title = ['title_' + w for w in q.title]
    q.desc_text = ['desc_text_' + w for w in q.desc_text]
    q.desc_code = ['desc_code_' + w for w in q.desc_code]
    q.combine = padding_and_indexing_sent(sent=q.title + q.desc_text + q.desc_code,
                                          length=len_dict["max_title_len"] + len_dict["max_desc_text_len"] + len_dict[
                                              "max_desc_code_len"], vocab=all_vocab)
    q.tags = indexing_label(label=q.tags, label_vocab=tag_vocab)
    if sum(q.tags) != 0:
        return q
    return None


def padding_and_indexing_q_title_desctext(q, len_dict, all_vocab, tag_vocab):
    # pre processing, padding and indexing
    combine_q = Question(None, None, None, None, None, None)
    combine_q.qid = q.qid
    combine_q.title = q.title if len(q.title) < len_dict["max_title_len"] else q.title[:len_dict["max_title_len"]]
    combine_q.desc_text = q.desc_text if len(q.title) < len_dict["max_desc_text_len"] else q.desc_text[:len_dict[
        "max_desc_text_len"]]
    combine_q.desc_code = q.desc_code if len(q.title) < len_dict["max_desc_code_len"] else q.desc_code[:len_dict[
        "max_desc_code_len"]]
    combine_q.creation_date = q.creation_date

    q.combine = padding_and_indexing_sent(sent=q.title + q.desc_text,
                                          length=len_dict["max_title_len"] + len_dict["max_desc_text_len"],
                                          vocab=all_vocab)
    q.tags = indexing_label(label=q.tags, label_vocab=tag_vocab)
    if sum(q.tags) != 0:
        return q
    return None


def padding_and_indexing_qlist(qlist, len_dict, title_vocab, desc_text_vocab, desc_code_vocab, tag_vocab):
    new_qlist = list()
    for q in qlist:
        # pre processing, padding and indexing
        q = padding_and_indexing_q(q, len_dict, title_vocab, desc_text_vocab, desc_code_vocab, tag_vocab)
        if q:
            new_qlist.append(q)

    return new_qlist


def padding_and_indexing_qlist_combine(qlist, len_dict, all_vocab, tag_vocab):
    new_qlist = list()
    for q in qlist:
        # pre processing, padding and indexing
        q = padding_and_indexing_q_combine(q, len_dict, all_vocab, tag_vocab)
        if q:
            new_qlist.append(q)

    return new_qlist


def padding_and_indexing_qlist_title_desctext(qlist, len_dict, all_vocab, tag_vocab):
    new_qlist = list()
    for q in qlist:
        # pre processing, padding and indexing
        q = padding_and_indexing_q_title_desctext(q, len_dict, all_vocab, tag_vocab)
        if q:
            new_qlist.append(q)

    return new_qlist


def padding_and_indexing_qlist_without_tag(qlist, len_dict, title_vocab, desc_text_vocab, desc_code_vocab):
    """
    without tag to reduce the size
    :param qlist:
    :param len_dict:
    :param title_vocab:
    :param desc_text_vocab:
    :param desc_code_vocab:
    :return:
    """
    new_qlist = list()
    for q in qlist:
        # pre processing, padding and indexing
        if type(q.title) == float and math.isnan(q.title):
            q.title = ''
        q.title = padding_and_indexing_sent(sent=q.title, length=len_dict["max_title_len"], vocab=title_vocab)
        if type(q.desc_text) == float and math.isnan(q.desc_text):
            q.desc_text = ''
        q.desc_text = padding_and_indexing_sent(sent=q.desc_text, length=len_dict["max_desc_text_len"],
                                                vocab=desc_text_vocab)
        if type(q.desc_code) == float and math.isnan(q.desc_code):
            q.desc_code = ''
        q.desc_code = padding_and_indexing_sent(sent=q.desc_code, length=len_dict["max_desc_code_len"],
                                                vocab=desc_code_vocab)

        if q:
            new_qlist.append(q)

    return new_qlist
