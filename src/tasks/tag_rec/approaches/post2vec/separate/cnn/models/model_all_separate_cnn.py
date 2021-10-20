import os
import sys

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from pyToolkit.lib.utils.csv_util import append_new_row
from pyToolkit.lib.utils.time_util import get_current_time
from utils.data_util import get_specific_comp_list
from utils.eval_util import evaluate_batch, evaluate_batch_f1_5


class MultiComp(nn.Module):

    def __init__(self, args):
        super(MultiComp, self).__init__()

        self.args = args
        self.title_embed = nn.Embedding(args.title_embed_num, args.embed_dim)
        self.desc_text_embed = nn.Embedding(args.desc_text_embed_num, args.embed_dim)
        self.desc_code_embed = nn.Embedding(args.desc_code_embed_num, args.embed_dim)
        self.convs_t = nn.ModuleList(
            [nn.Conv2d(1, args.title_kernel_num, (K, args.embed_dim)) for K in args.title_kernel_sizes])
        self.convs_dt = nn.ModuleList(
            [nn.Conv2d(1, args.desc_text_kernel_num, (K, args.embed_dim)) for K in args.desc_text_kernel_sizes])
        self.convs_dc = nn.ModuleList(
            [nn.Conv2d(1, args.desc_code_kernel_num, (K, args.embed_dim)) for K in args.desc_code_kernel_sizes])
        self.dropout = nn.Dropout(args.dropout)

        self.fc1 = nn.Linear(
            (len(args.title_kernel_sizes) * args.title_kernel_num + len(
                args.desc_text_kernel_sizes) * args.desc_text_kernel_num + len(
                args.desc_code_kernel_sizes) * args.desc_code_kernel_num),
            args.hidden_dim)
        self.fc2 = nn.Linear(args.hidden_dim, args.class_num)

    def forward(self, t, dt, dc):
        t = self.title_embed(t.cuda() if torch.cuda.is_available() else t)  # [128,1,100,32]
        dt = self.desc_text_embed(dt.cuda() if torch.cuda.is_available() else dt)  # [128,1,1000,32]
        dc = self.desc_code_embed(dc.cuda() if torch.cuda.is_available() else dc)  # [128,1,1000,32]

        if self.args.static:
            t = Variable(t)
            dt = Variable(dt)
            dc = Variable(dc)

        t = t.unsqueeze(1)  # (N, Ci, W, D) # [128,1,100,32]
        dt = dt.unsqueeze(1)  # (N, Ci, W, D) # [128,1,1000,32]
        dc = dc.unsqueeze(1)  # (N, Ci, W, D) # [128,1,1000,32]

        t = [F.relu(conv(t)).squeeze(3) for conv in self.convs_t]  # [(N, Co, W), ...]*len(Ks)
        dt = [F.relu(conv(dt)).squeeze(3) for conv in self.convs_dt]  # [(N, Co, W), ...]*len(Ks)
        dc = [F.relu(conv(dc)).squeeze(3) for conv in self.convs_dc]  # [(N, Co, W), ...]*len(Ks)

        t = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in t]  # [(N, Co), ...]*len(Ks)
        dt = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in dt]  # [(N, Co), ...]*len(Ks)
        dc = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in dc]  # [(N, Co), ...]*len(Ks)

        x_t, x_dt, x_dc = torch.cat(t, 1), torch.cat(dt, 1), torch.cat(dc, 1)
        x = torch.cat((x_t, x_dt, x_dc), 1)

        x = self.dropout(x)  # (N, len(Ks)*Co) (128, 900)
        sigmoid = nn.Sigmoid()
        x = F.relu(self.fc1(x))  # (N, C)
        logit = self.fc2(x)  # (N, C)
        output = sigmoid(logit)

        return output

    def get_output_vector(self, qlist=None, batch_size=64):
        with torch.no_grad():
            for i in range(0, len(qlist), batch_size):
                st = i
                if i + batch_size < len(qlist):
                    et = i + batch_size
                else:
                    et = len(qlist)

                # features
                t = get_specific_comp_list("title", qlist[st:et])
                dt = get_specific_comp_list("desc_text", qlist[st:et])
                dc = get_specific_comp_list("desc_code", qlist[st:et])

                t = torch.tensor(t).long()
                dt = torch.tensor(dt).long()
                dc = torch.tensor(dc).long()

                if self.args.cuda:
                    t, dt, dc = t.cuda(), dt.cuda(), dc.cuda()

                t = self.title_embed(t.cuda() if torch.cuda.is_available() else t)  # [128,1,100,32]
                dt = self.desc_text_embed(dt.cuda() if torch.cuda.is_available() else dt)  # [128,1,1000,32]
                dc = self.desc_code_embed(dc.cuda() if torch.cuda.is_available() else dc)  # [128,1,1000,32]

                if self.args.static:
                    t = Variable(t)
                    dt = Variable(dt)
                    dc = Variable(dc)

                t = t.unsqueeze(1)  # (N, Ci, W, D) # [128,1,100,32]
                dt = dt.unsqueeze(1)  # (N, Ci, W, D) # [128,1,1000,32]
                dc = dc.unsqueeze(1)  # (N, Ci, W, D) # [128,1,1000,32]

                t = [F.relu(conv(t)).squeeze(3) for conv in self.convs_t]  # [(N, Co, W), ...]*len(Ks)
                dt = [F.relu(conv(dt)).squeeze(3) for conv in self.convs_dt]  # [(N, Co, W), ...]*len(Ks)
                dc = [F.relu(conv(dc)).squeeze(3) for conv in self.convs_dc]  # [(N, Co, W), ...]*len(Ks)

                t = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in t]  # [(N, Co), ...]*len(Ks)
                dt = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in dt]  # [(N, Co), ...]*len(Ks)
                dc = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in dc]  # [(N, Co), ...]*len(Ks)

                x_t, x_dt, x_dc = torch.cat(t, 1), torch.cat(dt, 1), torch.cat(dc, 1)

                for j in range(et - st):
                    qlist[st + j].title = (Variable(x_t).data).cpu().numpy()[j]
                    qlist[st + j].desc_text = (Variable(x_dt).data).cpu().numpy()[j]
                    qlist[st + j].desc_code = (Variable(x_dc).data).cpu().numpy()[j]

        return qlist


