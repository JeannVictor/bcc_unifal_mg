# ==================================================================================
# condicao.py
# ==================================================================================
# Plano de Investigação Computacional
# Sistemas de Equações Lineares: Métodos Diretos em Python
# ==================================================================================
# Disciplina: Cálculo Numérico
# Professora: Angela Leite Moreno
# Aluno 1: Jeann Victor Batista  R.A = 2024.1.08.014 
# ==================================================================================
import numpy as np
from scipy.linalg import hilbert  # matriz de Hilbert

def experimento_hilbert(n):
    """Resolve H_n x = b com b = H_n @ ones e mede o erro."""
    H = hilbert(n)
    x_exato = np.ones(n)
    b = H @ x_exato
    x_calc = np.linalg.solve(H, b)
    erro_rel = np.linalg.norm(x_calc - x_exato) / np.linalg.norm(x_exato)
    kappa = np.linalg.cond(H)
    return kappa, erro_rel


def perturbar_b(A, b, nivel=1e-6, n_amostras=100):
    """Aplica perturbações aleatórias a b e mede a amplificação do erro."""
    x_exato = np.linalg.solve(A, b)
    amplificacoes = []
    for _ in range(n_amostras):
        db = nivel * np.random.randn(len(b))
        x_pert = np.linalg.solve(A, b + db)
        amp = (np.linalg.norm(x_pert - x_exato) / np.linalg.norm(x_exato)) / \
              (np.linalg.norm(db) / np.linalg.norm(b))
        amplificacoes.append(amp)
    return np.array(amplificacoes)