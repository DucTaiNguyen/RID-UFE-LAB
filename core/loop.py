import numpy as np

from core.hypothesis import generate_hypothesis
from core.agent import evaluate_hypothesis
from core.validation_split import time_split
from core.null_model import null_correlation_test


def run_loop(returns, iterations=5):

    history = []

    train, test, _ = time_split(returns)

    null_dist = null_correlation_test(test)

    threshold = np.mean(null_dist) + 2*np.std(null_dist)

    for i in range(iterations):

        hyp = generate_hypothesis()

        result = evaluate_hypothesis(test)

        accepted = result["best_corr"] > threshold

        history.append({
            "hypothesis": hyp,
            "result": result,
            "accepted": accepted,
            "threshold": float(threshold)
        })

    return history
