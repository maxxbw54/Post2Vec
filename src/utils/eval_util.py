# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       eval_util
   Description:
   Author:     bowen
   date:        1/7/19
-------------------------------------------------
"""


def evaluate(pred, label, topk, metric='ori'):
    """
    dimension of pred and label should be equal.
    :param pred: a list of prediction
    :param label: a list of true label
    :param topk:
    :return: a dictionary: {'precision': pre_k, 'recall': rec_k, 'f1': f1_k}
    """
    if metric == "ori":
        return evaluate_ori(pred, label, topk)
    elif metric == "standard":
        return evaluate_standard(pred, label, topk)
    elif metric == "topn":
        return evaluate_topn(pred, label, topk)
    elif metric == "map":
        return evaluate_map(pred, label)
    elif metric == "auc":
        return evaluate_auc(pred, label, topk)
    print("No such metric {} !".format(metric))
    exit(0)


def evaluate_ori(pred, label, topk):
    """
    dimension of pred and label should be equal.
    :param pred: a list of prediction
    :param label: a list of true label
    :param topk:
    :return: a dictionary: {'precision': pre_k, 'recall': rec_k, 'f1': f1_k}
    """
    top_idx_list = sorted(range(len(pred)), key=lambda i: pred[i])[-topk:]
    num_of_true_in_topk = len([idx for idx in top_idx_list if label[idx] == 1])
    # precision@k = #true label in topk / k
    pre_k = num_of_true_in_topk / float(topk)
    # recall@k = #true label in topk / #true label
    num_of_true_in_all = sum(label)
    if num_of_true_in_all > topk:
        rec_k = num_of_true_in_topk / float(topk)
    else:
        rec_k = num_of_true_in_topk / float(num_of_true_in_all)
    # f1@k = 2 * precision@k * recall@k / (precision@k + recall@k)
    if pre_k == 0 and rec_k == 0:
        f1_k = 0.0
    else:
        f1_k = 2 * pre_k * rec_k / (pre_k + rec_k)
    # return {'precision': pre_k, 'recall': rec_k, 'f1': f1_k}
    return pre_k, rec_k, f1_k


def evaluate_standard(pred, label, topk):
    """
    dimension of pred and label should be equal.
    :param pred: a list of prediction
    :param label: a list of true label
    :param topk:
    :return: a dictionary: {'precision': pre_k, 'recall': rec_k, 'f1': f1_k}
    """
    top_idx_list = sorted(range(len(pred)), key=lambda i: pred[i], reverse=True)[:topk]
    num_of_true_in_topk = len([idx for idx in top_idx_list if label[idx] == 1])
    # precision@k = #true label in topk / k
    pre_k = num_of_true_in_topk / float(topk)
    # recall@k = #true label in topk / #true label
    num_of_true_in_all = sum(label)
    rec_k = num_of_true_in_topk / float(num_of_true_in_all)
    # f1@k = 2 * precision@k * recall@k / (precision@k + recall@k)
    if pre_k == 0 and rec_k == 0:
        f1_k = 0.0
    else:
        f1_k = 2 * pre_k * rec_k / (pre_k + rec_k)
    # return {'precision': pre_k, 'recall': rec_k, 'f1': f1_k}
    # print("num_of_true_in_topk {} num_of_true_in_all {} pre_k {} rec_k {} f1_k {} topk {}".format(num_of_true_in_topk, num_of_true_in_all, pre_k, rec_k, f1_k, topk))
    # print("num_of_true_in_topk {} num_of_true_in_all {} pre_k {} rec_k {} f1_k {} topk {}".format(num_of_true_in_topk,
                                                                      
    #                                                                                                  num_of_true_in_all,
    #                                                                                                 pre_k, rec_k, f1_k,
    #                                                                                                topk))
    return pre_k, rec_k, f1_k


def evaluate_batch(pred, label, topk_list, metric=None):
    if metric == 'ori' or metric == 'standard':
        pre = [0.0] * len(topk_list)
        rc = [0.0] * len(topk_list)
        f1 = [0.0] * len(topk_list)
        cnt = 0
        for i in range(0, pred.shape[0]):
            for idx, topk in enumerate(topk_list):
                pre_val, rc_val, f1_val = evaluate(pred=pred[i], label=label[i], topk=topk, metric=metric)
                pre[idx] += pre_val
                rc[idx] += rc_val
                f1[idx] += f1_val
            cnt += 1
        pre[:] = [x / cnt for x in pre]
        rc[:] = [x / cnt for x in rc]
        f1[:] = [x / cnt for x in f1]
        return [pre, rc, f1, cnt]
    elif metric == 'topn':
        topn = [0.0] * len(topk_list)
        cnt = 0
        for i in range(0, pred.shape[0]):
            for idx, topk in enumerate(topk_list):
                success = evaluate(pred=pred[i], label=label[i], topk=topk, metric=metric)
                topn[idx] += success
            cnt += 1
        topn[:] = [x / float(cnt) for x in topn]
        return [topn]
    elif metric == 'map':
        map = list()
        for i in range(0, pred.shape[0]):
            avg_p = 0.0
            for idx, topk in enumerate(topk_list):
                pre_val = evaluate(pred=pred[i], label=label[i], topk=topk, metric=metric)
                avg_p += pre_val
            avg_p /= len(topk_list)
            map.append(avg_p)
        map_val = sum(map) / len(map)
        return [map_val]
    elif metric == 'mrr':
        mrr = list()
        for i in range(0, pred.shape[0]):
            mrr_val = evaluate_mrr(pred=pred[i], label=label[i])
            mrr.append(mrr_val)
        mrr_val = sum(mrr) / len(mrr)
        return [mrr_val]
    elif metric == 'auc':
        auc = evaluate_auc(pred=pred, label=label)
        return [auc]
    else:
        print("No such metric {}!".format(metric))


def evaluate_batch_f1_5(pred, label):
    f1_5_list = list()
    for i in range(0, pred.shape[0]):
        pre_5, rc_5, f1_5 = evaluate(pred=pred[i], label=label[i], topk=5)
        f1_5_list.append(f1_5)
    return f1_5_list


def evaluate_topn(pred, label, topk):
    top_idx_list = sorted(range(len(pred)), key=lambda i: pred[i], reverse=True)[:topk]
    num_of_true_in_topk = len([idx for idx in top_idx_list if label[idx] == 1])
    if num_of_true_in_topk > 0:
        return 1
    else:
        return 0


def evaluate_map(pred, label):
    top_idx_list = sorted(range(len(pred)), key=lambda i: pred[i], reverse=True)
    avgp = 0.0
    num_of_true_in_all = sum(label)
    num_of_true_in_topk = 0
    for i in range(len(top_idx_list)):
        idx = top_idx_list[i]
        if label[idx] == 1:
            num_of_true_in_topk += 1
            pi = num_of_true_in_topk / (i + 1.0)
            avgp += (pi / float(num_of_true_in_all))
        # optimize efficiency
        if num_of_true_in_all == num_of_true_in_topk:
            break
    return avgp


def evaluate_auc(pred, label):
    '''
    code from https://stackoverflow.com/questions/45139163/roc-auc-score-only-one-class-present-in-y-true?rq=1
    :param pred:
    :param label:
    :return:
    '''
    import numpy as np
    from sklearn.metrics import roc_auc_score
    label = [x.tolist() for x in label]
    pred = [x.tolist() for x in pred]
    return roc_auc_score(np.array(label), np.array(pred))


def evaluate_mrr(pred, label):
    top_idx_list = sorted(range(len(pred)), key=lambda i: pred[i], reverse=True)
    for pos, idx in enumerate(top_idx_list):
        if label[idx] != 0:
            return 1 / float(pos + 1.0)
    print("Exception in evaluate mrr!")
    exit()
