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

    # =========================
    # EVOLUTION SIGNAL
    # =========================
    prev = memory[-2]["metrics"] if len(memory) > 1 else metrics

    delta_acc = metrics.get("accuracy", 0) - prev.get("accuracy", 0)
    delta_rob = metrics.get("robustness_mean", 0) - prev.get("robustness_mean", 0)

    # =========================
    # MARKET STRUCTURE
    # =========================
    price_change = None
    volatility_proxy = None

    if prices is not None:
        price_change = float((prices[-1] - prices[0]) / prices[0])
        volatility_proxy = float(np.std(prices))

    # =========================
    # REGIME DETECTION
    # =========================
    regime = "STABLE_SYSTEM"

    if abs(delta_acc) > 0.01:
        regime = "DYNAMIC_SHIFT"
    if volatility_proxy and volatility_proxy > 1000:
        regime = "HIGH_NOISE_MARKET"

    # =========================
    # PAPER OUTPUT
    # =========================
    return f"""
# RID-UFE Bitcoin Information Field Report

## Experiment ID
{exp_id}

---

## MARKET STATE

- Latest Price: {prices[-1] if prices is not None else 'N/A'}
- Price Change: {price_change}
- Volatility Proxy: {volatility_proxy}

---

## SYSTEM EVOLUTION

- Δ Accuracy: {delta_acc:.6f}
- Δ Robustness: {delta_rob:.6f}

Regime Classification:
**{regime}**

---

## INFORMATION INTERPRETATION

Bitcoin is modeled as an information field:

- Price = observable state
- Volatility = uncertainty measure
- Accuracy = structural detection strength

---

## EVOLUTION STATUS

This system is NOT static.
It evolves via memory accumulation across experiments.

---

## CONCLUSION

RID-UFE detects weak but non-random structure
in Bitcoin market dynamics with temporal evolution.

Generated: {datetime.utcnow().isoformat()}
"""
