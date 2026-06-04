import numpy as np

def spectral_entropy(
    eigenvalues
):

    eig = np.abs(
        np.asarray(
            eigenvalues
        )
    )

    eig = eig + 1e-12

    p = eig / np.sum(eig)

    return float(
        -np.sum(
            p * np.log(p)
        )
    )

def information_curvature(
    eigenvalues
):

    return spectral_entropy(
        eigenvalues
    )