def train(train_iter, dev_iter, model, args, global_train_step, best_acc):
    if args.cuda:
        model.cuda()

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    steps = 0
    last_step = 0
    model.train()
    for epoch in range(1, args.epochs + 1):
        print("\n#epoch %s" % epoch, get_current_time())
        for batch in train_iter:
            # features
            t = np.array(get_specific_comp_list("title", batch))
            dt = np.array(get_specific_comp_list("desc_text", batch))
            dc = np.array(get_specific_comp_list("desc_code", batch))
            # label
            target = get_specific_comp_list("tags", batch)

            t = torch.tensor(t).long()
            dt = torch.tensor(dt).long()
            dc = torch.tensor(dc).long()
            target = torch.tensor(target).float()

            if args.cuda:
                t, dt, dc, target = t.cuda(), dt.cuda(), dc.cuda(), target.cuda()

            optimizer.zero_grad()
            logit = model(t, dt, dc)
            # debug
            # print("logit.reshape(-1) shape %s"%logit.reshape(-1).shape)
            # print("logit.reshape(-1).[:10] %s"%logit.reshape(-1)[:10])
            # print("target.reshape(-1) shape %s"%target.reshape(-1).shape)
            # print("target.reshape(-1)[:10] %s"%target.reshape(-1)[:10])
            loss = nn.BCELoss(reduction="none")
            loss = loss(logit.reshape(-1), target.reshape(-1))

            loss = loss.mean()
            loss.backward()
            optimizer.step()

            steps += 1
            global_train_step += 1
            # record loss foreach step
            loss_record_fpath = os.path.join(args.save_dir, "loss_cur.csv")
            append_new_row([global_train_step, loss.item()], loss_record_fpath)
            if steps % args.log_interval == 0:
                sys.stdout.write('\rBatch[{}] - loss: {:.10f}'.format(steps, loss))
            if steps % args.dev_interval == 0 and args.dev_ratio != 0.0 and len(dev_iter) != 0:
                dev_loss, dev_acc = dev_eval(dev_iter, model, args)
                # record loss foreach step
                dev_loss_record_fpath = os.path.join(args.save_dir, "dev_loss_cur.csv")
                append_new_row([global_train_step, dev_loss, dev_acc], dev_loss_record_fpath)
                if dev_acc > best_acc:
                    best_acc = dev_acc
                    last_step = steps
                    if args.save_best:
                        save(model, args.save_dir, 'best', global_train_step)
                    print("\tBest f1@5 {:5f}".format(dev_acc))
                else:
                    if steps - last_step >= args.early_stop:
                        print('\tearly stop by {} steps.'.format(args.early_stop))
            if global_train_step % args.save_interval == 0:
                print("\nglobal_train_step {} - step {} - loss {:.10f}".format(global_train_step, steps, loss),
                      get_current_time())
                save(model, args.save_dir, 'snapshot', global_train_step)
    return model, global_train_step, best_acc


