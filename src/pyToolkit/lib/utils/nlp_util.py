# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       nlp_util
   Description:
   Author:     bowen
   date:        7/24/19
-------------------------------------------------
"""
import nltk
from nltk.corpus import stopwords

# nltk.download()

stop_wlist = set(stopwords.words('english'))


def word_count_from_sent(sent, if_stem=False, if_remove_sw=False):
    cnt_dict = dict()
    if if_stem:
        wlist = tokenize(sent)
        wlist = stem_wlist(wlist)
    else:
        wlist = tokenize(sent)

    if if_remove_sw:
        wlist = stop_words_removal(wlist)

    for x in wlist:
        if x in cnt_dict:
            cnt_dict[x] = cnt_dict[x] + 1
        else:
            cnt_dict[x] = 1
    return cnt_dict


def stem_wlist(wlist):
    stemmer = nltk.stem.PorterStemmer()
    return [stemmer.stem(x) for x in wlist]


def word_count_from_corpus(corpus, if_stem=False, if_remove_sw=False, if_remove_symbol=True, exclude_wset=set()):
    wcnt_dict = dict()
    for sent in corpus:
        wcnt = word_count_from_sent(sent, if_stem, if_remove_sw)
        for w in wcnt:
            if len(w) <= 1:
                continue
            if w not in wcnt_dict:
                wcnt_dict[w] = 1
            else:
                wcnt_dict[w] = wcnt_dict[w] + 1
    return wcnt_dict


def tokenize(sent):
    return nltk.word_tokenize(sent)


def stop_words_removal(wlist):
    return [x for x in wlist if x not in stop_wlist]
