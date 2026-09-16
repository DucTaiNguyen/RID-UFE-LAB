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
    x = _validate_series(x)

    if order < 2:
        raise ValueError("order must be >= 2")

    if delay < 1:
        raise ValueError("delay must be >= 1")

    n = len(x) - delay * (order - 1)

    if n < 20:
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


def shannon_entropy(values):
    counts = {}

    for value in values:
        counts[value] = counts.get(value, 0) + 1

    total = len(values)

    entropy = 0.0

    for count in counts.values():
        p = count / total
        entropy -= p * math.log(p)

    return float(entropy)


def conditional_entropy(symbols):
    """
    H(S_t | S_{t-1})
    """
    if len(symbols) < 3:
        raise ValueError("Insufficient symbolic samples.")

    previous = symbols[:-1]
    current = symbols[1:]

    pairs = list(zip(previous, current))

    h_previous = shannon_entropy(previous)
    h_pairs = shannon_entropy(pairs)

    return float(h_pairs - h_previous)


def normalized_conditional_entropy(
    x,
    order=3,
    delay=1,
):
    symbols = ordinal_symbols(
        x,
        order=order,
        delay=delay,
    )

    h_cond = conditional_entropy(symbols)

    max_entropy = math.log(math.factorial(order))

    return float(
        h_cond / max_entropy
    )


def conditional_entropy_null(
    x,
    trials=10000,
    order=3,
    delay=1,
    seed=42,
):
    """
    Null model:
    preserve the marginal ordinal-symbol distribution,
    destroy temporal adjacency.
    """
    x = _validate_series(x)

    rng = np.random.default_rng(seed)

    symbols = ordinal_symbols(
        x,
        order=order,
        delay=delay,
    )

    observed = normalized_conditional_entropy(
        x,
        order=order,
        delay=delay,
    )

    null = np.empty(
        trials,
        dtype=float,
    )

    for i in range(trials):
        shuffled = [
            symbols[j]
            for j in rng.permutation(
                len(symbols)
            )
        ]

        h_cond = conditional_entropy(
            shuffled
        )

        max_entropy = math.log(
            math.factorial(order)
        )

        null[i] = (
            h_cond / max_entropy
        )

    null_mean = float(
        np.mean(null)
    )

    null_std = float(
        np.std(
            null,
            ddof=1,
        )
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
                np.abs(
                    null - null_mean
                )
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
        "seed": seed,
        "symbol_count": len(symbols),
    }


if __name__ == "__main__":
    from core.data_loader import load_asset
    from core.metrics import log_returns

    prices = load_asset()
    returns = log_returns(prices)

    print("=== CONDITIONAL ENTROPY V2 ===")

    result = conditional_entropy_null(
        returns,
        trials=10000,
        order=3,
        delay=1,
        seed=42,
    )

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        )
    )
