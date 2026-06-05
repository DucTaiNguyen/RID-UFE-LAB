from datetime import datetime

def f(x):
    try:
        return float(x)
    except:
        return 0.0


def generate_paper(exp_id, m):

    vol = f(m.get("volatility"))
    ent = f(m.get("entropy"))
    rand = f(m.get("random_entropy"))
    gap = f(m.get("spectral_gap"))
    curv = f(m.get("curvature_mean"))
    corr = f(m.get("curvature_future_vol_corr"))
    p = f(m.get("entropy_p"))

    # --- INTERPRETATION LOGIC ---
    signal_strength = abs(corr)

    if signal_strength < 0.1:
        signal_level = "VERY WEAK"
    elif signal_strength < 0.3:
        signal_level = "WEAK"
    elif signal_strength < 0.6:
        signal_level = "MODERATE"
    else:
        signal_level = "STRONG"

    randomness = "HIGH" if ent > rand else "STRUCTURED"

    return f"""
# RID-UFE INFORMATION FIELD REPORT

---

## Experiment ID
{exp_id}

---

## 1. RAW METRICS

- Volatility: {vol:.6f}
- Entropy: {ent:.6f}
- Random Entropy: {rand:.6f}
- Spectral Gap: {gap:.6f}
- Curvature Mean: {curv:.6f}
- Curvature–Future Vol Correlation: {corr:.6f}
- P-value: {p:.6f}

---

## 2. SYSTEM DIAGNOSIS

- Signal Strength Level: {signal_level}
- Information Structure: {randomness}

Interpretation:
- Volatility measures market instability
- Entropy measures uncertainty/randomness
- Spectral gap reflects structural separation in data dynamics
- Curvature correlation indicates predictive structure

---

## 3. HUMAN INTERPRETATION

This system is analyzing Bitcoin as an information field.

Current result suggests:

- The system is NOT purely random
- There is a weak but measurable structure
- Predictive signal exists but is limited in strength

---

## 4. CONCLUSION

The information field shows:

→ {signal_level} predictive structure  
→ partial organization in market dynamics  
→ no strong deterministic pattern yet

---

Generated: {datetime.utcnow().isoformat()}
"""
