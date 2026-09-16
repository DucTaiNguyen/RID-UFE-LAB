import json
import numpy as np

from core.data_loader import load_asset
from core.metrics import log_returns
from core.rolling import rolling_curvature
from core.causal import future_volatility, align_series, correlation


def corr_fast(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    x = x - np.mean(x)
    y = y - np.mean(y)

    denominator = np.sqrt(
        np.sum(x * x) *
        np.sum(y * y)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.sum(x * y) / denominator
    )


def block_shuffle(x, block_size, rng):
    x = np.asarray(x, dtype=float)

    n_blocks = len(x) // block_size

    if n_blocks < 2:
        raise ValueError(
            "Not enough blocks."
        )

    usable = n_blocks * block_size

    blocks = x[:usable].reshape(
        n_blocks,
        block_size
    )

    order = rng.permutation(
        n_blocks
    )

    shuffled = blocks[order].reshape(-1)

    if usable < len(x):
        shuffled = np.concatenate(
            [shuffled, x[usable:]]
        )

    return shuffled


def statistic(
    returns,
    window=80,
    k=7,
    future_window=10,
):
    curvature = rolling_curvature(
        returns,
        window=window
    )

    future_vol = future_volatility(
        returns,
        k=k,
        window=future_window
    )

    curvature, future_vol = align_series(
        curvature,
        future_vol
    )

    if len(curvature) < 20:
        raise ValueError(
            "Insufficient aligned samples."
        )

    return corr_fast(
        curvature,
        future_vol
    )


def to_python(obj):
    if isinstance(obj, dict):
        return {
            str(k): to_python(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [to_python(v) for v in obj]

    if isinstance(obj, tuple):
        return [to_python(v) for v in obj]

    if isinstance(obj, np.generic):
        return obj.item()

    return obj


def run_null(
    returns,
    observed,
    name,
    generator,
    trials,
    seed,
):
    rng = np.random.default_rng(seed)

    values = np.empty(
        trials,
        dtype=float
    )

    for i in range(trials):
        surrogate = generator(
            returns,
            rng
        )

        values[i] = statistic(
            surrogate
        )

    mean = float(
        np.mean(values)
    )

    std = float(
        np.std(
            values,
            ddof=1
        )
    )

    effect = float(
        observed - mean
    )

    z = float(
        effect /
        (std + 1e-12)
    )

    p = float(
        (
            np.sum(
                np.abs(
                    values - mean
                )
                >= abs(effect)
            )
            + 1
        )
        /
        (trials + 1)
    )

    return {
        "null_model": name,
        "observed": float(observed),
        "null_mean": mean,
        "null_std": std,
        "effect_size": effect,
        "z_score": z,
        "p_value_two_sided": p,
        "trials": trials,
        "seed": seed,
    }


def run(
    trials=500,
    window=80,
    k=7,
    future_window=10,
    seed=42,
):
    prices = load_asset()
    returns = log_returns(prices)

    observed = statistic(
        returns,
        window=window,
        k=k,
        future_window=future_window
    )

    results = []

    # --------------------------------------------------
    # Circular shift
    # --------------------------------------------------
    def circular(x, rng):
        shift = int(
            rng.integers(
                1,
                len(x)
            )
        )
        return np.roll(
            x,
            shift
        )

    results.append(
        run_null(
            returns,
            observed,
            "circular_shift",
            circular,
            trials,
            seed
        )
    )

    # --------------------------------------------------
    # Block shuffles
    # --------------------------------------------------
    for size in (
        8,
        16,
        32,
    ):
        def generator(
            x,
            rng,
            size=size
        ):
            return block_shuffle(
                x,
                size,
                rng
            )

        results.append(
            run_null(
                returns,
                observed,
                f"block_shuffle_{size}",
                generator,
                trials,
                seed
            )
        )

    # --------------------------------------------------
    # IID shuffle
    # --------------------------------------------------
    def iid(x, rng):
        return rng.permutation(x)

    results.append(
        run_null(
            returns,
            observed,
            "iid_shuffle",
            iid,
            trials,
            seed
        )
    )

    significant = sum(
        r["p_value_two_sided"] < 0.05
        for r in results
    )

    same_direction = sum(
        np.sign(
            r["effect_size"]
        ) ==
        np.sign(observed)
        for r in results
    )

    output = {
        "observed_association":
            observed,

        "null_models_tested":
            len(results),

        "significant_null_models_p_lt_0_05":
            significant,

        "same_direction_null_models":
            same_direction,

        "fraction_significant":
            significant / len(results),

        "fraction_same_direction":
            same_direction / len(results),

        "parameters": {
            "window": window,
            "future_offset": k,
            "future_window":
                future_window,
            "trials": trials,
            "seed": seed,
        },

        "results": results,
    }

    print(
        json.dumps(
            to_python(output),
            indent=4,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    run()
