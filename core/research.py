import json
from datetime import datetime
import numpy as np


def to_builtin(obj):

    if isinstance(obj, (np.integer,)):
        return int(obj)

    if isinstance(obj, (np.floating,)):
        return float(obj)

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, dict):
        return {str(k): to_builtin(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [to_builtin(v) for v in obj]

    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj

    return str(obj)


def save_research_result(path, hypothesis, metrics, conclusion):

    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "hypothesis": hypothesis,
        "metrics": to_builtin(metrics),
        "conclusion": conclusion
    }

    with open(f"{path}/research.json", "w") as f:
        json.dump(data, f, indent=4)
