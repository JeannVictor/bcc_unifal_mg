# =============================================================================
# integracao.py
# =============================================================================
# Regras de Integração Numérica - Newton-Cotes e Gauss-Legendre
# Disciplina: Cálculo Numérico
# =============================================================================

import numpy as np
from numpy.polynomial.legendre import leggauss


# =============================================================================
# Regras de Newton-Cotes
# =============================================================================

def ponto_medio(f, a, b, n):
    """
    Regra do Ponto Médio composta.
    Erro O(h^2).
    
    Parâmetros:
        f: função a ser integrada
        a, b: limites de integração
        n: número de subintervalos
    
    Retorna:
        Aproximação da integral
    """
    h = (b - a) / n
    xi = np.linspace(a + h/2, b - h/2, n)
    return h * np.sum(f(xi))


def trapezios(f, a, b, n):
    """
    Regra dos Trapézios composta.
    Erro O(h^2).
    Coeficientes: 1, 2, 2, ..., 2, 1.
    
    Parâmetros:
        f: função a ser integrada
        a, b: limites de integração
        n: número de subintervalos
    
    Retorna:
        Aproximação da integral
    """
    xi = np.linspace(a, b, n + 1)
    fi = f(xi)
    h = (b - a) / n
    return h / 2 * (fi[0] + 2 * np.sum(fi[1:-1]) + fi[-1])


def simpson13(f, a, b, n):
    """
    Regra de Simpson 1/3 composta.
    Erro O(h^4). n deve ser par.
    Coeficientes: 1, 4, 2, 4, ..., 4, 1.
    
    Parâmetros:
        f: função a ser integrada
        a, b: limites de integração
        n: número de subintervalos (deve ser par)
    
    Retorna:
        Aproximação da integral
    """
    if n % 2 != 0:
        raise ValueError("n deve ser par para Simpson 1/3")
    
    xi = np.linspace(a, b, n + 1)
    fi = f(xi)
    h = (b - a) / n
    
    return h / 3 * (fi[0] + 4 * np.sum(fi[1:-1:2]) + 2 * np.sum(fi[2:-2:2]) + fi[-1])


def trapezios_tabela(xi, fi):
    """
    Trapézios para dados tabelados.
    O espaçamento não precisa ser uniforme.
    
    Parâmetros:
        xi: array com coordenadas x
        fi: array com valores f(xi)
    
    Retorna:
        Aproximação da integral
    """
    xi, fi = np.asarray(xi, dtype=float), np.asarray(fi, dtype=float)
    return np.sum((fi[:-1] + fi[1:]) * np.diff(xi) / 2)


def simpson13_tabela(xi, fi):
    """
    Simpson 1/3 para dados tabelados.
    O número de subintervalos deve ser par.
    
    Parâmetros:
        xi: array com coordenadas x (espaçamento uniforme)
        fi: array com valores f(xi)
    
    Retorna:
        Aproximação da integral
    """
    n = len(fi) - 1
    if n % 2 != 0:
        raise ValueError("n deve ser par para Simpson 1/3")
    
    h = (xi[-1] - xi[0]) / n
    
    return h / 3 * (fi[0] + 4 * np.sum(fi[1:-1:2]) + 2 * np.sum(fi[2:-2:2]) + fi[-1])


# =============================================================================
# Cotas de erro
# =============================================================================

def cota_trapezio(f2max, a, b, n):
    """
    Cota superior do erro dos Trapézios compostos.
    
    Parâmetros:
        f2max: máximo de |f''(x)| no intervalo [a, b]
        a, b: limites de integração
        n: número de subintervalos
    
    Retorna:
        Cota superior do erro
    """
    return f2max * (b - a)**3 / (12 * n**2)


def cota_simpson(f4max, a, b, n):
    """
    Cota superior do erro de Simpson 1/3 composto.
    
    Parâmetros:
        f4max: máximo de |f^(4)(x)| no intervalo [a, b]
        a, b: limites de integração
        n: número de subintervalos (deve ser par)
    
    Retorna:
        Cota superior do erro
    """
    return f4max * (b - a)**5 / (180 * n**4)


# =============================================================================
# Quadratura Gaussiana
# =============================================================================

def gauss_legendre(f, a, b, n):
    """
    Quadratura de Gauss-Legendre com n pontos.
    Exata para polinômios de grau <= 2n-1.
    
    Parâmetros:
        f: função a ser integrada
        a, b: limites de integração
        n: número de pontos de quadratura
    
    Retorna:
        Aproximação da integral
    """
    t, A = leggauss(n)  # nós e pesos em [-1, 1]
    x = (b - a) / 2 * t + (b + a) / 2  # transformação para [a, b]
    return (b - a) / 2 * np.sum(A * f(x))


# =============================================================================
# Função auxiliar para tabelas comparativas
# =============================================================================

def tabela_comparativa(f, a, b, exato, ns_nc, ns_gauss):
    """
    Gera tabela comparando Newton-Cotes e Gauss-Legendre.
    
    Parâmetros:
        f: função a ser integrada
        a, b: limites de integração
        exato: valor exato da integral
        ns_nc: lista de n para Trapézios e Simpson
        ns_gauss: lista de n para Gauss-Legendre
    """
    print(f"{'Método':25s} {'n':>5s} {'Resultado':>14s} {'Erro':>12s}")
    print("-" * 60)
    
    for n in ns_nc:
        T = trapezios(f, a, b, n)
        print(f"{'Trapézios':25s} {n:>5d} {T:>14.8f} {abs(T - exato):>12.2e}")
    
    for n in ns_nc:
        if n % 2 == 0:
            S = simpson13(f, a, b, n)
            print(f"{'Simpson 1/3':25s} {n:>5d} {S:>14.8f} {abs(S - exato):>12.2e}")
    
    for n in ns_gauss:
        G = gauss_legendre(f, a, b, n)
        print(f"{'Gauss-Legendre':25s} {n:>5d} {G:>14.8f} {abs(G - exato):>12.2e}")