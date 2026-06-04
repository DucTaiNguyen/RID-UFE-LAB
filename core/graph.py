import numpy as np

def build_graph(series):

    x = np.asarray(series).reshape(-1)

    # normalize
    x = (x - np.mean(x)) / (np.std(x) + 1e-12)

    diff = np.abs(x[:, None] - x[None, :])

    sigma = np.std(diff) + 1e-12

    W = np.exp(-diff / sigma)

    return W
