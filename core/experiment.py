import os
import json
from datetime import datetime
import numpy as np


# =========================
# DEEP CONVERTER (IMPORTANT)
# =========================
def to_builtin(obj):

    # numpy scalar
    if isinstance(obj, (np.integer,)):
        return int(obj)

    if isinstance(obj, (np.floating,)):
        return float(obj)

    # numpy array
    if isinstance(obj, np.ndarray):
        return obj.tolist()

    # dict
    if isinstance(obj, dict):
        return {str(k): to_builtin(v) for k, v in obj.items()}

    # list / tuple
    if isinstance(obj, (list, tuple)):
        return [to_builtin(v) for v in obj]

    # fallback python types
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj

    # last resort
    return str(obj)


# =========================
# EXPERIMENT CREATOR
# =========================
def create_experiment():

    exp_id = "EXP-" + datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    path = f"experiments/{exp_id}"

    os.makedirs(path, exist_ok=True)

    return exp_id, path


# =========================
# SAFE SAVE
# =========================
def save_metrics(path, metrics):

    safe_metrics = to_builtin(metrics)

    with open(f"{path}/metrics.json", "w") as f:
        json.dump(safe_metrics, f, indent=4)


def save_research_result(path, hypothesis, metrics, conclusion):

    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "hypothesis": hypothesis,
        "metrics": to_builtin(metrics),
        "conclusion": conclusion
    }

    with open(f"{path}/research.json", "w") as f:
        json.dump(data, f, indent=4)
