import json
import math
import numpy as np

from core.data_loader import load_asset
from core.metrics import log_returns
from core.conditional_entropy import (
    ordinal_symbols,
    conditional_entropy,
)


def normalized_conditional_entropy_from_symbols(
    symbols,
    order,
):
    h = conditional_entropy(symbols)
    max_entropy = np.log(math.factorial(order))
    return float(h / max_entropy)


def circular_shift(x, shift):
    return np.roll(x, shift)


def run(
    trials=10000,
    order=3,
    delay=1,
    seed=42,
):
    prices = load_asset()
    returns = log_returns(prices)

    observed_symbols = ordinal_symbols(
        returns,
        order=order,
        delay=delay,
    )

    observed = (
        conditional_entropy(
            observed_symbols
        )
        / np.log(math.factorial(order))
    )

    rng = np.random.default_rng(seed)

    null = np.empty(
        trials,
        dtype=float,
    )

    n = len(returns)

    for i in range(trials):
        shift = int(
            rng.integers(
                1,
                n,
            )
        )

        surrogate = circular_shift(
            returns,
            shift,
        )

        symbols = ordinal_symbols(
            surrogate,
            order=order,
            delay=delay,
        )

        null[i] = (
            conditional_entropy(symbols)
            / np.log(math.factorial(order))
        )

    null_mean = float(np.mean(null))
    null_std = float(
        np.std(
            null,
            ddof=1,
        )
    )

    effect = float(
        observed - null_mean
    )

    z = float(
        effect /
        (null_std + 1e-12)
    )

    p = float(
        (
            np.sum(
                np.abs(
                    null - null_mean
                )
                >= abs(effect)
            )
            + 1
        )
        /
        (trials + 1)
    )

    result = {
        "observed": float(observed),
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size": effect,
        "z_score": z,
        "p_value_two_sided": p,
        "trials": trials,
        "order": order,
        "delay": delay,
        "seed": seed,
        "return_samples": len(returns),
        "symbol_count": len(observed_symbols),
        "null_model": "circular_shift_raw_returns",
    }

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    run()
