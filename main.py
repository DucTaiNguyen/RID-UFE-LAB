import numpy as np
import json
import warnings

from core.safe import safe_run
from core.data_loader import load_asset
from core.metrics import log_returns
from core.loop import run_loop
from core.robustness import run_robustness
from core.experiment import create_experiment, save_metrics
from core.paper import generate_paper

warnings.filterwarnings("ignore")


def load_memory():
    try:
        return json.load(open("memory.json"))
    except:
        return []


def save_memory(m):
    mem = load_memory()
    mem.append(m)
    json.dump(mem, open("memory.json", "w"), indent=4)


def pipeline():

    prices = load_asset().flatten()
    returns = log_returns(prices)

    history = run_loop(returns, iterations=6)

    acc = sum(h["accepted"] for h in history) / len(history)
    robustness = run_robustness(returns, runs=6)

    metrics = {
        "accuracy": acc,
        "robustness_mean": robustness["mean"]
    }

    exp_id, path = create_experiment()
    save_metrics(path, metrics)

    save_memory({"metrics": metrics})

    paper = generate_paper(exp_id, metrics, prices)

    with open(f"{path}/paper.md", "w") as f:
        f.write(paper)

    print("Experiment:", exp_id)
    print("Accuracy:", acc)
    print("Robustness:", robustness["mean"])


if __name__ == "__main__":
    safe_run(pipeline)
