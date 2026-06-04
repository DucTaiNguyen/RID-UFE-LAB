import numpy as np
from core.causal import future_volatility
from core.safe import safe_run


def null_correlation_test(returns, iterations=50):

    results = []

    for _ in range(iterations):

        shuffled = np.random.permutation(returns)

        fake_signal = np.random.normal(0, 1, len(shuffled))

        fut = future_volatility(shuffled, k=7, window=10)

        n = min(len(fake_signal), len(fut))

        if n < 5:
            continue

        corr = np.corrcoef(fake_signal[:n], fut[:n])[0, 1]

        if not np.isnan(corr):
            results.append(corr)

    return np.array(results if len(results) > 0 else [0.0])
