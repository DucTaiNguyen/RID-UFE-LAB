import numpy as np
import warnings

from core.safe import safe_run
from core.data_loader import load_asset
from core.metrics import log_returns
from core.loop import run_loop
from core.robustness import run_robustness
from core.experiment import create_experiment, save_metrics
from core.paper import generate_paper

warnings.filterwarnings("ignore")


def pipeline():

    prices = load_asset().flatten()
    returns = log_returns(prices)

    history = run_loop(returns, iterations=6)

    acc = sum(h["accepted"] for h in history) / len(history)
    robustness = run_robustness(returns, runs=6)

    metrics = {
        "accuracy": acc,
        "robustness_mean": robustness["mean"],
        "robustness_std": robustness["std"]
    }

    exp_id, path = create_experiment()
    save_metrics(path, metrics)

    paper = generate_paper(exp_id, metrics, prices)

    with open(f"{path}/paper.md", "w") as f:
        f.write(paper)

    print("Experiment:", exp_id)
    print("Price latest:", prices[-1])
    print("System updated paper with dynamics")

if __name__ == "__main__":
    safe_run(pipeline)
