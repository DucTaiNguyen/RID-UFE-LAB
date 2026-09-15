import numpy as np


def log_returns(prices):
    prices = np.asarray(prices, dtype=float)

    if len(prices) < 2:
        return np.array([], dtype=float)

    if np.any(prices <= 0):
        raise ValueError("Prices must be strictly positive")

    return np.diff(np.log(prices))


def volatility(returns):
    returns = np.asarray(returns, dtype=float)

    if len(returns) == 0:
        return 0.0

    return float(np.std(returns))


def entropy(returns, bins=30):
    """
    Shannon entropy of the empirical return distribution.
    """
    returns = np.asarray(returns, dtype=float)
    returns = returns[np.isfinite(returns)]

    if len(returns) < 2:
        return 0.0

    if np.allclose(returns, returns[0]):
        return 0.0

    counts, _ = np.histogram(returns, bins=bins)

    total = counts.sum()

    if total == 0:
        return 0.0

    probabilities = counts[counts > 0].astype(float) / total

    return float(-np.sum(probabilities * np.log(probabilities)))


def autocorrelation(returns, lag=1):
    returns = np.asarray(returns, dtype=float)
    returns = returns[np.isfinite(returns)]

    if len(returns) <= lag:
        return 0.0

    x = returns[:-lag]
    y = returns[lag:]

    if np.std(x) == 0 or np.std(y) == 0:
        return 0.0

    return float(np.corrcoef(x, y)[0, 1])


def structure_signal(returns):
    """
    Measure weak local structure relative to stochastic variation.
    """
    returns = np.asarray(returns, dtype=float)
    returns = returns[np.isfinite(returns)]

    if len(returns) < 2:
        return 0.0

    autocorr = autocorrelation(returns)
    vol = volatility(returns)
    ent = entropy(returns)

    return float(abs(autocorr) * vol * ent)


def basic_metrics(returns):
    """
    Unified basic information metrics.
    """
    returns = np.asarray(returns, dtype=float)
    returns = returns[np.isfinite(returns)]

    return {
        "volatility": volatility(returns),
        "entropy": entropy(returns),
        "autocorrelation": autocorrelation(returns),
        "structure_signal": structure_signal(returns),
        "sample_count": int(len(returns)),
    }
