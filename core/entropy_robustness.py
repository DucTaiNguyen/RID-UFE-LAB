import json

from core.data_loader import load_asset
from core.metrics import log_returns
from core.entropy_rate import entropy_rate_null


def run():
    prices = load_asset()
    returns = log_returns(prices)

    configurations = [
        (3, 1, 2),
        (3, 1, 3),
        (3, 1, 4),
        (3, 2, 2),
        (3, 2, 3),
        (3, 2, 4),
        (4, 1, 2),
        (4, 1, 3),
        (4, 1, 4),
        (4, 2, 2),
        (4, 2, 3),
        (4, 2, 4),
    ]

    results = []

    for order, delay, max_block in configurations:
        result = entropy_rate_null(
            returns,
            trials=2000,
            order=order,
            delay=delay,
            max_block_length=max_block,
            seed=42,
        )

        results.append(
            {
                "order": order,
                "delay": delay,
                "max_block_length": max_block,
                "observed": result["observed"],
                "null_mean": result["null_mean"],
                "null_std": result["null_std"],
                "effect_size": result["effect_size"],
                "z_score": result["z_score"],
                "p_value": result["p_value_two_sided"],
            }
        )

    significant = sum(
        r["p_value"] < 0.05
        for r in results
    )

    positive = sum(
        r["effect_size"] > 0
        for r in results
    )

    output = {
        "configurations_tested": len(results),
        "significant_configurations_p_lt_0_05": significant,
        "positive_effect_configurations": positive,
        "fraction_significant": significant / len(results),
        "fraction_positive": positive / len(results),
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
