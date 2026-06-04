import numpy as np
import warnings

from core.safe import safe_run
from core.datasets import get_datasets
from core.multidataset import evaluate_all

from core.experiment import create_experiment, save_metrics
from core.research import save_research_result
from core.paper import generate_paper


warnings.filterwarnings("ignore")
np.seterr(all="ignore")


def pipeline():

    datasets = get_datasets()

    results = evaluate_all(datasets)

    # =========================
    # SCIENTIFIC INTERPRETATION
    # =========================
    signal_strength = {
        k: v for k, v in results.items() if v > 0.5
    }

    noise_level = results["NOISE"]

    metrics = {
        "dataset_results": results,
        "signal_strength": signal_strength,
        "noise_baseline": noise_level
    }

    exp_id, path = create_experiment()

    save_metrics(path, metrics)

    save_research_result(
        path,
        "Cross-market information field structure analysis",
        metrics,
        "EVALUATED"
    )

    paper = generate_paper(exp_id, metrics, [])

    with open(f"{path}/paper.md", "w") as f:
        f.write(paper)

    print("Experiment:", exp_id)
    print("Results:", results)


if __name__ == "__main__":
    safe_run(pipeline)
