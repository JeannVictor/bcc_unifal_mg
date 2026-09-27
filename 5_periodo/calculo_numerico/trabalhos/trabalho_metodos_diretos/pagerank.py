# ==================================================================================
# pagerank.py
# ==================================================================================
# Plano de Investigação Computacional
# Sistemas de Equações Lineares: Métodos Diretos em Python
# ==================================================================================
# Disciplina: Cálculo Numérico
# Professora: Angela Leite Moreno
# Aluno 1: Jeann Victor Batista  R.A = 2024.1.08.014 
# ==================================================================================

import numpy as np

def matriz_transicao(G):
    """
    Constrói a matriz de transição P normalizando as linhas de G.
    
    Parâmetros:
    G : matriz de adjacência (n x n) onde G[i,j] = 1 indica link de i para j
    
    Retorna:
    P : matriz estocástica (cada linha soma 1)
    """
    G = np.array(G, dtype=float)
    grau_saida = G.sum(axis=1)
    
    # Tratamento para páginas sem links de saída (dangling nodes)
    # Neste caso, conecta a todas as páginas igualmente
    for i in range(len(grau_saida)):
        if grau_saida[i] == 0:
            G[i] = 1.0
            grau_saida[i] = len(G)
    
    return G / grau_saida[:, np.newaxis]


def pagerank_system(P, alpha=0.85):
    """
    Monta o sistema linear do PageRank.
    
    Sistema: (I - alpha * P^T) pi = ((1-alpha)/n) * e
    
    Parâmetros:
    P : matriz de transição (n x n)
    alpha : fator de amortecimento (padrão 0.85)
    
    Retorna:
    A : matriz do sistema (I - alpha * P^T)
    b : vetor do lado direito
    """
    n = P.shape[0]
    A = np.eye(n) - alpha * P.T
    b = ((1 - alpha) / n) * np.ones(n)
    return A, b


def condicionamento_pagerank(P, alphas=None):
    """
    Calcula o número de condição de I - alpha*P^T para diferentes alpha.
    
    Parâmetros:
    P : matriz de transição
    alphas : lista de valores de alpha (padrão: [0.5, 0.7, 0.85, 0.95, 0.99])
    
    Retorna:
    resultados : lista de tuplas (alpha, kappa)
    """
    if alphas is None:
        alphas = [0.5, 0.7, 0.85, 0.95, 0.99]
    
    resultados = []
    for alpha in alphas:
        A, _ = pagerank_system(P, alpha)
        kappa = np.linalg.cond(A)
        resultados.append((alpha, kappa))
    
    return resultados


def page_rank(G, alpha=0.85, method='gauss'):
    """
    Calcula o PageRank para uma dada matriz de adjacência.
    
    Parâmetros:
    G : matriz de adjacência
    alpha : fator de amortecimento
    method : 'gauss', 'lu', ou 'scipy'
    
    Retorna:
    pi : vetor de ranks
    """
    from gauss import resolver_gauss
    from lu import resolver_lu
    from scipy.linalg import lu_solve, lu_factor
    
    P = matriz_transicao(G)
    A, b = pagerank_system(P, alpha)
    
    if method == 'gauss':
        return resolver_gauss(A.copy(), b.copy())
    elif method == 'lu':
        pi, _, _ = resolver_lu(A.copy(), b.copy())
        return pi
    elif method == 'scipy':
        lu_fac = lu_factor(A)
        return lu_solve(lu_fac, b)
    else:
        raise ValueError(f"Método '{method}' não reconhecido")


__all__ = [
    'matriz_transicao',
    'pagerank_system', 
    'condicionamento_pagerank',
    'page_rank'
]