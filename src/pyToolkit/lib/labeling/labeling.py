from sklearn.metrics import cohen_kappa_score


def compute_kappa_score(label1, label2):
    return cohen_kappa_score(label1, label2)
