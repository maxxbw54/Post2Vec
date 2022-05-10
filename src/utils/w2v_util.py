# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       w2v_util
   Description:
   Author:     bowen
   date:        12/12/18
-------------------------------------------------
"""
from gensim.models.word2vec import Word2Vec, LineSentence
import gensim
from utils.time_util import get_current_time
from utils.data_util import save_pickle


def build_w2v_model(corpus_fpath, model_fpath):
    print('training %s' % corpus_fpath, get_current_time())
    # size is the dimensionality of the feature vectors.
    # window is the maximum distance between the current and predicted word within a sentence.
    # min_count = ignore all words with total frequency lower than this.
    # workers = use this many worker threads to train the model (=faster training with multicore machines).
    sentences = LineSentence(corpus_fpath)
    model = Word2Vec(sentences, size=200, workers=10, min_count=1)

    model.save(model_fpath)

    # vocab1 = dict()
    # wlist = model.wv.index2word
    # for i in range(len(wlist)):
    #     vocab1[wlist[i]] = i
    #
    # save_pickle(vocab1, vocab_fpath)
    print('end time : ', get_current_time())


def load_w2v_model(model_fpath):
    print("Loading w2v model %s..." % model_fpath, get_current_time())
    w2v_model = gensim.models.Word2Vec.load(model_fpath)

    print("Loaded.", get_current_time())
    return w2v_model


def get_word_index(model):
    idx_dict = dict()
    for w in model.wv.vocab.keys():
        idx_dict[w] = model.wv.vocab[w].index
    return idx_dict
