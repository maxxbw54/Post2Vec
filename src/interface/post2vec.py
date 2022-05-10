# -*- coding: utf-8 -*-
import os
from pathConfig import data_dir
from pyToolkit.lib.utils.pkl_util import load_pickle
from pyToolkit.lib.utils.time_util import get_current_time
from tasks.tag_rec.approaches.post2vec.post2vec_util import load_model, load_args
from utils.vocab_util import vocab_to_index_dict
import glob
import pickle


def get_post_vec(raw_qlist, data_dir):
    from utils.padding_and_indexing_util import padding_and_indexing_qlist_without_tag
    import copy

    model, len_dict, title_vocab, desc_text_vocab, desc_code_vocab = load_p2v_model_and_vocab(data_dir)

    # get corresponding vector
    print("Get corresponding vector...", get_current_time())
    raw_qlist = copy.deepcopy(raw_qlist)

    # processed qlist
    qlist = padding_and_indexing_qlist_without_tag(raw_qlist, len_dict, title_vocab, desc_text_vocab, desc_code_vocab)
    qvec = model.get_output_vector(qlist=qlist)

    print("qvec size %s" % len(qvec))

    q_dict = dict()
    for q in qvec:
        q_dict[q.qid] = q

    return q_dict


def load_p2v_model_and_vocab(data_dir):
    # load vocab
    # initial
    len_dict_fpath = os.path.join(data_dir, "vocab", "len.pkl")
    title_vocab_fpath = os.path.join(data_dir, "vocab", "title_vocab.pkl")
    desc_text_vocab_fpath = os.path.join(data_dir, "vocab", "desc_text_vocab.pkl")
    desc_code_vocab_fpath = os.path.join(data_dir, "vocab", "desc_code_vocab.pkl")

    # len
    len_dict = load_pickle(len_dict_fpath)

    # title vocabf
    title_vocab = load_pickle(title_vocab_fpath)
    title_vocab = vocab_to_index_dict(vocab=title_vocab, ifpad=True)

    # desc_text vocab1
    desc_text_vocab = load_pickle(desc_text_vocab_fpath)
    desc_text_vocab = vocab_to_index_dict(vocab=desc_text_vocab, ifpad=True)

    # desc_code_vocab
    desc_code_vocab = load_pickle(desc_code_vocab_fpath)
    desc_code_vocab = vocab_to_index_dict(vocab=desc_code_vocab, ifpad=True)

    param_fpath = os.path.join(data_dir, "model", "snapshot_steps_1291000.pt")
    arg_json_fpath = os.path.join(data_dir, "model", "args.json")

    # load approach
    print("Load args and model...", get_current_time())
    args = load_args(arg_json_fpath)
    model = load_model(args, param_fpath)

    return model, len_dict, title_vocab, desc_text_vocab, desc_code_vocab


def convert_input_qlist(csv_fpath):
    from data_structure.question import Question
    import pandas as pd

    qlist = []

    df = pd.read_csv(csv_fpath)
    for index, row in df.iterrows():
        # if math.isnan(row['Body Code']):
        #     row['Body Code'] = ''
        q = Question(qid=row['Id'], title=row['Title'], desc_text=row['Body Text'], desc_code=row['Body Code'])
        qlist.append(q)

    return qlist


def convert_output_qlist(qlist):
    general_output_qlist = dict()
    for qid in qlist:
        q = qlist[qid]
        general_output_qlist[q.qid] = {"Id": q.qid, "Title": q.title, "Body Text": q.desc_text,
                                       "Body Code": q.desc_code}

    return general_output_qlist


if __name__ == '__main__':

    input_data_dir = os.path.join(data_dir, "input", "XXX")  # set up input directory

    print(input_data_dir)

    for filepath in glob.iglob(input_data_dir + '/**/*', recursive=True):
        print(filepath)
        if os.path.isfile(filepath) and filepath.endswith(".csv"):  # filter dirs
            print(filepath)

            # input
            qlist = convert_input_qlist(filepath)

            # output
            output_pkl_fpath = filepath.replace(".csv", ".pkl")

            # get vectors
            qvectors = get_post_vec(qlist, data_dir)

            general_output_qlist = convert_output_qlist(qvectors)

            # save vectors
            with open(output_pkl_fpath, 'wb') as handle:
                pickle.dump(general_output_qlist, handle, protocol=pickle.HIGHEST_PROTOCOL)

            # test
            # with open(output_pkl_fpath, "rb") as input_file:
            #     e = pickle.load(input_file)
            #
            # print(e)
