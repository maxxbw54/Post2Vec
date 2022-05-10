import _pickle as cPickle
from pyToolkit.lib.utils.time_util import get_current_time


def save_pickle(data, fpath):
    print("Saving %s..." % fpath, get_current_time())
    with open(fpath, 'wb') as handle:
        cPickle.dump(data, handle)
    print("Saved.", get_current_time())


def load_pickle(fpath):
    # print("Loading %s..." % fpath, get_current_time())
    with open(fpath, 'rb') as handle:
        data = cPickle.load(handle)
    # print("Loaded.", get_current_time())
    return data
