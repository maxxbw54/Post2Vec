import csv
import math
import numpy as np
from data_structure.question import Question


def load_csv(path_file):
    with open(path_file, mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        data = list()
        for row in csv_reader:
            if line_count == 0:
                print('Column names are %s' % row)
                line_count += 1
            else:
                soq = Question(row[0], row[1], row[2], row[3], row[4])
                data.append(soq)
                line_count += 1
        print('Processed %s lines.' % line_count)
    return data


def random_mini_batch(data, mini_batch_size=64, seed=0):
    m = len(data)
    mini_batches = list()
    np.random.seed(seed)

    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_data = [data[idx] for idx in permutation]

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = math.floor(
        m / float(mini_batch_size))  # number of mini batches of size mini_batch_size in your partitionning
    num_complete_minibatches = int(num_complete_minibatches)
    for k in range(0, num_complete_minibatches):
        mini_batch = shuffled_data[k * mini_batch_size: k * mini_batch_size + mini_batch_size]
        mini_batches.append(mini_batch)

    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch = shuffled_data[num_complete_minibatches * mini_batch_size: m]
        mini_batches.append(mini_batch)
    return mini_batches


def build_vocab(text):
    new_text = list()
    for t in text:
        new_text += t
    new_text = sorted(list(set(new_text)))
    dictionary = dict()
    for i in range(len(new_text)):
        dictionary[new_text[i]] = i
    dictionary['<PAD>'] = len(new_text)
    return dictionary


def build_tag(tag):
    new_tags = list()
    for t in tag:
        new_tags += t
    new_tags = sorted(list(set(new_tags)))
    return new_tags


def get_specific_comp_list(comp_name, data_list):
    if comp_name == "id":
        return [d.qid for d in data_list]
    elif comp_name == "title":
        return [d.title for d in data_list]
    elif comp_name == "desc_text":
        return [d.desc_text for d in data_list]
    elif comp_name == "desc_code":
        return [d.desc_code for d in data_list]
    elif comp_name == "tags":
        return [d.tags for d in data_list]
    elif comp_name == "text":
        return [d.text for d in data_list]
    elif comp_name == "combine":
        return [d.combine for d in data_list]
    else:
        raise Exception("No such %s component!" % comp_name)


def vectorize_tags(tags, tag_idx_vocab):
    import numpy as np
    tag_vec = np.zeros(len(tag_idx_vocab))
    for t in tags:
        tag_vec[tag_idx_vocab[t]] = 1
    return tag_vec