def dev_eval(data_iter, model, args):
    model.eval()
    metric = args.dev_metric
    topk_list = args.dev_metric_topk
    with torch.no_grad():
        if metric == 'ori' or metric == 'standard':
            pre = [0.0] * len(topk_list)
            rc = [0.0] * len(topk_list)
            f1 = [0.0] * len(topk_list)
        else:
            print("No such metric {}!".format(metric))
            exit(0)
        cnt = 0
        for batch in data_iter:
            # features
            t = get_specific_comp_list("title", batch)
            dt = get_specific_comp_list("desc_text", batch)
            dc = get_specific_comp_list("desc_code", batch)
            # label
            target = np.array(get_specific_comp_list("tags", batch))

            t = torch.tensor(t).long()
            dt = torch.tensor(dt).long()
            dc = torch.tensor(dc).long()
            target = torch.tensor(target).float()

            if args.cuda:
                t, dt, dc, target = t.cuda(), dt.cuda(), dc.cuda(), target.cuda()

            logit = model(t, dt, dc)

            loss = nn.BCELoss(reduction="none")
            loss = loss(logit.reshape(-1), target.reshape(-1))

            loss = loss.mean()

            if torch.cuda.is_available():
                res = evaluate_batch(pred=logit.cpu().detach().numpy(), label=target.cpu().detach().numpy(),
                                     topk_list=topk_list, metric=metric)
            else:
                res = evaluate_batch(pred=logit.detach().numpy(), label=target.detach().numpy(),
                                     topk_list=topk_list, metric=metric)

            if metric == 'ori' or metric == 'standard':
                pre_batch, rc_batch, f1_batch = res[0], res[1], res[2]
                for idx, topk in enumerate(topk_list):
                    pre[idx] += pre_batch[idx]
                    rc[idx] += rc_batch[idx]
                    f1[idx] += f1_batch[idx]

            cnt += 1

        if metric == 'ori' or metric == 'standard':
            pre[:] = [x / cnt for x in pre]
            rc[:] = [x / cnt for x in rc]
            f1[:] = [x / cnt for x in f1]
            return loss.item(), f1[4]  # regard f1@5 as main metric


