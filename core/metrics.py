import numpy as np

def log_returns(prices):
    prices = np.asarray(prices, dtype=float)
    return np.diff(np.log(prices))


def structure_signal(returns):
    """
    measure if market is structured or noise-like
    """

    if len(returns) < 2:
        return 0.0

    autocorr = np.corrcoef(returns[:-1], returns[1:])[0,1]

    volatility = np.std(returns)

    entropy_proxy = -np.sum(
        (returns**2) / (np.sum(returns**2) + 1e-9)
    )

    signal = abs(autocorr) * volatility * abs(entropy_proxy)

    return float(signal)
