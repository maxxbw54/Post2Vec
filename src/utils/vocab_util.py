def vocab_to_index_dict(vocab, ifpad=False):
    # use sort because require consistent
    vocab_list = list(vocab)
    vocab_list.sort()
    vocab_dict = dict()
    for i in range(len(vocab_list)):
        vocab_dict[vocab_list[i]] = i
    if ifpad:
        vocab_dict['<PAD>'] = len(vocab_dict)
    return vocab_dict
