import numpy as np
from scipy.stats import ortho_group

def cg(A, b, x0=None, tol=1e-8, max_iter=1000):
    """
    Gradiente Conjugado para A SPD.
    Retorna (solucao, num_iteracoes, historico_residuos).
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    r = b - A @ x
    p = r.copy()
    rr = np.dot(r, r)
    historico = [np.sqrt(rr)]
    
    for k in range(max_iter):
        Ap = A @ p
        alpha = rr / np.dot(p, Ap)
        x = x + alpha * p
        r = r - alpha * Ap
        rr_new = np.dot(r, r)
        historico.append(np.sqrt(rr_new))
        if np.sqrt(rr_new) < tol:
            return x, k + 1, historico
        beta = rr_new / rr
        p = r + beta * p
        rr = rr_new
    
    return x, max_iter, historico


def pcg(A, b, M_inv=None, x0=None, tol=1e-8, max_iter=1000):
    """
    Gradiente Conjugado Pre-Condicionado.
    M_inv: funcao que aplica M^{-1} a um vetor (pre-condicionador).
    Se M_inv = None, usa M = I (equivalente ao CG puro).
    Retorna (solucao, num_iteracoes, historico_residuos).
    """
    if M_inv is None:
        M_inv = lambda v: v.copy()
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    r = b - A @ x
    z = M_inv(r)
    p = z.copy()
    rz = np.dot(r, z)
    historico = [np.linalg.norm(r)]
    
    for k in range(max_iter):
        Ap = A @ p
        alpha = rz / np.dot(p, Ap)
        x = x + alpha * p
        r = r - alpha * Ap
        historico.append(np.linalg.norm(r))
        if np.linalg.norm(r) < tol:
            return x, k + 1, historico
        z = M_inv(r)
        rz_new = np.dot(r, z)
        beta = rz_new / rz
        p = z + beta * p
        rz = rz_new
    
    return x, max_iter, historico

def criar_matriz_spd_condicionamento(n, kappa):
    """
    Cria matriz SPD n x n com número de condição κ.
    
    Parâmetros:
    n: dimensão da matriz
    kappa: número de condição desejado (λ_max/λ_min)
    
    Retorna:
    A: matriz SPD com condicionamento κ
    """
    # Matriz ortogonal aleatória
    Q = ortho_group.rvs(dim=n)
    
    # Autovalores de 1 até kappa (escala log)
    lambdas = np.logspace(0, np.log10(kappa), n)
    
    # Construir matriz
    A = Q @ np.diag(lambdas) @ Q.T
    
    return A