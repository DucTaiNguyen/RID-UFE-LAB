import random

HYPOTHESES = [
    "Curvature encodes short-term volatility regimes.",
    "Entropy dynamics correlate with market instability.",
    "Spectral gap reflects liquidity structure.",
    "Multi-scale curvature reveals hidden market memory.",
    "Information geometry predicts volatility clustering."
]

def generate_hypothesis():
    return random.choice(HYPOTHESES)
