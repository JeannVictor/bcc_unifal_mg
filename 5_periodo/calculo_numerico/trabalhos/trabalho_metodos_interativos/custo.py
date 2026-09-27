import numpy as np
import time
from jacobi_seidel import jacobi, gauss_seidel
from sor import sor, omega_young
from gradiente_conjugado import cg

def gerar_tridiagonal(n, diag=4, sub=-1):
    """Gera matriz tridiagonal n x n."""
    A = diag * np.eye(n)
    A += np.diag([sub] * (n-1), k=1)
    A += np.diag([sub] * (n-1), k=-1)
    b = np.ones(n)
    return A, b

def medir_tempo(func, *args, repeticoes=3, **kwargs):
    """Retorna o menor tempo entre 'repeticoes' execucoes."""
    tempos = []
    for _ in range(repeticoes):
        t0 = time.perf_counter()
        func(*args, **kwargs)
        tempos.append(time.perf_counter() - t0)
    return min(tempos)