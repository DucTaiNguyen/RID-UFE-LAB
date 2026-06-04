import numpy as np

def time_split(series, train_ratio=0.6, test_ratio=0.2):

    series = np.asarray(series)

    n = len(series)

    a = int(n * train_ratio)
    b = int(n * (train_ratio + test_ratio))

    train = series[:a]
    test = series[a:b]
    val = series[b:]

    return train, test, val
