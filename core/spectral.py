from __future__ import annotations

import numpy as np


def laplacian(W) -> np.ndarray:
    """
    Construct the graph Laplacian L = D - W.
    """

    W = np.asarray(W, dtype=float)

    if W.ndim != 2:
        raise ValueError(
            "Adjacency matrix must be two-dimensional."
        )

    if W.shape[0] != W.shape[1]:
        raise ValueError(
            "Adjacency matrix must be square."
        )

    if W.shape[0] < 2:
        raise ValueError(
            "At least two graph nodes are required."
        )

    if not np.all(np.isfinite(W)):
        raise ValueError(
            "Adjacency matrix contains non-finite values."
        )

    # Remove numerical asymmetry.
    W = 0.5 * (W + W.T)

    # No self-loops.
    W = W.copy()
    np.fill_diagonal(W, 0.0)

    degree = np.sum(W, axis=1)

    D = np.diag(degree)

    L = D - W

    if not np.all(np.isfinite(L)):
        raise ValueError(
            "Laplacian contains non-finite values."
        )

    return L


def eigenvalues(L) -> np.ndarray:
    """
    Return sorted eigenvalues of a symmetric Laplacian.
    """

    L = np.asarray(L, dtype=float)

    if L.ndim != 2:
        raise ValueError(
            "Laplacian must be two-dimensional."
        )

    if L.shape[0] != L.shape[1]:
        raise ValueError(
            "Laplacian must be square."
        )

    if L.shape[0] < 2:
        raise ValueError(
            "At least two eigenvalues are required."
        )

    if not np.all(np.isfinite(L)):
        raise ValueError(
            "Laplacian contains non-finite values."
        )

    L = 0.5 * (L + L.T)

    eig = np.linalg.eigvalsh(L)

    eig = np.real(eig)
    eig.sort()

    if not np.all(np.isfinite(eig)):
        raise ValueError(
            "Eigenvalue computation produced non-finite values."
        )

    return eig


def spectral_gap(eig) -> float:
    """
    Spectral gap = lambda_1 - lambda_0.
    """

    eig = np.asarray(eig, dtype=float).reshape(-1)

    eig = eig[np.isfinite(eig)]

    if len(eig) < 2:
        raise ValueError(
            "At least two eigenvalues are required "
            "to compute the spectral gap."
        )

    eig = np.sort(eig)

    gap = float(eig[1] - eig[0])

    if not np.isfinite(gap):
        raise ValueError(
            "Spectral gap is non-finite."
        )

    # Small negative values can arise from floating-point error.
    if gap < 0 and abs(gap) < 1e-12:
        gap = 0.0

    if gap < 0:
        raise ValueError(
            f"Invalid negative spectral gap: {gap}"
        )

    return gap
