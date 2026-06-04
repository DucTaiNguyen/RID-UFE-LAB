import numpy as np

def log_returns(prices):

    prices = np.asarray(prices)

    prices = prices[prices > 0]

    returns = np.diff(np.log(prices))

    returns = returns[np.isfinite(returns)]

    return returns

def volatility(r):

    return float(np.std(r))

def entropy(r, bins=30):

    hist, _ = np.histogram(
        r,
        bins=bins,
        density=True
    )

    hist = hist[hist > 0]

    p = hist / hist.sum()

    return float(
        -np.sum(
            p * np.log(p)
        )
    )
