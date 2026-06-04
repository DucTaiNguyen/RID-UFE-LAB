import numpy as np

def laplacian(W):
    D = np.diag(np.sum(W, axis=1))
    return D - W


def eigenvalues(L):
    return np.linalg.eigvalsh(L)


def spectral_gap(eig):
    eig = np.sort(eig)
    return float(eig[1] - eig[0])
