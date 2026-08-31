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
            value = correlation(c, v)

            if np.isfinite(value):
                corrs.append(value)

    return np.array(corrs)


def run_robustness(returns, runs=6):
    results = []

    for i in range(runs):
        values = rolling_correlation(
            returns,
            k=7,
            window=80,
            step=5 + i
        )

        if len(values) > 0:
            results.append(float(np.mean(values)))

    if not results:
        return {
            "mean": 0.0,
            "std": 0.0,
            "runs": 0
        }

    return {
        "mean": float(np.mean(results)),
        "std": float(np.std(results)),
        "runs": len(results)
    }
