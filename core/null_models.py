import numpy as np


def _validate_series(x, min_length=30):
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


def permutation_entropy(
    x,
    order=3,
    delay=1,
    normalize=True,
):
    """
    Permutation entropy of a scalar time series.

    Measures temporal ordering patterns rather than
    marginal histogram entropy.
    """
    x = _validate_series(x)

    if order < 2:
        raise ValueError("order must be >= 2")

    if delay < 1:
        raise ValueError("delay must be >= 1")

    n = len(x) - delay * (order - 1)

    if n < 10:
        raise ValueError("Insufficient samples for permutation entropy.")

    patterns = {}

    for i in range(n):
        window = x[
            i : i + delay * order : delay
        ]

        # Stable ordering handles equal values deterministically.
        pattern = tuple(np.argsort(window, kind="mergesort"))

        patterns[pattern] = patterns.get(pattern, 0) + 1

    counts = np.asarray(list(patterns.values()), dtype=float)
    probabilities = counts / counts.sum()

    entropy = -np.sum(
        probabilities * np.log(probabilities + 1e-15)
    )

    if normalize:
        import math
        max_entropy = np.log(math.factorial(order))
        entropy /= max_entropy

    return float(entropy)


def block_shuffle(x, block_size=8, rng=None):
    """
    Shuffle contiguous blocks.

    Preserves local structure inside each block while
    destroying long-range temporal ordering.
    """
    x = _validate_series(x)

    if block_size < 2:
        raise ValueError("block_size must be >= 2")

    if rng is None:
        rng = np.random.default_rng()

    n_blocks = len(x) // block_size

    if n_blocks < 2:
        raise ValueError("Not enough blocks for block shuffle.")

    usable = n_blocks * block_size

    blocks = x[:usable].reshape(n_blocks, block_size)

    order = rng.permutation(n_blocks)

    shuffled = blocks[order].reshape(-1)

    # Preserve remainder without modifying its internal order.
    if usable < len(x):
        shuffled = np.concatenate(
            [shuffled, x[usable:]]
        )

    return shuffled


def permutation_entropy_null(
    x,
    trials=1000,
    order=3,
    delay=1,
    block_size=8,
    seed=42,
):
    """
    Temporal null model using block shuffling.

    Returns observed permutation entropy,
    surrogate mean/std, z-score and empirical two-sided p-value.
    """
    x = _validate_series(x)

    rng = np.random.default_rng(seed)

    observed = permutation_entropy(
        x,
        order=order,
        delay=delay,
        normalize=True,
    )

    null = np.empty(trials, dtype=float)

    for i in range(trials):
        surrogate = block_shuffle(
            x,
            block_size=block_size,
            rng=rng,
        )

        null[i] = permutation_entropy(
            surrogate,
            order=order,
            delay=delay,
            normalize=True,
        )

    null_mean = float(np.mean(null))
    null_std = float(np.std(null, ddof=1))

    z_score = float(
        (observed - null_mean)
        / (null_std + 1e-12)
    )

    p_value = float(
        (
            np.sum(
                np.abs(null - null_mean)
                >= abs(observed - null_mean)
            )
            + 1
        )
        / (trials + 1)
    )

    effect_size = float(
        observed - null_mean
    )

    return {
        "observed": observed,
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size": effect_size,
        "z_score": z_score,
        "p_value_two_sided": p_value,
        "trials": trials,
        "order": order,
        "delay": delay,
        "block_size": block_size,
        "seed": seed,
    }
