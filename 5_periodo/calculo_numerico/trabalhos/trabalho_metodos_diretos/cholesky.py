# ==================================================================================
# cholesky.py
# ==================================================================================
# Plano de Investigação Computacional
# Sistemas de Equações Lineares: Métodos Diretos em Python
# ==================================================================================
# Disciplina: Cálculo Numérico
# Professora: Angela Leite Moreno
# Aluno 1: Jeann Victor Batista  R.A = 2024.1.08.014 
# ==================================================================================
import numpy as np

def cholesky(A):
    """Fatoração de Cholesky: A = L @ L.T
    Requer A simétrica positiva definida (SPD).
    Lança ValueError se A não for SPD."""
    A = np.array(A, dtype=float)
    n = A.shape[0]
    L = np.zeros((n, n))

    for k in range(n):
        soma_diag = A[k, k] - np.sum(L[k, :k] ** 2)
        if soma_diag <= 0:
            raise ValueError(
                f"Matriz não SPD: elemento diagonal {k} negativo ({soma_diag:.4e})"
            )
        L[k, k] = np.sqrt(soma_diag)
        for i in range(k + 1, n):
            L[i, k] = (A[i, k] - np.sum(L[i, :k] * L[k, :k])) / L[k, k]

    return L


def resolver_cholesky(A, b):
    """Resolve Ax = b via Cholesky (A deve ser SPD)."""
    L = cholesky(A)
    # Ly = b (substituição progressiva)
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - L[i, :i] @ y[:i]) / L[i, i]
    # L^T x = y (substituição retroativa)
    x = np.zeros(n)
    Lt = L.T
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - Lt[i, i+1:] @ x[i+1:]) / Lt[i, i]
    return x, L