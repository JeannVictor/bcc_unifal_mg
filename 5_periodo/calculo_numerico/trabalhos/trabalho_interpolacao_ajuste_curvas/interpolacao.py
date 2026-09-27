import numpy as np
from scipy.interpolate import CubicSpline

def lagrange(x_pts, y_pts, x_eval):
    """
    Interpolacao de Lagrange.
    Retorna o valor interpolado em x_eval (escalar ou array).
    """
    x_pts = np.array(x_pts, dtype=float)
    y_pts = np.array(y_pts, dtype=float)
    n = len(x_pts)
    x_eval = np.atleast_1d(np.array(x_eval, dtype=float))
    result = np.zeros_like(x_eval)
    for i in range(n):
        L = np.ones_like(x_eval)
        for j in range(n):
            if j != i:
                L *= (x_eval - x_pts[j]) / (x_pts[i] - x_pts[j])
        result += y_pts[i] * L
    return result if result.size > 1 else result[0]


def diferencas_divididas(x_pts, y_pts):
    """
    Calcula a tabela de diferencas divididas de Newton.
    Retorna os coeficientes [f[x0], f[x0,x1], f[x0,x1,x2], ...].
    """
    x_pts = np.array(x_pts, dtype=float)
    y_pts = np.array(y_pts, dtype=float)
    n = len(x_pts)
    tabela = y_pts.copy()
    coefs = [tabela[0]]
    for k in range(1, n):
        tabela = (tabela[1:] - tabela[:-1]) / (x_pts[k:] - x_pts[:n-k])
        coefs.append(tabela[0])
    return np.array(coefs)


def newton(x_pts, y_pts, x_eval):
    """
    Interpolacao de Newton por diferencas divididas.
    Retorna o valor interpolado em x_eval.
    """
    x_pts = np.array(x_pts, dtype=float)
    coefs = diferencas_divididas(x_pts, y_pts)
    x_eval = np.atleast_1d(np.array(x_eval, dtype=float))
    n = len(coefs)
    result = coefs[-1] * np.ones_like(x_eval)
    for k in range(n-2, -1, -1):
        result = result * (x_eval - x_pts[k]) + coefs[k]
    return result if result.size > 1 else result[0]


def nos_chebyshev(a, b, n):
    """
    Retorna n nos de Chebyshev no intervalo [a, b].
    """
    k = np.arange(1, n + 1)
    return 0.5 * (a + b) + 0.5 * (b - a) * np.cos((2*k - 1) * np.pi / (2*n))


def spline_cubica(x_pts, y_pts, x_eval, tipo='not-a-knot'):
    """
    Spline cubica via scipy.interpolate.CubicSpline.
    tipo: 'not-a-knot', 'natural', 'clamped'
    """
    cs = CubicSpline(x_pts, y_pts, bc_type=tipo if tipo != 'not-a-knot' else 'not-a-knot')
    return cs(x_eval), cs