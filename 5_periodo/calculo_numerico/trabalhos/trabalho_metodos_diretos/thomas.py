# ==================================================================================
# thomas.py
# ==================================================================================
# Plano de Investigação Computacional
# Sistemas de Equações Lineares: Métodos Diretos em Python
# ==================================================================================
# Disciplina: Cálculo Numérico
# Professora: Angela Leite Moreno
# Aluno 1: Jeann Victor Batista  R.A = 2024.1.08.014 
# ==================================================================================

import numpy as np

def thomas(a, b, c, d):
    """Resolve sistema tridiagonal pelo Algoritmo de Thomas.

    Parâmetros
    ----------
    a : subdiagonal (comprimento n-1; a[0] = elemento (2,1))
    b : diagonal principal (comprimento n)
    c : superdiagonal (comprimento n-1; c[0] = elemento (1,2))
    d : lado direito (comprimento n)

    Retorna
    -------
    x : vetor solução (comprimento n)
    """
    n = len(b)
    # Cópias para não modificar os vetores originais
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)
    d = np.array(d, dtype=float)

    # Etapa de eliminação progressiva
    for k in range(1, n):
        m = a[k - 1] / b[k - 1]  # multiplicador
        b[k] -= m * c[k - 1]
        d[k] -= m * d[k - 1]

    # Substituição retroativa
    x = np.zeros(n)
    x[-1] = d[-1] / b[-1]
    for k in range(n - 2, -1, -1):
        x[k] = (d[k] - c[k] * x[k + 1]) / b[k]

    return x


def montar_tridiagonal(a, b, c):
    """Constrói matriz densa a partir das diagonais (para verificação)."""
    n = len(b)
    A = np.diag(b) + np.diag(a, -1) + np.diag(c, 1)
    return A