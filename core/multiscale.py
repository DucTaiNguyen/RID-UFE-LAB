import numpy as np

from core.graph import build_graph
from core.spectral import laplacian, eigenvalues
from core.curvature import information_curvature


def multiscale_curvature(series, scales=[20, 40, 80]):

    results = {}

    for s in scales:

        vals = []

        for i in range(s, len(series)):

            window = series[i-s:i]

            W = build_graph(window)
            L = laplacian(W)
            eig = eigenvalues(L)

            vals.append(information_curvature(eig))

        results[f"scale_{s}"] = np.array(vals)

    return results
