import json
import numpy as np

from core.null_models import permutation_entropy_null


def multi_scale_temporal_robustness(
    x,
    block_sizes=(4, 8, 16, 32),
    trials=2000,
    order=3,
    delay=1,
    seed=42,
):
    """
    Multi-scale temporal null-model robustness test.

    Tests whether the observed temporal-information signal
    remains qualitatively consistent across multiple
    surrogate block sizes.
    """

    results = []

    for block_size in block_sizes:
        result = permutation_entropy_null(
            x,
            trials=trials,
            order=order,
            delay=delay,
            block_size=block_size,
            seed=seed,
        )

        result["block_size"] = block_size

        results.append(result)

    p_values = np.array(
        [r["p_value_two_sided"] for r in results],
        dtype=float,
    )

    z_scores = np.array(
        [r["z_score"] for r in results],
        dtype=float,
    )

    effects = np.array(
        [r["effect_size"] for r in results],
        dtype=float,
    )

    significant_count = int(np.sum(p_values < 0.05))

    positive_effect_count = int(np.sum(effects > 0))

    summary = {
        "scales_tested": list(block_sizes),
        "trials_per_scale": trials,
        "significant_scales_p_lt_0_05": significant_count,
        "positive_effect_scales": positive_effect_count,
        "mean_effect_size": float(np.mean(effects)),
        "std_effect_size": float(np.std(effects, ddof=1)),
        "mean_z_score": float(np.mean(z_scores)),
        "min_p_value": float(np.min(p_values)),
        "max_p_value": float(np.max(p_values)),
        "scale_robust_positive_effect": bool(
            positive_effect_count == len(block_sizes)
        ),
        "scale_robust_significance": bool(
            significant_count == len(block_sizes)
        ),
    }

    return {
        "summary": summary,
        "scales": results,
    }


if __name__ == "__main__":
    from core.data_loader import load_asset
    from core.metrics import log_returns

    prices = load_asset()
    returns = log_returns(prices)

    result = multi_scale_temporal_robustness(
        returns,
        block_sizes=(4, 8, 16, 32),
        trials=2000,
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
