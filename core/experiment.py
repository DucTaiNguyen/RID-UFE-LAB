import json
import os
from datetime import datetime

EXPERIMENT_DIR = "experiments"

def create_experiment():

    os.makedirs(
        EXPERIMENT_DIR,
        exist_ok=True
    )

    exp_id = datetime.utcnow().strftime(
        "EXP-%Y%m%d-%H%M%S"
    )

    path = os.path.join(
        EXPERIMENT_DIR,
        exp_id
    )

    os.makedirs(path)

    return exp_id, path

def save_metrics(path, metrics):

    with open(
        os.path.join(
            path,
            "metrics.json"
        ),
        "w"
    ) as f:

        json.dump(
            metrics,
            f,
            indent=2
        )
