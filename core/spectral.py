import numpy as np

def laplacian(W):

    D = np.diag(
        np.sum(W, axis=1)
    )

    return D - W

def eigenvalues(L):

    vals = np.linalg.eigvalsh(L)

    return np.sort(vals)

def spectral_gap(vals):

    if len(vals) < 2:
        return 0.0

    return float(
        vals[1] - vals[0]
    )
