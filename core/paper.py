from datetime import datetime

def generate_paper(exp_id, metrics, history):

    acc = metrics.get("acceptance_rate", 0.0)

    best = max(
        [h["result"].get("best_corr", 0) for h in history],
        default=0.0
    )

    text = f"""
# RID-UFE Autonomous Research Report

## Experiment
{exp_id}

## Abstract
This report analyzes information dynamics in financial time series using graph-based curvature and multi-scale spectral methods.

## Results
- Acceptance Rate: {acc}
- Best Correlation: {best}

## Method
- Curvature extraction
- Spectral graph analysis
- Null model statistical testing

## Conclusion
The system {'detects non-trivial structure' if acc > 0.5 else 'does not detect statistically significant structure'}.

Generated: {datetime.utcnow().isoformat()}
"""

    return text
