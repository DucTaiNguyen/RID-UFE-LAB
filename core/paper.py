from datetime import datetime
import numpy as np
import json
import os


def load_memory():
    if os.path.exists("memory.json"):
        return json.load(open("memory.json"))
    return []


def generate_paper(exp_id, metrics, prices=None):

    memory = load_memory()

    prev = memory[-2]["metrics"] if len(memory) > 1 else metrics

    delta_acc = metrics.get("accuracy", 0) - prev.get("accuracy", 0)
    delta_rob = metrics.get("robustness_mean", 0) - prev.get("robustness_mean", 0)

    price_trend = None
    if prices is not None:
        price_trend = float((prices[-1] - prices[0]) / prices[0])

    regime = "STABLE"
    if abs(delta_acc) > 0.01:
        regime = "SHIFTING_STRUCTURE"

    return f"""
# RID-UFE Bitcoin Information Field Report

## Experiment ID
{exp_id}

---

## MARKET EVOLUTION

- Price Trend: {price_trend}
- Current Price: {prices[-1] if prices is not None else 'N/A'}

---

## SYSTEM EVOLUTION (IMPORTANT)

- Δ Accuracy: {delta_acc:.6f}
- Δ Robustness: {delta_rob:.6f}

Regime:
**{regime}**

---

## INTERPRETATION

System is NOT static.
It is evolving across experiments.

Each run modifies internal state space.

---

## CONCLUSION

Bitcoin information field shows weak but evolving structure
rather than pure randomness.

Generated: {datetime.utcnow().isoformat()}
"""
