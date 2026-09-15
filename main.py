from core.data_loader import load_asset
from core.metrics import log_returns, basic_metrics
from core.loop import run_loop
from core.robustness import run_robustness
from core.experiment import create_experiment, save_metrics
from core.paper import generate_paper
from core.safe import safe_run
from core.evidence import save_evidence
from validation_pipeline import run_validation

import warnings

warnings.filterwarnings("ignore")


def pipeline():
    # 1. Load data
    prices = load_asset()

    # 2. Transform to log returns
    returns = log_returns(prices)

    # 3. Basic information metrics
    metrics = basic_metrics(returns)

    # 4. Research loop
    history = run_loop(
        returns,
        iterations=6
    )

    if history:
        metrics["acceptance_rate"] = float(
            sum(
                h["accepted"]
                for h in history
            ) / len(history)
        )
    else:
        metrics["acceptance_rate"] = None

    # 5. Robustness
    robustness = run_robustness(
        returns,
        runs=6
    )

    metrics["robustness_mean"] = float(
        robustness["mean"]
    )

    if "std" in robustness:
        metrics["robustness_std"] = float(
            robustness["std"]
        )

    # 6. Experiment registry
    exp_id, path = create_experiment()

    # 7. Save metrics
    save_metrics(
        path,
        metrics
    )

    # 8. Statistical validation
    evidence = run_validation(
        window=80,
        k=7,
        future_window=10,
        null_trials=2000,
        train_ratio=0.70,
        seed=42,
    )

    save_evidence(
        path,
        evidence
    )

    # 9. Generate research paper
    paper = generate_paper(
        exp_id,
        metrics
    )

    with open(
        f"{path}/paper.md",
        "w"
    ) as f:
        f.write(paper)

    # 10. Console output
    print("Experiment:", exp_id)
    print("Metrics:")

    for key, value in metrics.items():
        print(
            f"  {key}: {value}"
        )

    print("Evidence:")
    for key, value in evidence.items():
        print(
            f"  {key}: {value}"
        )


if __name__ == "__main__":
    safe_run(pipeline)
