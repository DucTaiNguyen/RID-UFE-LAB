import json
import numpy as np

from core.data_loader import load_asset
from core.metrics import log_returns
from core.rolling import rolling_curvature
from core.causal import future_volatility, align_series, correlation


def circular_shift(x, shift):
    return np.roll(x, shift)


def block_shuffle(x, block_size, rng):
    x = np.asarray(x, dtype=float)

    n_blocks = len(x) // block_size

    if n_blocks < 2:
        raise ValueError("Not enough data for block shuffle.")

    usable = n_blocks * block_size

    blocks = x[:usable].reshape(
        n_blocks,
        block_size,
    )

    order = rng.permutation(n_blocks)

    shuffled = blocks[order].reshape(-1)

    if usable < len(x):
        shuffled = np.concatenate(
            [shuffled, x[usable:]]
        )

    return shuffled


def iid_shuffle(x, rng):
    return rng.permutation(x)


def statistic_from_returns(
    returns,
    window=80,
    k=7,
    future_window=10,
):
    curvature = rolling_curvature(
        returns,
        window=window,
    )

    future_vol = future_volatility(
        returns,
        k=k,
        window=future_window,
    )

    curvature, future_vol = align_series(
        curvature,
        future_vol,
    )

    if len(curvature) < 20:
        raise ValueError(
            "Insufficient aligned samples."
        )

    return float(
        correlation(
            curvature,
            future_vol,
        )
    )


def surrogate_test(
    returns,
    observed,
    null_name,
    generator,
    trials=2000,
    seed=42,
):
    rng = np.random.default_rng(seed)

    null = np.empty(
        trials,
        dtype=float,
    )

    for i in range(trials):
        surrogate = generator(
            returns,
            rng,
        )

        null[i] = statistic_from_returns(
            surrogate
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

    return {
        "null_model": null_name,
        "observed": float(observed),
        "null_mean": null_mean,
        "null_std": null_std,
        "effect_size": effect,
        "z_score": z,
        "p_value_two_sided": p,
        "trials": trials,
        "seed": seed,
    }


def make_circular_shift():
    def generator(x, rng):
        shift = int(
            rng.integers(
                1,
                len(x),
            )
        )
        return circular_shift(
            x,
            shift,
        )

    return generator


def make_block_shuffle(block_size):
    def generator(x, rng):
        return block_shuffle(
            x,
            block_size=block_size,
            rng=rng,
        )

    return generator


def make_iid_shuffle():
    def generator(x, rng):
        return iid_shuffle(
            x,
            rng,
        )

    return generator


def run(
    window=80,
    k=7,
    future_window=10,
    trials=2000,
    seed=42,
):
    prices = load_asset()
    returns = log_returns(prices)

    observed = statistic_from_returns(
        returns,
        window=window,
        k=k,
        future_window=future_window,
    )

    results = []

    results.append(
        surrogate_test(
            returns,
            observed,
            "circular_shift",
            make_circular_shift(),
            trials=trials,
            seed=seed,
        )
    )

    for block_size in (8, 16, 32):
        results.append(
            surrogate_test(
                returns,
                observed,
                f"block_shuffle_{block_size}",
                make_block_shuffle(block_size),
                trials=trials,
                seed=seed,
            )
        )

    results.append(
        surrogate_test(
            returns,
            observed,
            "iid_shuffle",
            make_iid_shuffle(),
            trials=trials,
            seed=seed,
        )
    )

    significant = sum(
        r["p_value_two_sided"] < 0.05
        for r in results
    )

    same_sign = sum(
        np.sign(r["effect_size"])
        == np.sign(observed)
        for r in results
    )

    output = {
        "observed_association": observed,
        "null_models_tested": len(results),
        "significant_null_models_p_lt_0_05": significant,
        "same_direction_null_models": same_sign,
        "fraction_significant":
            significant / len(results),
        "fraction_same_direction":
            same_sign / len(results),
        "parameters": {
            "window": window,
            "future_offset": k,
            "future_window": future_window,
            "trials": trials,
            "seed": seed,
        },
        "results": results,
    }

    print(
        json.dumps(
            output,
            indent=4,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    run()
