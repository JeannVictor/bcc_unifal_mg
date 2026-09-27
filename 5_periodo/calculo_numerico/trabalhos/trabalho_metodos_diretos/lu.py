# ==================================================================================
# lu.py
# ==================================================================================
# Plano de Investigação Computacional
# Sistemas de Equações Lineares: Métodos Diretos em Python
# ==================================================================================
# Disciplina: Cálculo Numérico
# Professora: Angela Leite Moreno
# Aluno 1: Jeann Victor Batista  R.A = 2024.1.08.014 
# ==================================================================================
import numpy as np

def fatoracao_lu(A):
    """Fatoração de Doolittle: A = LU sem pivoteamento.
    Retorna (L, U)."""
    A = np.array(A, dtype=float)
    n = A.shape[0]
    L = np.eye(n)
    U = np.zeros((n, n))

    for k in range(n):
        # Linha k de U
        for j in range(k, n):
            U[k, j] = A[k, j] - L[k, :k] @ U[:k, j]
        # Coluna k de L
        for i in range(k + 1, n):
            L[i, k] = (A[i, k] - L[i, :k] @ U[:k, k]) / U[k, k]

    return L, U


def subst_prog(L, b):
    """Substituição progressiva: resolve Ly = b."""
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - L[i, :i] @ y[:i]
    return y


def subst_retro(U, y):
    """Substituição retroativa: resolve Ux = y."""
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i+1:] @ x[i+1:]) / U[i, i]
    return x


def resolver_lu(A, b):
    """Resolve Ax = b via fatoração LU."""
    L, U = fatoracao_lu(A)
    y = subst_prog(L, b)
    x = subst_retro(U, y)
    return x, L, U