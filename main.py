import numpy as np
import warnings
import json
import os

from core.safe import safe_run
from core.data_loader import load_asset
from core.metrics import log_returns
from core.loop import run_loop
from core.experiment import create_experiment, save_metrics
from core.robustness import run_robustness

warnings.filterwarnings("ignore")


MEM_FILE = "memory.json"


def load_memory():
    if os.path.exists(MEM_FILE):
        return json.load(open(MEM_FILE))
    return []


def save_memory(data):
    mem = load_memory()
    mem.append(data)
    json.dump(mem, open(MEM_FILE, "w"), indent=4)


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

    # ======================
    # MEMORY COMPARISON
    # ======================
    memory = load_memory()

    prev = memory[-1]["metrics"] if memory else metrics

    delta = {
        k: metrics[k] - prev.get(k, 0)
        for k in metrics.keys()
    }

    # ======================
    # EXPERIMENT
    # ======================
    exp_id, path = create_experiment()
    save_metrics(path, metrics)

    save_memory({
        "metrics": metrics,
        "delta": delta
    })

    # ======================
    # DYNAMIC PAPER (IMPORTANT)
    # ======================
    paper = f"""
# RID-UFE Bitcoin Information Field Report

## Experiment
{exp_id}

---

## CURRENT STATE

Accuracy: {metrics['accuracy']:.6f}
Robustness: {metrics['robustness_mean']:.6f}

---

## CHANGE vs PREVIOUS RUN

Δ Accuracy: {delta['accuracy']:.6f}
Δ Robustness: {delta['robustness_mean']:.6f}

---

## INTERPRETATION

{"Stable system" if abs(delta["accuracy"]) < 0.01 else "System shifted state"}

---

## CONCLUSION

This report is NOT static.
It is generated from an evolving memory system.

Each run modifies system state.
"""

    with open(f"{path}/paper.md", "w") as f:
        f.write(paper)

    print("Experiment:", exp_id)
    print("Delta:", delta)


if __name__ == "__main__":
    safe_run(pipeline)
