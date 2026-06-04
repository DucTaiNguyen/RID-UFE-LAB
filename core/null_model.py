import numpy as np
from core.causal import future_volatility, align_series
from core.safe_math import safe_corr

def null_correlation_test(returns, iterations=50):

    base = []

    for _ in range(iterations):

        shuffled = np.random.permutation(returns)

        curv = np.random.normal(0, 1, len(shuffled))
        fut = future_volatility(shuffled, k=7, window=10)

        n = min(len(curv), len(fut))

        base.append(safe_corr(curv[:n], fut[:n]))

    return np.array(base)
