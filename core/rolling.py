import numpy as np

from core.graph import build_graph
from core.spectral import laplacian, eigenvalues
from core.curvature import information_curvature


def rolling_curvature(series, window=80):

    out = []

    for i in range(window, len(series)):

        w = series[i-window:i]

        W = build_graph(w)
        L = laplacian(W)
        eig = eigenvalues(L)

        out.append(information_curvature(eig))

    return np.array(out)
