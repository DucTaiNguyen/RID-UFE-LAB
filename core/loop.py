import numpy as np

from core.hypothesis import generate_hypothesis
from core.agent import evaluate_hypothesis
from core.validation_split import time_split
from core.null_model import null_correlation_test


def run_loop(returns, iterations=5):

    history = []

    train, test, _ = time_split(returns)

    null_dist = null_correlation_test(test)

    threshold = float(np.mean(null_dist) + 2 * np.std(null_dist))

    for _ in range(iterations):

        hyp = generate_hypothesis()

        result = evaluate_hypothesis(test)

        corr = result.get("best_corr", 0.0)

        if np.isnan(corr) or np.isinf(corr):
            corr = 0.0

        accepted = corr > threshold

        history.append({
            "hypothesis": hyp,
            "result": result,
            "accepted": accepted,
            "threshold": threshold
        })

    return history
