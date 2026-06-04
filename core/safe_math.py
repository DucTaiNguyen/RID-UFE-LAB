import numpy as np

def safe_corr(x, y):

    x = np.asarray(x)
    y = np.asarray(y)

    if len(x) < 5 or len(y) < 5:
        return 0.0

    if np.std(x) == 0 or np.std(y) == 0:
        return 0.0

    c = np.corrcoef(x, y)[0, 1]

    if np.isnan(c) or np.isinf(c):
        return 0.0

    return float(c)
