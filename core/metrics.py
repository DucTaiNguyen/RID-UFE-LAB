from __future__ import annotations

import numpy as np


MIN_RETURN_SAMPLES = 20


def _clean_returns(returns) -> np.ndarray:
    x = np.asarray(returns, dtype=float).reshape(-1)
    x = x[np.isfinite(x)]

    if len(x) < MIN_RETURN_SAMPLES:
        raise ValueError(
            f"Insufficient return samples: {len(x)} "
            f"(minimum required: {MIN_RETURN_SAMPLES})."
        )

    return x


def _require_variation(x: np.ndarray, name: str) -> None:
    if len(x) < 2:
        raise ValueError(
            f"{name}: insufficient samples."
        )

    if np.std(x) == 0:
        raise ValueError(
            f"{name}: zero variance / degenerate series."
        )


def log_returns(prices) -> np.ndarray:
    prices = np.asarray(prices, dtype=float).reshape(-1)

    prices = prices[np.isfinite(prices)]

    if len(prices) < 2:
        raise ValueError(
            "At least two prices are required."
        )

    if np.any(prices <= 0):
        raise ValueError(
            "Prices must be strictly positive."
        )

    returns = np.diff(np.log(prices))

    if not np.all(np.isfinite(returns)):
        raise ValueError(
            "Computed log returns contain non-finite values."
        )

    return returns


def volatility(returns) -> float:
    x = _clean_returns(returns)
    _require_variation(x, "volatility")

    value = float(np.std(x))

    if not np.isfinite(value):
        raise ValueError(
            "Volatility is non-finite."
        )

    return value


def entropy(returns, bins: int = 20) -> float:
    x = _clean_returns(returns)

    if np.std(x) == 0:
        raise ValueError(
            "Entropy cannot be computed for a constant series."
        )

    bins = max(2, int(bins))

    hist, _ = np.histogram(
        x,
        bins=bins,
        density=False,
    )

    total = hist.sum()

    if total <= 0:
        raise ValueError(
            "Entropy histogram is empty."
        )

    probabilities = hist.astype(float) / float(total)

    probabilities = probabilities[
        probabilities > 0
    ]

    value = float(
        -np.sum(
            probabilities * np.log(probabilities)
        )
    )

    if not np.isfinite(value):
        raise ValueError(
            "Entropy is non-finite."
        )

    return value


def autocorrelation(returns, lag: int = 1) -> float:
    x = _clean_returns(returns)

    lag = int(lag)

    if lag <= 0:
        raise ValueError(
            "Lag must be positive."
        )

    if len(x) <= lag:
        raise ValueError(
            f"Insufficient samples for lag={lag}."
        )

    x1 = x[:-lag]
    x2 = x[lag:]

    _require_variation(x1, "autocorrelation input")
    _require_variation(x2, "autocorrelation shifted input")

    value = float(
        np.corrcoef(x1, x2)[0, 1]
    )

    if not np.isfinite(value):
        raise ValueError(
            "Autocorrelation is non-finite."
        )

    return value


def structure_signal(returns, lag: int = 1) -> float:
    x = _clean_returns(returns)

    ac = autocorrelation(x, lag=lag)

    return float(abs(ac))


def basic_metrics(returns) -> dict:
    x = _clean_returns(returns)

    return {
        "volatility": volatility(x),
        "entropy": entropy(x),
        "autocorrelation": autocorrelation(x),
        "structure_signal": structure_signal(x),
    }
