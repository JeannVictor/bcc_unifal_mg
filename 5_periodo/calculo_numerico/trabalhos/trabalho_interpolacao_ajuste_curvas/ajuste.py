import numpy as np
from scipy.optimize import curve_fit

def regressao_linear(x, y):
    """
    Ajuste linear y = a0 + a1*x pelo metodo dos minimos quadrados.
    Retorna (a0, a1, r_quadrado).
    """
    n = len(x)
    Sx = np.sum(x)
    Sy = np.sum(y)
    Sxx = np.sum(x**2)
    Sxy = np.sum(x * y)
    D = n * Sxx - Sx**2
    a1 = (n * Sxy - Sx * Sy) / D
    a0 = (Sy - a1 * Sx) / n
    y_hat = a0 + a1 * x
    ss_res = np.sum((y - y_hat)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return a0, a1, r2


def regressao_polinomial(x, y, grau):
    """
    Ajuste polinomial de grau 'grau' por minimos quadrados.
    Retorna coeficientes (grau crescente) e r_quadrado.
    """
    coefs = np.polyfit(x, y, grau)[::-1]  # grau crescente
    y_hat = np.polyval(coefs[::-1], x)
    ss_res = np.sum((y - y_hat)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return coefs, r2


def ajuste_exponencial(x, y):
    """
    Lineariza y = a * exp(b*x) via ln(y) = ln(a) + b*x.
    Retorna (a, b, r_quadrado_log).
    """
    ln_y = np.log(y)
    a0, a1, r2 = regressao_linear(x, ln_y)
    return np.exp(a0), a1, r2


def ajuste_potencia(x, y):
    """
    Lineariza y = a * x^b via log-log: ln(y) = ln(a) + b*ln(x).
    Retorna (a, b, r_quadrado_log).
    """
    ln_x = np.log(x)
    ln_y = np.log(y)
    a0, b, r2 = regressao_linear(ln_x, ln_y)
    return np.exp(a0), b, r2


def ajuste_nao_linear(func, x, y, p0=None):
    """
    Ajuste nao-linear generico via scipy.optimize.curve_fit.
    Retorna (params_otimos, cov_matrix).
    """
    popt, pcov = curve_fit(func, x, y, p0=p0, maxfev=10000)
    return popt, pcov


def residuos(x, y, y_hat):
    """
    Retorna vetor de residuos e estatisticas basicas.
    """
    res = y - y_hat
    return res, np.std(res), np.max(np.abs(res))