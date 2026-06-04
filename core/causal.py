import numpy as np

def future_volatility(returns, k=7, window=10):

    vols = []

    for i in range(len(returns) - k - window):

        future = returns[i + k : i + k + window]

        vol = np.std(future)

        vols.append(vol)

    return np.array(vols)


def align_series(curvature, target):

    n = min(len(curvature), len(target))

    return curvature[:n], target[:n]


def correlation(x, y):

    x = np.asarray(x)
    y = np.asarray(y)

    return float(np.corrcoef(x, y)[0, 1])
