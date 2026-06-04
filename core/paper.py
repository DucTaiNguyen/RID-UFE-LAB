from datetime import datetime
import json

def generate_paper(exp_id, metrics):

    def pretty(v):
        try:
            return f"{float(v):.6f}"
        except:
            return str(v)

    return f"""
# RID-UFE Information Field Report

---

## Experiment ID
{exp_id}

---

## 1. ABSTRACT (Simple Explanation)

This system analyzes Bitcoin as an information field.

It studies whether price movements show:
- structure
- randomness
- hidden signals

---

## 2. RESULTS (Core Metrics)

- Volatility: {pretty(metrics.get('volatility'))}
- Entropy: {pretty(metrics.get('entropy'))}
- Random Entropy: {pretty(metrics.get('random_entropy'))}
- Spectral Gap: {pretty(metrics.get('spectral_gap'))}

---

## 3. INFORMATION STRUCTURE

- Curvature Mean: {pretty(metrics.get('curvature_mean'))}
- Curvature Std: {pretty(metrics.get('curvature_std'))}
- Curvature–Future Vol Correlation:
  {pretty(metrics.get('curvature_future_vol_corr'))}

---

## 4. STATISTICAL INTERPRETATION

- Entropy Z: {pretty(metrics.get('entropy_z'))}
- P-value: {pretty(metrics.get('entropy_p'))}

Interpretation:
- If p-value ≈ 1 → no strong statistical significance
- If correlation > 0 → weak predictive structure possible

---

## 5. CONCLUSION (Human-readable)

This report suggests that Bitcoin market behavior:

- shows weak but measurable structure
- is not fully random
- contains low-strength predictive signals

However, the signal strength is still limited.

---

Generated: {datetime.utcnow().isoformat()}
"""
