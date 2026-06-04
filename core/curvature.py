import numpy as np

def information_curvature(eig):

    eig = np.asarray(eig)
    eig = eig - np.min(eig)

    h1 = np.sum(np.exp(-eig))
    h2 = np.sum(np.exp(-2 * eig))

    return float(np.log(h1 + 1e-12) - np.log(h2 + 1e-12))
