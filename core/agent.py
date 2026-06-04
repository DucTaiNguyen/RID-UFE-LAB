import numpy as np

from core.rolling import rolling_curvature
from core.causal import future_volatility, align_series
from core.multiscale import multiscale_curvature
from core.safe_math import safe_corr


def evaluate_hypothesis(returns):

    curv = rolling_curvature(returns)
    fut = future_volatility(returns, k=7, window=10)

    n = min(len(curv), len(fut))

    base_corr = safe_corr(curv[:n], fut[:n])

    multi = multiscale_curvature(returns)

    best_scale = None
    best_corr = -999

    for k, v in multi.items():

        m = min(len(v), len(fut))

        c = safe_corr(v[:m], fut[:m])

        if c > best_corr:
            best_corr = c
            best_scale = k

    return {
        "base_corr": base_corr,
        "best_scale": best_scale,
        "best_corr": float(best_corr)
    }
