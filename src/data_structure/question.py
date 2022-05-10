# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     SO_question
   Description :
   Author :       xubowen
   date：          2018/10/31 11:02 AM
-------------------------------------------------
"""
from nltk import word_tokenize


class Question:
    # use __slots to decrease the memory usage
    __slots__ = ['qid', 'title', 'desc_text', 'desc_code', 'creation_date', 'tags', 'combine']

    def __init__(self, qid=None, title=None, desc_text=None, desc_code=None, creation_date=None, tags=None):
        self.qid = qid
        self.title = title
        self.desc_text = desc_text
        self.desc_code = desc_code
        self.creation_date = creation_date
        self.tags = tags
        self.combine = None

    def get_comp_by_name(self, comp_name):
        if comp_name == "qid":
            return self.qid
        if comp_name == "title":
            return self.title
        if comp_name == "desc_text":
            return self.desc_text
        if comp_name == "desc_code":
            return self.desc_code
        if comp_name == "creation_date":
            return self.creation_date
        if comp_name == "tags":
            return self.tags
        if comp_name == "combine":
            return self.combine


def get_title(data):
    return [word_tokenize(d.title.lower()) for d in data]


def get_desc_text(data):
    return [word_tokenize(d.desc_text.lower()) for d in data]


def get_desc_code(data):
    return [word_tokenize(d.desc_code.lower()) for d in data]


def get_tags(data):
    return [d.tags.lower().replace('<', ' ').replace('>', ' ').strip().split() for d in data]
