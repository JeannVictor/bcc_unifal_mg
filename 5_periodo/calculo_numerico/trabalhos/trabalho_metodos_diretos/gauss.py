# ==================================================================================
# gauss.py
# ==================================================================================
# Plano de Investigação Computacional
# Sistemas de Equações Lineares: Métodos Diretos em Python
# ==================================================================================
# Disciplina: Cálculo Numérico
# Professora: Angela Leite Moreno
# Aluno 1: Jeann Victor Batista  R.A = 2024.1.08.014 
# ==================================================================================

import numpy as np

def gauss(A, b):
    """Eliminação de Gauss com pivoteamento parcial.
    Preserva o dtype original (float32 ou float64).
    Retorna (A_triangular, b_modificado).
    """
    A = np.array(A)
    b = np.array(b)
    n = len(b)

    for k in range(n - 1):
        # Pivoteamento parcial: busca maior |a_ik| abaixo da linha k
        p = np.argmax(np.abs(A[k:, k])) + k
        A[[k, p]] = A[[p, k]]
        b[[k, p]] = b[[p, k]]

        for i in range(k + 1, n):
            m = A[i, k] / A[k, k]  # multiplicador
            A[i, k:] -= m * A[k, k:]
            b[i] -= m * b[k]

    return A, b


def gauss_sem_pivoteamento(A, b):
    """Eliminação de Gauss SEM pivoteamento.
    Preserva o dtype original (float32 ou float64).
    Retorna (A_triangular, b_modificado).
    """
    A = np.array(A)
    b = np.array(b)
    n = len(b)

    for k in range(n - 1):
        for i in range(k + 1, n):
            m = A[i, k] / A[k, k]  # multiplicador
            A[i, k:] -= m * A[k, k:]
            b[i] -= m * b[k]

    return A, b


def gauss_com_deteccao_singularidade(A, b, limiar=1e-12):
    """Eliminação de Gauss com pivoteamento parcial e detecção de singularidade.
    Lança ValueError se o pivô for menor que o limiar.
    Sempre opera em float64 para máxima precisão na detecção.
    Retorna (A_triangular, b_modificado).
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)

    for k in range(n - 1):
        # Pivoteamento parcial
        p = np.argmax(np.abs(A[k:, k])) + k
        A[[k, p]] = A[[p, k]]
        b[[k, p]] = b[[p, k]]

        # Detecção de singularidade: pivô nulo ou muito pequeno
        if abs(A[k, k]) < limiar:
            raise ValueError(
                f"Sistema singular ou quase-singular: pivô na coluna {k} "
                f"é {A[k, k]:.4e} (< limiar {limiar:.4e})"
            )

        for i in range(k + 1, n):
            m = A[i, k] / A[k, k]
            A[i, k:] -= m * A[k, k:]
            b[i] -= m * b[k]

    # Verifica também o último pivô
    if abs(A[n - 1, n - 1]) < limiar:
        raise ValueError(
            f"Sistema singular ou quase-singular: pivô na coluna {n - 1} "
            f"é {A[n - 1, n - 1]:.4e} (< limiar {limiar:.4e})"
        )

    return A, b


def subst_retro(A, b):
    """Substituição retroativa para sistema triangular superior.
    Preserva o dtype de A (float32 ou float64).
    """
    n = len(b)
    x = np.zeros(n, dtype=A.dtype)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - A[i, i + 1:] @ x[i + 1:]) / A[i, i]
    return x


def resolver_gauss(A, b):
    """Pipeline completo: Gauss com pivoteamento + substituição retroativa.
    Preserva o dtype original de A e b.
    """
    Au, bu = gauss(A, b)
    return subst_retro(Au, bu)


def resolver_gauss_sem_pivoteamento(A, b):
    """Pipeline completo: Gauss SEM pivoteamento + substituição retroativa.
    Preserva o dtype original de A e b.
    """
    Au, bu = gauss_sem_pivoteamento(A, b)
    return subst_retro(Au, bu)


def resolver_gauss_singular(A, b, limiar=1e-12):
    """Pipeline com detecção de singularidade: Gauss + substituição retroativa.
    Sempre opera em float64 (detecção de singularidade requer precisão máxima).
    """
    Au, bu = gauss_com_deteccao_singularidade(A, b, limiar)
    return subst_retro(Au, bu)