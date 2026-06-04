import numpy as np

from core.rolling import rolling_curvature
from core.causal import future_volatility, align_series, correlation


def rolling_correlation(returns, k=7, window=80, step=5):

    corrs = []

    for i in range(window, len(returns) - k - window, step):

        sub = returns[i-window:i]

        curv = rolling_curvature(sub, window=40)

        fut = future_volatility(sub, k=k, window=10)

        c, v = align_series(curv, fut)

        if len(c) > 5:
            corrs.append(correlation(c, v))

    return np.array(corrs)
