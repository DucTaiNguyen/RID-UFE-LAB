import random

HYPOTHESES = [
    "Curvature encodes short-term volatility regimes.",
    "Entropy dynamics correlate with market instability.",
    "Spectral gap may provide a graph-theoretic descriptor of the constructed similarity network; its relationship to liquidity structure remains an empirical hypothesis.",
    "Multi-scale curvature reveals hidden market memory.",
    "Information geometry predicts volatility clustering."
]

def generate_hypothesis():
    return random.choice(HYPOTHESES)
