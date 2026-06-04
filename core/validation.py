import numpy as np

def entropy_from_series(x):

    hist, _ = np.histogram(x, bins=30, density=True)
    hist = hist[hist > 0]

    p = hist / np.sum(hist)

    return -np.sum(p * np.log(p))


def entropy_baseline_distribution(returns, trials=200):

    ent = []

    for _ in range(trials):

        surrogate = np.random.permutation(returns)

        ent.append(entropy_from_series(surrogate))

    return np.array(ent)


def z_score(real, base):
    return (real - np.mean(base)) / (np.std(base) + 1e-12)


def p_value(real, base):
    return np.mean(base <= real)
