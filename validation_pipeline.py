import json
import numpy as np

from core.data_loader import load_asset
from core.metrics import log_returns, volatility, entropy
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

    # ============================================================
    # RAW METRICS
    # ============================================================

    raw_volatility = float(
        volatility(returns)
    )

    raw_entropy = float(
        entropy(returns)
    )

    rng = np.random.default_rng(seed)

    random_returns = rng.permutation(returns)

    raw_random_entropy = float(
        entropy(random_returns)
    )

    # ============================================================
    # SPECTRAL VALIDATION
    # ============================================================

    spectral_window = min(
        window,
        len(returns)
    )

    if spectral_window < 3:
        raise ValueError(
            "Insufficient data for spectral validation: "
            f"{spectral_window}"
        )

    spectral_series = returns[
        -spectral_window:
    ]

    W = build_graph(
        spectral_series
    )

    L = laplacian(W)

    eig = eigenvalues(L)

    lambda_0 = float(eig[0])
    lambda_1 = float(eig[1])

    spectral_gap_value = float(
        spectral_gap(eig)
    )

    spectral_finite = bool(
        np.isfinite(eig).all()
    )

    # ============================================================
    # CURVATURE / FUTURE VOLATILITY
    # ============================================================

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
            "Insufficient aligned samples: "
            f"{len(curvature)}"
        )

    real = float(
        correlation(
            curvature,
            future_vol,
        )
    )

    # ============================================================
    # TIME-SERIES NULL / PERMUTATION TEST
    # ============================================================

    rng = np.random.default_rng(seed)

    n = len(future_vol)

    if n < 2:
        raise ValueError(
            "Insufficient samples for permutation test."
        )

    null = np.empty(
        null_trials,
        dtype=float,
    )

    for i in range(null_trials):
        shift = int(
            rng.integers(
                1,
                n,
            )
        )

        shifted = np.roll(
            future_vol,
            shift,
        )

        null[i] = correlation(
            curvature,
            shifted,
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

    z_score = float(
        (real - null_mean)
        / (null_std + 1e-12)
    )

    p_value = float(
        (
            np.sum(
                np.abs(null) >= abs(real)
            )
            + 1
        )
        / (null_trials + 1)
    )

    # ============================================================
    # TRAIN / TEST
    # ============================================================

    split = int(
        train_ratio
        * len(curvature)
    )

    if split < 2 or len(curvature) - split < 2:
        raise ValueError(
            "Invalid train/test split."
        )

    train_curvature = curvature[:split]
    train_vol = future_vol[:split]

    test_curvature = curvature[split:]
    test_vol = future_vol[split:]

    train_association = float(
        correlation(
            train_curvature,
            train_vol,
        )
    )

    test_association = float(
        correlation(
            test_curvature,
            test_vol,
        )
    )

    # ============================================================
    # EVIDENCE CLASSIFICATION
    # ============================================================

    evidence = classify_evidence(
        observed_association=real,
        null_p_value=p_value,
        train_association=train_association,
        test_association=test_association,
    )

    # ============================================================
    # OUTPUT
    # ============================================================

    evidence.update(
        {
            "raw_metrics": {
                "volatility": raw_volatility,
                "entropy": raw_entropy,
                "random_entropy": raw_random_entropy,
                "spectral_gap": spectral_gap_value,
                "curvature_future_vol_correlation": real,
                "permutation_p_value": p_value,
            },

            "random_entropy": raw_random_entropy,
            "observed_association": real,

            "time_series_null_supported": bool(
                p_value < 0.05
            ),

            "out_of_sample_stable": bool(
                np.sign(train_association)
                == np.sign(test_association)
                and abs(test_association) > 0.1
            ),

            "predictive_claim": (
                "ESTABLISHED"
                if (
                    p_value < 0.05
                    and np.sign(train_association)
                    == np.sign(test_association)
                    and abs(test_association) > 0.1
                )
                else "NOT_ESTABLISHED"
            ),

            "causal_claim": "NOT_ESTABLISHED",

            "null_mean": null_mean,
            "null_std": null_std,
            "null_z_score": z_score,

            "null_p_value_two_sided": p_value,

            "p_value_scientific": (
                f"{p_value:.6e}"
            ),

            "train_association":
                train_association,

            "test_association":
                test_association,

            "sample_count":
                len(curvature),

            "train_samples":
                len(train_curvature),

            "test_samples":
                len(test_curvature),

            "spectral": {
                "lambda_0": lambda_0,
                "lambda_1": lambda_1,
                "algebraic_connectivity":
                    lambda_1,
                "spectral_gap":
                    spectral_gap_value,
                "finite":
                    spectral_finite,
                "window":
                    spectral_window,
            },

            "spectral_gap":
                spectral_gap_value,

            "parameters": {
                "window": window,
                "future_offset": k,
                "future_window":
                    future_window,
                "null_trials":
                    null_trials,
                "train_ratio":
                    train_ratio,
                "seed":
                    seed,
            },
        }
    )

    return evidence


if __name__ == "__main__":
    result = run_validation()

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        )
    )
