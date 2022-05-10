# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     model_util
   Description :
   Author :       bowenxu
   date：          11/12/18
-------------------------------------------------
"""
import argparse
import os
import torch
from pyToolkit.lib.utils.json_util import read_json_from_file
from pyToolkit.lib.utils.time_util import get_current_time


def save_args(args):
    # save args
    import json, os
    from copy import copy

    if not os.path.isdir(args.save_dir):
        os.makedirs(args.save_dir)
    arg_fpath = os.path.join(args.save_dir, "args.json")
    arg_dict = vars(copy(args))
    for x in arg_dict:
        arg_dict[x] = str(arg_dict[x])
    with open(arg_fpath, 'w') as f:
        f.write(json.dumps(arg_dict, indent=4))
    print("Saved argument in %s" % arg_fpath)


def load_args(arg_json_path):
    ############################ model arguments settings ############################
    parser = argparse.ArgumentParser(description='Multi-label Classifier based on Multi-component')
    args = parser.parse_args()
    arg_dict = args.__dict__

    # load arguments from arg.json
    arg_json = read_json_from_file(arg_json_path)
    for key, val in arg_json.items():
        try:
            if key == "device":
                val = -1
            if key != "model_selection":
                val = eval(val)
        except Exception as e:
            pass
        finally:
            arg_dict[key] = val

    arg_dict["train"] = None

    args.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print("Loaded args.", get_current_time())

    return args


def load_model(args, param_fpath):
    # model selection
    if args.model_selection == 'ori_separate_all_cnn':
        from tasks.tag_rec.approaches.post2vec.orignal.models.ori_model_all_cnn import MultiComp

        model = MultiComp(args)
    # cnn
    elif args.model_selection == 'separate_all_cnn':
        from tasks.tag_rec.approaches.post2vec.separate.cnn.models.model_all_separate_cnn import MultiComp

        model = MultiComp(args)
    elif args.model_selection == 'separate_title_desctext_cnn':
        from tasks.tag_rec.approaches.post2vec.separate.cnn.models.model_title_desctext_separate_cnn import MultiComp

        model = MultiComp(args)
    elif args.model_selection == 'combine_all_cnn':
        from tasks.tag_rec.approaches.post2vec.combine.cnn.models.model_combine_cnn import MultiComp

        model = MultiComp(args)
    # lstm
    elif args.model_selection == 'separate_all_bilstm':
        from tasks.tag_rec.approaches.post2vec.separate.lstm.models.model_all_separate_bilstm import MultiComp

        model = MultiComp(args)
    elif args.model_selection == 'separate_title_desctext_bilstm':
        from tasks.tag_rec.approaches.post2vec.separate.lstm.models.model_title_desctext_separate_bilstm import MultiComp

        model = MultiComp(args)
    elif args.model_selection == 'combine_all_lstm':
        from tasks.tag_rec.approaches.post2vec.combine.lstm.models.model_combine_lstm import MultiComp

        model = MultiComp(args)
    else:
        print("No such model!")
        exit()

    print("Inited model %s use param %s." % (args.model_selection, param_fpath), get_current_time())

    model.load_state_dict(torch.load(param_fpath))

    if args.cuda:
        torch.cuda.set_device(-1)
        model = model.cuda()

    print("Loaded model.", get_current_time())

    return model
