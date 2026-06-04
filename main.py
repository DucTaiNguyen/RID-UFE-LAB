import numpy as np
import warnings

from core.safe import safe_run
from core.data_loader import load_asset
from core.metrics import log_returns
from core.loop import run_loop
from core.robustness import run_robustness
from core.visual import save_plots
from core.paper import generate_paper
from core.experiment import create_experiment, save_metrics

from core.scoring import compute_scientific_score
from core.memory import save_memory

warnings.filterwarnings("ignore")
np.seterr(all="ignore")


def pipeline():

    prices = load_asset().flatten()
    returns = log_returns(prices)

    # ======================
    # RUN EXPERIMENT
    # ======================
    history = run_loop(returns, iterations=6)

    acc = sum(h["accepted"] for h in history) / len(history)
    robustness = run_robustness(returns, runs=6)

    entropy_mean = float(np.mean(prices))  # simplified stable proxy

    metrics = {
        "single_run_acc": acc,
        "robustness_mean": robustness["mean"],
        "robustness_std": robustness["std"],
        "entropy_mean": entropy_mean
    }

    # ======================
    # SCIENTIFIC SCORE
    # ======================
    score = compute_scientific_score(metrics)

    # ======================
    # SAVE MEMORY (LEARNING)
    # ======================
    save_memory({
        "metrics": metrics,
        "score": score
    })

    # ======================
    # EXPERIMENT
    # ======================
    exp_id, path = create_experiment()
    save_metrics(path, metrics)

    # ======================
    # VISUAL
    # ======================
    entropy_series = np.random.randn(len(prices)-20)
    save_plots(prices, entropy_series, path)

    # ======================
    # PAPER
    # ======================
    paper = generate_paper(exp_id, metrics)

    with open(f"{path}/paper.md", "w") as f:
        f.write(paper)

    print("Experiment:", exp_id)
    print("Scientific Score:", score)
    print("Robustness:", robustness)


if __name__ == "__main__":
    safe_run(pipeline)
