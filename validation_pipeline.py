import json
import numpy as np

from core.data_loader import load_asset
from core.metrics import log_returns
from core.rolling import rolling_curvature
from core.causal import future_volatility, align_series, correlation
from core.evidence import classify_evidence
from core.graph import build_graph
from core.spectral import laplacian, eigenvalues, spectral_gap


def run_validation(
    window=80,
    k=7,
    future_window=10,
    null_trials=2000,
    train_ratio=0.70,
    seed=42,
):
    prices = load_asset()

    returns = log_returns(prices)

    # Spectral validation on the terminal return window
    spectral_window = min(window, len(returns))

    if spectral_window < 3:
        raise ValueError(
            f"Insufficient data for spectral validation: {spectral_window}"
        )

    spectral_series = returns[-spectral_window:]

    W = build_graph(spectral_series)
    L = laplacian(W)
    eig = eigenvalues(L)

    lambda_0 = float(eig[0])
    lambda_1 = float(eig[1])
    spectral_gap_value = float(spectral_gap(eig))
    spectral_finite = bool(np.isfinite(eig).all())

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
            f"Insufficient aligned samples: {len(curvature)}"
        )

    real = correlation(
        curvature,
        future_vol
    )

    rng = np.random.default_rng(seed)

    n = len(future_vol)

    null = np.empty(null_trials)

    for i in range(null_trials):
        shift = int(
            rng.integers(1, n)
        )

        shifted = np.roll(
            future_vol,
            shift
        )

        null[i] = correlation(
            curvature,
            shifted
        )

    null_mean = float(
        np.mean(null)
    )

    null_std = float(
        np.std(
            null,
            ddof=1
        )
    )

    z_score = float(
        (real - null_mean)
        / (null_std + 1e-12)
    )

    p_value = float(
        (
            np.sum(
                np.abs(null) >= abs(real)
            ) + 1
        )
        / (null_trials + 1)
    )

    split = int(
        train_ratio * len(curvature)
    )

    train_curvature = curvature[:split]
    train_vol = future_vol[:split]

    test_curvature = curvature[split:]
    test_vol = future_vol[split:]

    train_association = correlation(
        train_curvature,
        train_vol
    )

    test_association = correlation(
        test_curvature,
        test_vol
    )

    evidence = classify_evidence(
        observed_association=real,
        null_p_value=p_value,
        train_association=train_association,
        test_association=test_association,
    )

    evidence.update({
        "observed_association": float(real),

        "null_mean": null_mean,

        "null_std": null_std,

        "null_z_score": z_score,

        "null_p_value_two_sided": p_value,

        "train_association": float(
            train_association
        ),

        "test_association": float(
            test_association
        ),

        "sample_count": int(
            len(curvature)
        ),

        "train_samples": int(
            len(train_curvature)
        ),

        "test_samples": int(
            len(test_curvature)
        ),

        "spectral": {
            "lambda_0": lambda_0,
            "lambda_1": lambda_1,
            "algebraic_connectivity": lambda_1,
            "spectral_gap": spectral_gap_value,
            "finite": spectral_finite,
            "window": int(spectral_window),
        },

        "spectral_gap": spectral_gap_value,

        "parameters": {
            "window": window,
            "future_offset": k,
            "future_window": future_window,
            "null_trials": null_trials,
            "train_ratio": train_ratio,
            "seed": seed,
        },
    })

    return evidence


if __name__ == "__main__":

    evidence = run_validation()

    print(
        json.dumps(
            evidence,
            indent=4
        )
    )