def test_eval(data_iter, model, args, topk_list, metric):
    model.eval()
    with torch.no_grad():
        if metric == 'ori' or metric == 'standard':
            pre = [0.0] * len(topk_list)
            rc = [0.0] * len(topk_list)
            f1 = [0.0] * len(topk_list)
        elif metric == 'topn':
            topn = [0.0] * len(topk_list)
        elif metric == 'map':
            map = 0.0
        elif metric == 'mrr':
            mrr = 0.0
        elif metric == 'auc':
            auc = 0.0
        else:
            print("No such metric {}!".format(metric))
            exit(0)
        cnt = 0
        for batch in data_iter:
            # features
            t = get_specific_comp_list("title", batch)
            dt = get_specific_comp_list("desc_text", batch)
            dc = get_specific_comp_list("desc_code", batch)
            # label
            target = np.array(get_specific_comp_list("tags", batch))

            t = torch.tensor(t).long()
            dt = torch.tensor(dt).long()
            dc = torch.tensor(dc).long()
            target = torch.tensor(target).float()

            if args.cuda:
                t, dt, dc, target = t.cuda(), dt.cuda(), dc.cuda(), target.cuda()

            logit = model(t, dt, dc)

            if torch.cuda.is_available():
                res = evaluate_batch(pred=logit.cpu().detach().numpy(), label=target.cpu().detach().numpy(),
                                     topk_list=topk_list, metric=metric)
            else:
                res = evaluate_batch(pred=logit.detach().numpy(), label=target.detach().numpy(),
                                     topk_list=topk_list, metric=metric)

            if metric == 'ori' or metric == 'standard':
                pre_batch, rc_batch, f1_batch = res[0], res[1], res[2]
                for idx, topk in enumerate(topk_list):
                    pre[idx] += pre_batch[idx]
                    rc[idx] += rc_batch[idx]
                    f1[idx] += f1_batch[idx]
            elif metric == 'topn':
                topn_batch = res[0]
                for idx, topk in enumerate(topk_list):
                    topn[idx] += topn_batch[idx]
            elif metric == 'map':
                map_batch = res[0]
                map += map_batch
            elif metric == 'mrr':
                mrr_batch = res[0]
                mrr += mrr_batch
            elif metric == 'auc':
                auc_batch = res[0]
                auc += auc_batch

            cnt += 1

        if metric == 'ori' or metric == 'standard':
            pre[:] = [x / cnt for x in pre]
            rc[:] = [x / cnt for x in rc]
            f1[:] = [x / cnt for x in f1]
            return [pre, rc, f1]
        elif metric == 'topn':
            topn[:] = [x / cnt for x in topn]
            return [topn]
        elif metric == 'map':
            map /= cnt
            return [map]
        elif metric == 'mrr':
            mrr /= cnt
            return [mrr]
        elif metric == 'auc':
            auc /= cnt
            return [auc]

def test_f1_5_eval(data_iter, model, args, metric):
    model.eval()
    with torch.no_grad():
        f1_5_list = []
        if metric != 'ori' and metric != 'standard':
            print("No such metric {}!".format(metric))
            exit(0)
        for batch in data_iter:
            # features
            t = get_specific_comp_list("title", batch)
            dt = get_specific_comp_list("desc_text", batch)
            dc = get_specific_comp_list("desc_code", batch)
            # label
            target = np.array(get_specific_comp_list("tags", batch))

            t = torch.tensor(t).long()
            dt = torch.tensor(dt).long()
            dc = torch.tensor(dc).long()
            target = torch.tensor(target).float()

            if args.cuda:
                t, dt, dc, target = t.cuda(), dt.cuda(), dc.cuda(), target.cuda()

            logit = model(t, dt, dc)

            if torch.cuda.is_available():
                f1_5_list_single_batch = evaluate_batch_f1_5(pred=logit.cpu().detach().numpy(),
                                                             label=target.cpu().detach().numpy())
            else:
                f1_5_list_single_batch = evaluate_batch_f1_5(pred=logit.detach().numpy(), label=target.detach().numpy())

            if metric == 'ori' or metric == 'standard':
                f1_5_list.extend(f1_5_list_single_batch)

        return f1_5_list


def save(model, save_dir, save_prefix, steps):
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    # save parameter
    save_prefix = os.path.join(save_dir, save_prefix)
    save_path = '{}_steps_{}.pt'.format(save_prefix, steps)
    torch.save(model.state_dict(), save_path)
