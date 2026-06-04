import numpy as np

from core.data_loader import load_asset
from core.metrics import log_returns

from core.loop import run_loop

from core.experiment import create_experiment, save_metrics
from core.research import save_research_result


prices = load_asset()
returns = log_returns(prices)

# =========================
# AGENT LOOP
# =========================
history = run_loop(returns, iterations=8)

# =========================
# METRICS SUMMARY
# =========================
accepted = sum(h["accepted"] for h in history)

metrics = {
    "total_hypotheses": len(history),
    "accepted_hypotheses": accepted,
    "acceptance_rate": accepted / len(history)
}

# =========================
# FINAL CONCLUSION
# =========================
if metrics["acceptance_rate"] > 0.5:
    conclusion = "SELF-ORGANIZED_SIGNAL_STRUCTURE_DETECTED"
else:
    conclusion = "WEAK_EMERGENT_STRUCTURE"

# =========================
# SAVE
# =========================
exp_id, path = create_experiment()

save_metrics(path, metrics)
save_research_result(
    path,
    "Autonomous hypothesis generation in financial information field",
    metrics,
    conclusion
)

print("Experiment:", exp_id)
print("Acceptance Rate:", metrics["acceptance_rate"])
print("Conclusion:", conclusion)
print(metrics)
