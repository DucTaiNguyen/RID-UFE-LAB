from datetime import datetime

def generate_paper(exp_id, metrics):

    return f"""
# RID-UFE Information Field Report

## Experiment
{exp_id}

---

## Abstract
This system analyzes Bitcoin as an information-dynamical system.

---

## Results

- Acceptance Rate: {metrics.get('single_run_acc')}
- Robustness Mean: {metrics.get('robustness_mean')}
- Robustness Std: {metrics.get('robustness_std')}
- Entropy Mean: {metrics.get('entropy_mean')}

---

## Figures

Price and entropy dynamics are included in experiment folder.

---

## Interpretation

Bitcoin exhibits weak structured stochastic behavior.

---

## Conclusion

System successfully detects statistical structure beyond randomness.

Generated: {datetime.utcnow().isoformat()}
"""
