import numpy as np

def log_returns(x):

    x = np.asarray(x)

    return np.diff(np.log(x + 1e-12))


def volatility(r):

    return float(np.std(r))


def entropy(r):

    hist, _ = np.histogram(r, bins=30, density=True)

    hist = hist[hist > 0]

    p = hist / np.sum(hist)

    return float(-np.sum(p * np.log(p)))
