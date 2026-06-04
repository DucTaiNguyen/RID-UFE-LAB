import numpy as np

from core.data_loader import load_asset

from core.metrics import (
    log_returns,
    volatility,
    entropy
)

from core.graph import build_graph

from core.spectral import (
    laplacian,
    eigenvalues,
    spectral_gap
)

from core.curvature import (
    information_curvature
)

from core.experiment import (
    create_experiment,
    save_metrics
)

from core.report import (
    generate_report
)

from core.research import (
    save_research_result
)

prices = load_asset()

returns = log_returns(
    prices
)

vol = volatility(
    returns
)

ent = entropy(
    returns
)

random_entropy = entropy(
    np.random.normal(
        0,
        np.std(returns),
        len(returns)
    )
)

W = build_graph(
    returns[-100:]
)

L = laplacian(W)

eig = eigenvalues(L)

gap = spectral_gap(eig)

curvature = information_curvature(
    eig
)

metrics = {
    "volatility": vol,
    "entropy": ent,
    "random_entropy": random_entropy,
    "spectral_gap": gap,
    "information_curvature": curvature
}

hypothesis = (
    "Bitcoin information field exhibits "
    "non-random structure."
)

if ent < random_entropy:
    conclusion = "SUPPORTED"
else:
    conclusion = "NOT_SUPPORTED"

exp_id, path = create_experiment()

save_metrics(
    path,
    metrics
)

save_research_result(
    path,
    hypothesis,
    metrics,
    conclusion
)

generate_report(
    exp_id,
    metrics,
    f"{path}/report.md"
)

print()
print("Experiment:", exp_id)
print("Hypothesis:", hypothesis)
print("Conclusion:", conclusion)
print(metrics)
