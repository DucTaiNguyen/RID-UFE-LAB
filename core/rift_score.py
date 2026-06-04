from core.metrics import log_returns, volatility, entropy, information_ratio

def compute_rift(prices):

    r = log_returns(prices)

    return {
        "volatility": volatility(r),
        "entropy": entropy(r),
        "information_ratio": information_ratio(r),
        "rift_score": entropy(r) / (volatility(r) + 1e-8)
    }
