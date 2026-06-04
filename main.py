from core.data_loader import load_asset
from core.metrics import log_returns, structure_signal
from core.loop import run_loop
from core.robustness import run_robustness
from core.experiment import create_experiment, save_metrics
from core.paper import generate_paper
from core.safe import safe_run

import warnings
warnings.filterwarnings("ignore")


def pipeline():

    prices = load_asset()
    returns = log_returns(prices)

    signal = structure_signal(returns)

    history = run_loop(returns, iterations=6)

    acc = sum(h["accepted"] for h in history) / len(history)
    robustness = run_robustness(returns, runs=6)

    metrics = {
        "accuracy": float(acc),
        "robustness_mean": float(robustness["mean"]),
        "structure_signal": float(signal)
    }

    exp_id, path = create_experiment()
    save_metrics(path, metrics)

    paper = generate_paper(exp_id, metrics, prices)

    with open(f"{path}/paper.md", "w") as f:
        f.write(paper)

    print("Experiment:", exp_id)
    print("Structure Signal:", signal)


if __name__ == "__main__":
    safe_run(pipeline)
