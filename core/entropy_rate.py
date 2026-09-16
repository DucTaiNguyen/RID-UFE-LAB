import json
import math
import numpy as np


def _validate_series(x, min_length=50):
    x = np.asarray(x, dtype=float)

    if x.ndim != 1:
        raise ValueError("Input series must be one-dimensional.")

    x = x[np.isfinite(x)]

    if len(x) < min_length:
        raise ValueError(
            f"Insufficient samples: {len(x)} < {min_length}"
        )

    if np.std(x) == 0:
        raise ValueError("Series is constant.")

    return x


def ordinal_symbols(x, order=3, delay=1):
    """
    Convert a continuous time series into immutable ordinal-pattern symbols.
    """
    x = _validate_series(x)

    if order < 2:
        raise ValueError("order must be >= 2")

    if delay < 1:
        raise ValueError("delay must be >= 1")

    n = len(x) - delay * (order - 1)

    if n < 10:
        raise ValueError("Insufficient samples.")

    symbols = []

    for i in range(n):
        window = x[
            i : i + delay * order : delay
        ]

        pattern = tuple(
            int(v)
            for v in np.argsort(
                window,
                kind="mergesort",
            )
        )

        symbols.append(pattern)

    return symbols


def block_entropy(symbols, block_length):
    """
    Shannon entropy of consecutive symbolic blocks.
    """
    if block_length < 1:
        raise ValueError("block_length must be >= 1")

    if len(symbols) < block_length:
        raise ValueError("Insufficient symbols.")

    counts = {}

    for i in range(len(symbols) - block_length + 1):
        block = tuple(
            symbols[i:i + block_length]
        )

        counts[block] = counts.get(block, 0) + 1

    total = sum(counts.values())

    entropy = 0.0

    for count in counts.values():
        p = count / total
        entropy -= p * math.log(p)

    return float(entropy)


def entropy_rate(
    x,
    order=3,
    delay=1,
    max_block_length=4,
):
    """
    Estimate symbolic entropy rate.

    h_k = H(k) - H(k-1)
    """
    symbols = ordinal_symbols(
        x,
        order=order,
        delay=delay,
    )

    entropies = []

    for k in range(1, max_block_length + 1):
        H = block_entropy(symbols, k)
        entropies.append(H)

    rates = [
        entropies[i] - entropies[i - 1]
        for i in range(1, len(entropies))
    ]

    return {
        "block_entropies": entropies,
        "entropy_rates": rates,
        "estimate": float(rates[-1]),
        "order": order,
        "delay": delay,
        "max_block_length": max_block_length,
        "symbol_count": len(symbols),
    }


def entropy_rate_null(
    x,
    trials=1000,
    order=3,
    delay=1,
    max_block_length=4,
    seed=42,
):
    """
    Temporal null model.

    The ordinal-symbol marginal distribution is preserved,
    while temporal ordering is destroyed.
    """
    x = _validate_series(x)

    rng = np.random.default_rng(seed)

    observed_result = entropy_rate(
        x,
        order=order,
        delay=delay,
        max_block_length=max_block_length,
    )

    observed = observed_result["estimate"]

    symbols = ordinal_symbols(
        x,
        order=order,
        delay=delay,
    )

    null = np.empty(trials, dtype=float)

    for i in range(trials):
        permutation = rng.permutation(
            len(symbols)
        )

        shuffled = [
            symbols[j]
            for j in permutation
        ]

        entropies = []

        for k in range(1, max_block_length + 1):
            H = block_entropy(
                shuffled,
                k,
            )
            entropies.append(H)

        null[i] = (
            entropies[-1]
            - entropies[-2]
        )

    null_mean = float(np.mean(null))
    null_std = float(
        np.std(null, ddof=1)
    )

    effect_size = float(
        observed - null_mean
    )

    z_score = float(
        effect_size /
        (null_std + 1e-12)
    )

    p_value = float(
        (
            np.sum(
                np.abs(null - null_mean)
                >= abs(effect_size)
            )
            + 1
        )
        / (trials + 1)
    )

    return {
        "observed": float(observed),
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size": effect_size,
        "z_score": z_score,
        "p_value_two_sided": p_value,
        "trials": trials,
        "order": order,
        "delay": delay,
        "max_block_length": max_block_length,
        "seed": seed,
        "observed_details": observed_result,
    }


if __name__ == "__main__":
    from core.data_loader import load_asset
    from core.metrics import log_returns

    prices = load_asset()
    returns = log_returns(prices)

    print("=== ENTROPY RATE V1 ===")

    result = entropy_rate_null(
        returns,
        trials=1000,
        order=3,
        delay=1,
        max_block_length=4,
        seed=42,
    )

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        )
    )
