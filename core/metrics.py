import numpy as np

def log_returns(prices):
    return np.diff(np.log(prices))

def volatility(r):
    return np.std(r)

def entropy(r, bins=50):
    hist, _ = np.histogram(r, bins=bins, density=True)
    hist = hist[hist > 0]
    return -np.sum(hist * np.log(hist))

def information_ratio(r):
    return np.mean(r) / (np.std(r) + 1e-8)
