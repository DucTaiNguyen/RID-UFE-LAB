import numpy as np

def build_graph(series):

    series = np.asarray(series).reshape(-1)

    diff = np.abs(
        series[:, None]
        -
        series[None, :]
    )

    return np.exp(-diff)
