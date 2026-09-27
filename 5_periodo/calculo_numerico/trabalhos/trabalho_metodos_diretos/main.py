# ==================================================================================
# main.py
# ==================================================================================
# Plano de Investigação Computacional
# Sistemas de Equações Lineares: Métodos Diretos em Python
# ==================================================================================
# Disciplina: Cálculo Numérico
# Professora: Angela Leite Moreno
# Aluno 1: Jeann Victor Batista  R.A = 2024.1.08.014 
# ==================================================================================
# Este script reproduz todos os resultados do relatório, incluindo:
#   - Eliminação de Gauss com pivoteamento parcial
#   - Fatoração LU (Doolittle)
#   - Fatoração de Cholesky para matrizes SPD
#   - Algoritmo de Thomas para sistemas tridiagonais
#   - Custo computacional empírico
#   - Condicionamento e sensibilidade à perturbação
#   - Projeto integrador: PageRank numérico
#   - Desafio (Opcional)
# ==================================================================================

import numpy as np
import matplotlib.pyplot as plt
import time as _time
from scipy.linalg import lu as scipy_lu

from gauss import gauss, resolver_gauss, resolver_gauss_sem_pivoteamento, resolver_gauss_singular
from lu import fatoracao_lu, resolver_lu, subst_retro, subst_prog
from cholesky import resolver_cholesky
from thomas import thomas, montar_tridiagonal
from condicao import experimento_hilbert, perturbar_b
from scipy.linalg import hilbert
from pagerank import matriz_transicao, pagerank_system, condicionamento_pagerank

# ==================================================================================
# 1. Eliminação de Gauss e Pivoteamento
# ==================================================================================

# ----------------------------------------------------------------------------------
# Q1.1 - Verificação básica
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q1.1 - Verificação básica")
print("=\n" * 60)

A = np.array([
    [3, 2,  4],
    [1, 1,  2],
    [4, 3, -2]
], dtype=float)

b = np.array([1, 2, 3], dtype=float)

x = resolver_gauss(A, b)

print(f"\nSolução encontrada x: {x}")
print(f"Resíduo ||Ax - b||_2: {np.linalg.norm(A @ x - b, 2):.4e}")

# ----------------------------------------------------------------------------------
# Q1.2 - Matriz triangular superior U após a eliminação
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q1.2 - Matriz triangular superior U")
print("=" * 60)

# .copy() garante que A e b originais não sejam alterados
U, _ = gauss(A.copy(), b.copy())

print("\nMatriz triangular superior U:")
print(U)

# ----------------------------------------------------------------------------------
# Q1.3 - Efeito do pivoteamento na precisão (float32)
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q1.3 - Efeito do pivoteamento na precisão")
print("=" * 60)

# Sistema e solução exata em float32 para simular precisão reduzida
C = np.array([[0.0003, 3],
              [1,      1]], dtype=np.float32)
c = np.array([2.0001, 1], dtype=np.float32)
x_exato = np.array([1/3, 2/3], dtype=np.float32)

# Ambas as chamadas recebem float32 e preservam o dtype internamente
x_sem = resolver_gauss_sem_pivoteamento(C, c)
x_com = resolver_gauss(C, c)

erro_sem = np.abs((x_sem - x_exato) / x_exato)
erro_com = np.abs((x_com - x_exato) / x_exato)

print("\n--- Sem pivoteamento ---")
print(f"x = {x_sem}")
print(f"Erro relativo: {erro_sem}")

print("\n--- Com pivoteamento parcial ---")
print(f"x = {x_com}")
print(f"Erro relativo: {erro_com}")

# ----------------------------------------------------------------------------------
# Q1.4 - Variando a11 (escala log-log)
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q1.4 - Erro vs. tamanho do pivô (log-log)")
print("=" * 60)

valores_a11 = [1e-1, 1e-3, 1e-6, 1e-9]
erros_sem = []
erros_com = []

x_exato = np.array([1/3, 2/3], dtype=np.float32)

for a11 in valores_a11:
    D = np.array([[a11, 3],
                  [1,   1]], dtype=np.float32)
    d = np.array([2.0001, 1], dtype=np.float32)

    # Ambos em float32 — comparação justa
    x_sem_piv = resolver_gauss_sem_pivoteamento(D, d)
    x_com_piv = resolver_gauss(D, d)

    erros_sem.append(abs((x_sem_piv[0] - x_exato[0]) / x_exato[0]))
    erros_com.append(abs((x_com_piv[0] - x_exato[0]) / x_exato[0]))

    print(f"a11={a11:.0e} | sem piv: {erros_sem[-1]:.4e} | com piv: {erros_com[-1]:.4e}")

plt.figure(figsize=(7, 4.5))
plt.loglog(valores_a11, erros_sem, 'o-', label='Sem pivoteamento')
plt.loglog(valores_a11, erros_com, 's-', label='Com pivoteamento')
plt.gca().invert_xaxis()  # pivô diminuindo da esquerda para direita
plt.xlabel('$a_{11}$')
plt.ylabel('Erro relativo em $x_1$')
plt.title('Erro vs tamanho do pivô (float32)')
plt.legend()
plt.grid(True, which='both', ls='--', alpha=0.6)
plt.tight_layout()
plt.savefig('q14_plot.png', dpi=150)
plt.show()

# ----------------------------------------------------------------------------------
# Q1.5 - Sistemas singulares e quase-singulares
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q1.5 - Sistemas singulares e quase-singulares")
print("=" * 60)

E = np.array([
    [ 1, -3,  1],
    [ 6, -18, 4],
    [-1,  3, -1]
], dtype=float)
e = np.array([1, 2, 4], dtype=float)

# Parte 1: o que acontece sem detecção
print("\n--- Sem detecção de singularidade (resolver_gauss) ---")
x = resolver_gauss(E, e)
print(f"Solução retornada: {x}")
print(f"Resíduo ||Ax - b||_2: {np.linalg.norm(E @ x - e, 2)}")

# Parte 2: com detecção explícita do pivô nulo (limiar 1e-12)
print("\n--- Com detecção de singularidade (resolver_gauss_singular) ---")
try:
    x = resolver_gauss_singular(E, e, limiar=1e-12)
    print(f"Solução encontrada: {x}")
except ValueError as err:
    print(f"Singularidade detectada: {err}")

# ==================================================================================
# 2. Fatoração LU (Doolittle)
# ==================================================================================

# ----------------------------------------------------------------------------------
# Q2.1 - Construção e verificação da fatoração LU
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q2.1 - Construção e verificação da fatoração LU")
print("=" * 60)

F = np.array([
    [ 2, 1, 1],
    [ 4,-6, 0],
    [-2, 7, 2]
], dtype=float)

L, U = fatoracao_lu(F)

print("\nMatriz L (triangular inferior):")
print(np.array2string(L, formatter={'float_kind': lambda x: f'{x:8.4f}'}))

print("\nMatriz U (triangular superior):")
print(np.array2string(U, formatter={'float_kind': lambda x: f'{x:8.4f}'}))

erro_fat = np.linalg.norm(L @ U - F, 'fro')
print(f"\nErro de fatoração ||LU - A||_F = {erro_fat:.4e}")

print(f"\nL é triangular inferior: {'Sim' if np.allclose(L, np.tril(L)) else 'Não'}")
print(f"U é triangular superior: {'Sim' if np.allclose(U, np.triu(U)) else 'Não'}")
print(f"Diagonal de L toda = 1:  {'Sim' if np.allclose(np.diag(L), 1) else 'Não'}")

# ----------------------------------------------------------------------------------
# Q2.2 - Dois lados direitos reutilizando L e U
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q2.2 - Dois lados direitos reutilizando L e U")
print("=" * 60)

F1 = np.array([1, 2, 3], dtype=float)
F2 = np.array([0, 1, -1], dtype=float)

# Fatorar A apenas uma vez
L, U = fatoracao_lu(F)

# Resolver para b1
y1 = subst_prog(L, F1)
x1 = subst_retro(U, y1)

# Resolver para b2 (reutiliza L e U)
y2 = subst_prog(L, F2)
x2 = subst_retro(U, y2)

print(f"\nSolução x1 (b1 = {F1}): {x1}")
print(f"Resíduo ||A·x1 - b1||_2 = {np.linalg.norm(F @ x1 - F1, 2):.4e}")

print(f"\nSolução x2 (b2 = {F2}): {x2}")
print(f"Resíduo ||A·x2 - b2||_2 = {np.linalg.norm(F @ x2 - F2, 2):.4e}")

# ----------------------------------------------------------------------------------
# Q2.3 - Vantagem com múltiplos lados direitos (n=200, k=50)
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q2.3 - Vantagem com múltiplos lados direitos (n=200, k=50)")
print("=" * 60)

np.random.seed(42)
n, k = 200, 50
A_rand = np.random.randn(n, n)
Bs = [np.random.randn(n) for _ in range(k)]

# (a) Gauss repetido
t0 = _time.perf_counter()
for b in Bs:
    resolver_gauss(A_rand, b)
t_gauss = _time.perf_counter() - t0

# (b) LU reutilizado
t0 = _time.perf_counter()
L_rand, U_rand = fatoracao_lu(A_rand)
for b in Bs:
    y = subst_prog(L_rand, b)
    x = subst_retro(U_rand, y)
t_lu = _time.perf_counter() - t0

fator = t_gauss / t_lu

print(f"\n{'Estratégia':<25} {'Tempo total (s)':>16} {'Tempo por sistema (ms)':>22}")
print("-" * 65)
print(f"{'Gauss repetido':<25} {t_gauss:>16.4f} {(t_gauss/k)*1000:>22.4f}")
print(f"{'LU reutilizado':<25} {t_lu:>16.4f} {(t_lu/k)*1000:>22.4f}")
print(f"\nFator de aceleração: {fator:.2f}x")

# ----------------------------------------------------------------------------------
# Q2.4 - Pivoteamento: fatoracao_lu vs scipy.linalg.lu
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q2.4 - Pivoteamento: fatoracao_lu vs scipy.linalg.lu")
print("=" * 60)

G = np.array([[0, 1],
              [2, 3]], dtype=float)

# (a) fatoracao_lu própria
print("\n--- (a) fatoracao_lu própria ---")
try:
    L_g, U_g = fatoracao_lu(G)
    print(f"L:\n{L_g}")
    print(f"U:\n{U_g}")
    print(f"Erro ||LU - A||_F = {np.linalg.norm(L_g @ U_g - G, 'fro'):.4e}")
except Exception as e:
    print(f"FALHA - {type(e).__name__}: {e}")

# (b) scipy.linalg.lu
print("\n--- (b) scipy.linalg.lu ---")
P, L_s, U_s = scipy_lu(G)
print(f"P:\n{P}")
print(f"L:\n{L_s}")
print(f"U:\n{U_s}")
print(f"Erro ||PA - LU||_F = {np.linalg.norm(P @ G - L_s @ U_s, 'fro'):.4e}")

# Demonstração: resolver Ax = b usando P, L, U
b_g = np.array([1.0, 5.0])
x_g = subst_retro(U_s, subst_prog(L_s, P @ b_g))
print(f"\nDemonstração Ax = b com b = {b_g}")
print(f"Solução x = {x_g}")
print(f"Resíduo ||Ax - b||_2 = {np.linalg.norm(G @ x_g - b_g, 2):.4e}")

# ==================================================================================
# 3. Fatoração de Cholesky para Matrizes SPD
# ==================================================================================

# ----------------------------------------------------------------------------------
# Q3.1 - Identificando matrizes SPD
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q3.1 - Identificando matrizes SPD")
print("=" * 60)

matrizes = {
    "A1": np.array([[4, 2],
                    [2, 3]], dtype=float),

    "A2": np.array([[1, 2],
                    [2, 1]], dtype=float),

    "A3": np.array([[4, 2, 2],
                    [2, 3, 0],
                    [2, 0, 3]], dtype=float),
}

previsoes = {
    "A1": "SPD — diagonal dominante, det > 0",
    "A2": "NÃO SPD — autovalor negativo esperado",
    "A3": "SPD — simétrica, diagonal dominante por blocos",
}

for nome, M in matrizes.items():
    print(f"\n{'─' * 50}")
    print(f"Matriz {nome}:")
    print(M)

    print(f"\nPrevisão: {previsoes[nome]}")

    # (a) Tentativa de fatoração de Cholesky
    print("\n(a) Cholesky:")
    try:
        x_dummy, L = resolver_cholesky(M, np.ones(M.shape[0]))
        print(f"    Sucesso — L obtida:")
        print(np.array2string(L, formatter={'float_kind': lambda v: f'{v:8.4f}'}))
        print(f"    Verificação ||L @ L.T - A||_F = {np.linalg.norm(L @ L.T - M, 'fro'):.4e}")
        resultado = "SPD"
    except ValueError as err:
        print(f"    Falha detectada: {err}")
        resultado = "NÃO SPD"

    # (b) Autovalores
    autovalores = np.linalg.eigvalsh(M)
    todos_positivos = np.all(autovalores > 0)
    print(f"\n(b) Autovalores (eigvalsh): {autovalores}")
    print(f"    Todos positivos? {'Sim → SPD' if todos_positivos else 'Não → NÃO SPD'}")
    print(f"\n    Conclusão: {resultado}")
    print(f"    Previsão {'CORRETA' if (todos_positivos) == (resultado == 'SPD') else 'INCORRETA'}")

# ----------------------------------------------------------------------------------
# Q3.2 - Cholesky vs. LU: custo
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q3.2 - Cholesky vs. LU: custo computacional")
print("=" * 60)

tamanhos = [50, 100, 200, 500]
tempos_cholesky = []
tempos_lu = []
repeticoes = 5  # média de repetições para reduzir ruído

np.random.seed(42)

print(f"\n{'n':>6} {'Cholesky (s)':>14} {'LU (s)':>14} {'Razão LU/Chol':>15}")
print("-" * 52)

for n in tamanhos:
    # Gerar matriz SPD: A = B^T B + nI
    B = np.random.randn(n, n)
    A_spd = B.T @ B + n * np.eye(n)
    b_vec = np.random.randn(n)

    # Medir Cholesky (média de `repeticoes` execuções)
    t0 = _time.perf_counter()
    for _ in range(repeticoes):
        resolver_cholesky(A_spd, b_vec)
    t_chol = (_time.perf_counter() - t0) / repeticoes

    # Medir LU (média de `repeticoes` execuções)
    t0 = _time.perf_counter()
    for _ in range(repeticoes):
        fatoracao_lu(A_spd)
    t_lu_val = (_time.perf_counter() - t0) / repeticoes

    tempos_cholesky.append(t_chol)
    tempos_lu.append(t_lu_val)

    razao = t_lu_val / t_chol
    print(f"{n:>6} {t_chol:>14.6f} {t_lu_val:>14.6f} {razao:>15.2f}x")

# --- Ajuste de curva n^3 para referência teórica ---
ns = np.array(tamanhos, dtype=float)
coef_chol = tempos_cholesky[-1] / (tamanhos[-1] ** 3)
coef_lu   = tempos_lu[-1]       / (tamanhos[-1] ** 3)
ref_chol  = coef_chol * ns ** 3
ref_lu    = coef_lu   * ns ** 3

# --- Plot log-log ---
plt.figure(figsize=(7, 4.5))
plt.loglog(tamanhos, tempos_cholesky, 'o-',  color='steelblue',  label='Cholesky')
plt.loglog(tamanhos, tempos_lu,       's--', color='tomato',     label='LU (Doolittle)')
plt.loglog(ns, ref_chol, ':',  color='steelblue', alpha=0.5, label=r'$O(n^3)$ ref. Cholesky')
plt.loglog(ns, ref_lu,   ':',  color='tomato',    alpha=0.5, label=r'$O(n^3)$ ref. LU')
plt.xlabel('Tamanho $n$')
plt.ylabel('Tempo médio (s)')
plt.title('Cholesky vs LU — tempo × $n$ (log-log)')
plt.legend()
plt.grid(True, which='both', ls='--', alpha=0.6)
plt.tight_layout()
plt.savefig('q32_plot.png', dpi=150)
plt.show()

# --- Confirmação empírica da razão ≈ 2x ---
razoes = [tlu / tch for tlu, tch in zip(tempos_lu, tempos_cholesky)]
print(f"\nRazão média LU / Cholesky: {np.mean(razoes):.2f}x")
print("Teoricamente esperado: ≈ 2x (LU custa ~n³/3, Cholesky ~n³/6)")

# ----------------------------------------------------------------------------------
# Q3.3 - Comparação de desempenho
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q3.3 - Regressão linear: equações normais via Cholesky")
print("=" * 60)

np.random.seed(42)

# --- Geração dos dados ---
n_obs, n_col = 100, 5
beta_star = np.array([2.0, -1.0, 3.0, 0.5, -2.0])

X = np.hstack([
    np.ones((n_obs, 1)),
    np.random.randn(n_obs, n_col - 1)
])
epsilon = np.random.randn(n_obs) * 0.5
y = X @ beta_star + epsilon

# --- Equações normais: (X^T X) β = X^T y ---
A_normal = X.T @ X
b_normal = X.T @ y

# --- Resolução via Cholesky ---
beta_chol, _ = resolver_cholesky(A_normal, b_normal)

# --- Referência: np.linalg.lstsq ---
beta_lstsq, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

# --- Comparação ---
print(f"\n{'Coeficiente':<14} {'β*':>10} {'Cholesky':>12} {'lstsq':>12}")
print("-" * 50)
nomes = ['β0 (intercepto)', 'β1', 'β2', 'β3', 'β4']
for i, nome in enumerate(nomes):
    print(f"{nome:<14} {beta_star[i]:>10.4f} {beta_chol[i]:>12.4f} {beta_lstsq[i]:>12.4f}")

print(f"\n||β_chol - β_lstsq||_2 = {np.linalg.norm(beta_chol - beta_lstsq, 2):.4e}")

# ==================================================================================
# 4. Algoritmo de Thomas para Sistemas Tridiagonais
# ==================================================================================

# ----------------------------------------------------------------------------------
# Q4.1 - Execução e verificação
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q4.1 - Sistema tridiagonal 5×5 (Algoritmo de Thomas)")
print("=" * 60)

# Definição das diagonais
n = 5
b_diag = [4.0, 4.0, 4.0, 4.0, 4.0]   # diagonal principal
a_diag = [-1.0, -1.0, -1.0, -1.0]    # subdiagonal (n-1 elementos)
c_diag = [-1.0, -1.0, -1.0, -1.0]    # superdiagonal (n-1 elementos)
d_vec  = [1.0, 0.0, 0.0, 0.0, 1.0]   # lado direito

# Resolução pelo Algoritmo de Thomas
x_thomas = thomas(a_diag, b_diag, c_diag, d_vec)

print(f"\nSolução x = {x_thomas}")

# Verificação do resíduo usando montar_tridiagonal
A_tri = montar_tridiagonal(a_diag, b_diag, c_diag)
d_np  = np.array(d_vec)
residuo = np.linalg.norm(A_tri @ x_thomas - d_np, 2)

print(f"\nMatriz A (montada por montar_tridiagonal):")
print(A_tri)
print(f"\nResíduo ||Ax - d||_2 = {residuo:.4e}")

# ----------------------------------------------------------------------------------
# Q4.2 - Thomas vs. Gauss: escalonamento
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q4.2 - Thomas vs. Gauss: escalonamento")
print("=" * 60)

tamanhos = [100, 500, 1000, 5000, 10000]
tempos_thomas = []
tempos_gauss  = []
repeticoes = 5

print(f"\n{'n':>7} {'Thomas (ms)':>13} {'Gauss (ms)':>12} {'Razão':>10} {'Razão teórica':>15}")
print("-" * 62)

for n in tamanhos:
    a = [-1.0] * (n - 1)
    b = [ 4.0] * n
    c = [-1.0] * (n - 1)
    d = [ 1.0] * n

    # (a) Thomas
    t0 = _time.perf_counter()
    for _ in range(repeticoes):
        x_t = thomas(a, b, c, d)
    t_th = (_time.perf_counter() - t0) / repeticoes * 1000

    tempos_thomas.append(t_th)

    # (b) Gauss — apenas para n <= 1000 (evitar travamento)
    if n <= 1000:
        A_dense = montar_tridiagonal(a, b, c)
        d_vec   = np.array(d)
        t0 = _time.perf_counter()
        for _ in range(repeticoes):
            resolver_gauss(A_dense, d_vec)
        t_gs = (_time.perf_counter() - t0) / repeticoes * 1000
        tempos_gauss.append(t_gs)
        razao      = t_gs / t_th
        razao_teo  = n ** 2          # O(n^3) / O(n) = O(n^2)
        print(f"{n:>7} {t_th:>13.4f} {t_gs:>12.4f} {razao:>10.1f} {razao_teo:>15}")
    else:
        tempos_gauss.append(None)
        print(f"{n:>7} {t_th:>13.4f} {'N/A (n>1000)':>12} {'---':>10} {'---':>15}")

# --- Plot ---
ns_thomas = tamanhos
ns_gauss  = [n for n, t in zip(tamanhos, tempos_gauss) if t is not None]
tg_vals   = [t for t in tempos_gauss if t is not None]

plt.figure(figsize=(8, 5))
plt.loglog(ns_thomas, tempos_thomas, 'o-', color='steelblue', label='Thomas  O(n)')
plt.loglog(ns_gauss,  tg_vals,       's--', color='tomato',   label='Gauss   O(n³)')

# Referências teóricas
ns_arr = np.array(ns_thomas, dtype=float)
ref_on  = tempos_thomas[0] * (ns_arr / ns_arr[0])
ref_on3 = tg_vals[0]       * (np.array(ns_gauss, dtype=float) / ns_gauss[0]) ** 3

plt.loglog(ns_arr,                ref_on,  ':',  color='steelblue', alpha=0.5, label='O(n) ref.')
plt.loglog(np.array(ns_gauss),    ref_on3, ':',  color='tomato',    alpha=0.5, label='O(n³) ref.')

plt.xlabel('n')
plt.ylabel('Tempo médio (ms)')
plt.title('Thomas vs. Gauss — tempo × n (log-log)')
plt.legend()
plt.grid(True, which='both', ls='--', alpha=0.6)
plt.tight_layout()
plt.savefig('q42_plot.png', dpi=150)
plt.show()
# ----------------------------------------------------------------------------------
# Q4.3 - Comparação de eficiência
# ----------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Q4.3 - Memoria: matriz densa vs. representacao tridiagonal")
print("=" * 60)

n = 10000

mb_densa       = (n ** 2 * 8) / (2 ** 20)
mb_tridiagonal = ((3 * n - 2) * 8) / (2 ** 20)

print(f"\nn = {n}")
print(f"Matriz densa       : {mb_densa:.2f} MB")
print(f"Repr. tridiagonal  : {mb_tridiagonal:.4f} MB")
print(f"Razao              : {mb_densa / mb_tridiagonal:.0f}x mais memoria na forma densa")
# ==================================================================================
# 5. Custo Computacional Empírico
# ==================================================================================

# ----------------------------------------------------------------------------------
# Q5.1 - Lei de escala
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q5.1 - Lei de potencia: T(n) = c * n^alpha")
print("=" * 60)

tamanhos_gauss = [10, 20, 50, 100, 200, 500]
tempos_q51     = []
repeticoes     = 5

np.random.seed(42)

print(f"\n{'n':>6} {'Tempo medio (ms)':>18}")
print("-" * 26)

for n in tamanhos_gauss:
    A_r = np.random.randn(n, n)
    b_r = np.random.randn(n)

    t0 = _time.perf_counter()
    for _ in range(repeticoes):
        resolver_gauss(A_r.copy(), b_r.copy())
    t_ms = (_time.perf_counter() - t0) / repeticoes * 1000
    tempos_q51.append(t_ms)

    print(f"{n:>6} {t_ms:>18.4f}")

# Ajuste lei de potencia no espaco log-log
log_n = np.log(tamanhos_gauss)
log_t = np.log(tempos_q51)
alpha, log_c = np.polyfit(log_n, log_t, 1)
c = np.exp(log_c)

print(f"\nLei ajustada : T(n) = {c:.4e} * n^{alpha:.4f}")
print(f"Expoente alpha = {alpha:.4f}  (teorico: 3.0)")

# Plot
ns_arr  = np.array(tamanhos_gauss, dtype=float)
fit_arr = c * ns_arr ** alpha

plt.figure(figsize=(7, 4.5))
plt.loglog(tamanhos_gauss, tempos_q51, 'o', color='steelblue', label='Medido')
plt.loglog(ns_arr, fit_arr, '--', color='tomato',
           label=f'Ajuste $T = c \\cdot n^{{{alpha:.2f}}}$')
plt.xlabel('n')
plt.ylabel('Tempo medio (ms)')
plt.title('Custo empirico da Eliminacao de Gauss (log-log)')
plt.legend()
plt.grid(True, which='both', ls='--', alpha=0.6)
plt.tight_layout()
plt.savefig('q51_plot.png', dpi=150)
plt.show()

# ----------------------------------------------------------------------------------
# Q5.2 - Comparação de métodos
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q5.2 - Eficiencia relativa Tmed / Tteo")
print("=" * 60)

# Estimar R: operacoes de ponto flutuante por segundo
n_ref = 500
ops   = n_ref ** 3
t0    = _time.perf_counter()
total = 0.0
for _ in range(n_ref ** 3 // n_ref):   # n^2 iteracoes com n ops cada
    total += 1.0 * n_ref
R = ops / (_time.perf_counter() - t0)

print(f"\nR estimado = {R:.4e} flops/s")

print(f"\n{'n':>6} {'Tmed (ms)':>12} {'Tteo (ms)':>12} {'Tmed/Tteo':>12}")
print("-" * 45)

for n, t_med in zip(tamanhos_gauss, tempos_q51):
    t_teo = (2 * n**3 / 3) / R * 1000   # em ms
    print(f"{n:>6} {t_med:>12.4f} {t_teo:>12.4f} {t_med/t_teo:>12.4f}")

# ----------------------------------------------------------------------------------
# Q5.3 - Comparacao de metodos: n=300, matriz SPD
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q5.3 - Comparacao de metodos: n=300, matriz SPD")
print("=" * 60)

np.random.seed(42)
n = 300
B = np.random.randn(n, n)
A_spd = B.T @ B + n * np.eye(n)
b_spd = np.random.randn(n)
rep   = 5

t0 = _time.perf_counter()
for _ in range(rep):
    resolver_gauss(A_spd.copy(), b_spd.copy())
t_gauss = (_time.perf_counter() - t0) / rep * 1000

t0 = _time.perf_counter()
for _ in range(rep):
    resolver_lu(A_spd.copy(), b_spd.copy())
t_lu = (_time.perf_counter() - t0) / rep * 1000

t0 = _time.perf_counter()
for _ in range(rep):
    resolver_cholesky(A_spd.copy(), b_spd.copy())
t_chol = (_time.perf_counter() - t0) / rep * 1000

t0 = _time.perf_counter()
for _ in range(rep):
    np.linalg.solve(A_spd, b_spd)
t_numpy = (_time.perf_counter() - t0) / rep * 1000

flops  = {'Gauss': 2*n**3/3, 'LU': 2*n**3/3, 'Cholesky': n**3/3, 'NumPy': n**3/3}
tempos = {'Gauss': t_gauss,  'LU': t_lu,      'Cholesky': t_chol, 'NumPy': t_numpy}

print(f"\n{'Metodo':<12} {'Tempo (ms)':>12} {'Flops teoricos':>16} {'Razao / Chol':>14}")
print("-" * 56)
for metodo, t in tempos.items():
    print(f"{metodo:<12} {t:>12.4f} {flops[metodo]:>16.2e} {t/t_chol:>14.4f}")

# ==================================================================================
# 6. Condicionamento e Sensibilidade à Perturbação
# ==================================================================================

# ----------------------------------------------------------------------------------
# Q6.1 - Matriz de Hilbert
# ----------------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Q6.1 - Condicionamento da Matriz de Hilbert")
print("=" * 60)
 
tamanhos = [4, 6, 8, 10, 12]
 
print(f"\n{'n':>4} {'κ₂(Hₙ)':>16} {'Erro relativo':>16} {'Dígitos corretos':>17}")
print("-" * 57)
 
for n in tamanhos:
    kappa, erro_rel = experimento_hilbert(n)
    digitos_corretos = max(0.0, 16 - np.log10(kappa))
    print(f"{n:>4} {kappa:>16.4e} {erro_rel:>16.4e} {digitos_corretos:>17.2f}")
 
print("\nA partir de n = 12 o resultado é completamente não confiável:")
print("κ₂ ≈ 10¹⁶ esgota toda a precisão do float64, zerando os dígitos corretos.")

# ----------------------------------------------------------------------------------
# Q6.2 - Amplificação de erros
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q6.2 - Amplificação de erros por perturbação em b")
print("=" * 60)
 
nivel = 1e-6
n = 6
 
H6 = hilbert(n)
I6 = np.eye(n)
b_H = H6 @ np.ones(n)
b_I = I6 @ np.ones(n)
 
amps_H = perturbar_b(H6, b_H, nivel=nivel, n_amostras=100)
amps_I = perturbar_b(I6, b_I, nivel=nivel, n_amostras=100)
 
kappa_H = np.linalg.cond(H6)
kappa_I = np.linalg.cond(I6)
 
print(f"\n{'Matriz':<6} {'κ₂(A)':>14} {'Amp. máxima':>14} {'Amp. média':>12} {'Dentro do limite?':>18}")
print("-" * 68)
for nome, amps, kappa in [("H6", amps_H, kappa_H), ("I6", amps_I, kappa_I)]:
    amp_max = amps.max()
    amp_med = amps.mean()
    dentro  = "Sim (igualdade)" if abs(amp_max - kappa) < 1e-8 else ("Sim" if amp_max <= kappa else "Não")
    print(f"{nome:<6} {kappa:>14.4e} {amp_max:>14.4e} {amp_med:>12.4e} {dentro:>18}")
 
# --- Histogramas ---
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
 
for ax, amps, kappa, nome, cor in zip(
    axes,
    [amps_H, amps_I],
    [kappa_H, kappa_I],
    ["H₆ (mal condicionada)", "I₆ (identidade)"],
    ["tomato", "steelblue"]
):
    ax.hist(amps, bins=20, color=cor, edgecolor='white', alpha=0.85)
    ax.axvline(amps.max(), color='black', linestyle='--', linewidth=1.2,
               label=f'Amp. máx = {amps.max():.2e}')
    ax.axvline(kappa, color='gray', linestyle=':', linewidth=1.2,
               label=f'κ = {kappa:.2e}')
    ax.set_xlabel('Amplificação do erro')
    ax.set_ylabel('Frequência')
    ax.set_title(nome)
    ax.legend(fontsize=8)
    ax.grid(True, ls='--', alpha=0.5)
 
plt.suptitle('Histograma das amplificações — perturbação em b (nível = 1e-6)')
plt.tight_layout()
plt.savefig('q62_histogramas.png', dpi=150)
plt.show()

# ----------------------------------------------------------------------------------
# Q6.3 - Análise de sensibilidade
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q6.3 - Sensibilidade à perturbação em A")
print("=" * 60)
 
np.random.seed(42)
nivel = 1e-6
 
# Diagonal 5×5: κ ≈ 1.33  (bem condicionada)
A_bem = np.diag([1.0, 1.2, 0.9, 1.1, 1.0])
 
# Hilbert 7×7: κ ≈ 4.75e8 > 10⁶  (mal condicionada)
# H5 tem κ ≈ 4.77e5, insuficiente; H7 garante κ > 10⁶
A_mal = hilbert(7)
 
print(f"\n{'Matriz':<14} {'n':>3} {'κ₂(A)':>14} {'Erro relativo em x':>20} {'κ·ε teórico':>15}")
print("-" * 70)
 
for nome, A in [("Diagonal 5×5", A_bem), ("Hilbert 7×7", A_mal)]:
    n = A.shape[0]
    x_exato = np.ones(n)
    b = A @ x_exato
    kappa = np.linalg.cond(A)
 
    # Perturbação com norma relativa exata = nivel
    ruido = np.random.randn(n, n)
    escala = nivel * np.linalg.norm(A, 'fro') / np.linalg.norm(ruido, 'fro')
    dA = ruido * escala
 
    x_pert = np.linalg.solve(A + dA, b)
    erro_rel = np.linalg.norm(x_pert - x_exato) / np.linalg.norm(x_exato)
    limite_teorico = kappa * nivel
 
    print(f"{nome:<14} {n:>3} {kappa:>14.4e} {erro_rel:>20.4e} {limite_teorico:>15.4e}")
 
print(f"\nPerturbação relativa aplicada em A: {nivel:.0e}")
print("Observação: erro observado ≤ κ·ε (pior caso teórico)")


# ==================================================================================
# 7. Projeto Integrador: PageRank Numérico
# ==================================================================================

from pagerank import matriz_transicao, pagerank_system, condicionamento_pagerank

# ----------------------------------------------------------------------------------
# Q7.1 - PageRank para mini-rede de 4 páginas
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q7.1 - PageRank Numérico (Mini-rede de 4 páginas)")
print("=" * 60)

alpha = 0.85
n = 4

G = np.array([
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=float)

P = matriz_transicao(G)
A_pr, b_pr = pagerank_system(P, alpha)

print("\n(a) Matriz de transição P:")
print(np.array2string(P, formatter={'float_kind': lambda x: f'{x:7.4f}'}))

# Resolver com Gauss e LU
pi_gauss = resolver_gauss(A_pr.copy(), b_pr.copy())
L_pr, U_pr = fatoracao_lu(A_pr.copy())
pi_lu = subst_retro(U_pr, subst_prog(L_pr, b_pr))

print("\n(c) Solução π:")
print(f"{'Página':<8} {'Gauss':>12} {'LU':>12}")
print("-" * 34)
for i in range(n):
    print(f"{'Pág ' + str(i+1):<8} {pi_gauss[i]:>12.6f} {pi_lu[i]:>12.6f}")

print(f"\n(d) ||π||₁ = {pi_gauss.sum():.10f} (deve ser 1)")

# Ranking
ranking = np.argsort(pi_gauss)[::-1]
print("\n(e) Ranking:")
for pos, idx in enumerate(ranking, start=1):
    print(f"    {pos}º lugar: Página {idx+1} (PageRank = {pi_gauss[idx]:.6f})")


# ----------------------------------------------------------------------------------
# Q7.2 - PageRank em rede aleatória (n = 20)
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q7.2 - PageRank: Rede aleatória n=20")
print("=" * 60)

from scipy.linalg import lu_factor, lu_solve

np.random.seed(0)
n, alpha, p = 20, 0.85, 0.3

G20 = (np.random.rand(n, n) < p).astype(float)
np.fill_diagonal(G20, 0)

P20 = matriz_transicao(G20)
A20, b20 = pagerank_system(P20, alpha)

# Gauss
t0 = _time.perf_counter()
pi_gauss = resolver_gauss(A20.copy(), b20.copy())
t_gauss = (_time.perf_counter() - t0) * 1000

# LU próprio
t0 = _time.perf_counter()
L20, U20 = fatoracao_lu(A20.copy())
pi_lu = subst_retro(U20, subst_prog(L20, b20))
t_lu = (_time.perf_counter() - t0) * 1000

# scipy LU
t0 = _time.perf_counter()
pi_scipy = lu_solve(lu_factor(A20), b20)
t_scipy = (_time.perf_counter() - t0) * 1000

print(f"\n{'Método':<14} {'Tempo (ms)':>12} {'Resíduo':>18}")
print("-" * 46)
print(f"{'Gauss':<14} {t_gauss:>12.4f} {np.linalg.norm(A20@pi_gauss - b20):>18.4e}")
print(f"{'LU próprio':<14} {t_lu:>12.4f} {np.linalg.norm(A20@pi_lu - b20):>18.4e}")
print(f"{'scipy LU':<14} {t_scipy:>12.4f} {np.linalg.norm(A20@pi_scipy - b20):>18.4e}")

ranking = np.argsort(pi_scipy)[::-1]
print("\nTop-5 páginas:")
for pos in range(5):
    print(f"    {pos+1}º: Página {ranking[pos]+1} ({pi_scipy[ranking[pos]]:.6f})")

# ----------------------------------------------------------------------------------
# Q7.3 - Condicionamento do sistema PageRank
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q7.3 - κ₂(I − αPᵀ) para diferentes valores de α")
print("=" * 60)

alphas = [0.5, 0.7, 0.85, 0.95, 0.99]
resultados = condicionamento_pagerank(P20, alphas)

print(f"\n{'α':>6} {'κ₂':>16}")
print("-" * 25)
for a, k in resultados:
    print(f"{a:>6.2f} {k:>16.4e}")

plt.figure(figsize=(7, 4.5))
plt.semilogy(alphas, [k for _, k in resultados], 'o-', color='steelblue')
plt.axvline(0.85, color='tomato', linestyle='--', label='α = 0.85')
plt.xlabel('α'); plt.ylabel('κ₂ (escala log)')
plt.title('Condicionamento do sistema PageRank')
plt.legend(); plt.grid(True, alpha=0.6)
plt.tight_layout(); plt.savefig('q73_kappa_alpha.png', dpi=150)
plt.show()

print("\nα = 0.85 equilibra qualidade do ranking e estabilidade numérica.")

# ==================================================================================
# 8. Desafio (Opcional — Pontuação Extra)
# ==================================================================================

# ----------------------------------------------------------------------------------
# Q8.1 - Implementação otimizada
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q8.1 - Estabilidade em cascata: Aε com ε → 0")
print("=" * 60)
 
# Aε = ones(n,n) + ε·I  →  A0 = ones(n,n) é singular (posto 1)
# Autovalores de Aε: ε (n-1 vezes) e n+ε (uma vez)
# κ(Aε) = (n + ε) / ε  ≈  n/ε  quando ε → 0
 
n        = 5
x_exato  = np.ones(n)
A0       = np.ones((n, n), dtype=float)
epsilons = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]
 
print(f"\nAε = ones({n},{n}) + ε·I  →  κ(Aε) = (n+ε)/ε ≈ n/ε\n")
 
print(f"{'ε':>10} {'κ(Aε)':>14} {'κ teórico':>12} {'Erro relativo':>15} {'Resíduo':>14}")
print("-" * 68)
 
for eps in epsilons:
    Ae    = A0 + eps * np.eye(n)
    b     = Ae @ x_exato
    kappa = np.linalg.cond(Ae)
    x_calc = resolver_gauss(Ae.copy(), b.copy())
    erro  = np.linalg.norm(x_calc - x_exato) / np.linalg.norm(x_exato)
    res   = np.linalg.norm(Ae @ x_calc - b)
    print(f"{eps:>10.0e} {kappa:>14.4e} {(n+eps)/eps:>12.4e} {erro:>15.4e} {res:>14.4e}")
 
print("\nConclusão: erro relativo ∝ κ(Aε) · ε_machine = (n/ε) · 10⁻¹⁶")
print("O resíduo permanece pequeno mesmo quando o erro explode —")
print("resíduo pequeno não garante solução correta em sistemas mal condicionados.")

# ----------------------------------------------------------------------------------
# Q8.2 - Comparação com métodos iterativos
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q8.2 - Poisson 2D: Gauss denso vs scipy esparso (m=10)")
print("=" * 60)
 
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import spsolve
 
m = 10          # grade m×m
n = m * m       # tamanho do sistema: n = m² = 100
h = 1 / (m+1)  # passo da grade
 
# --- Construção da matriz bloco-tridiagonal (formato denso) ---
# -4 na diagonal principal, 1 nas quatro vizinhanças (FD 5 pontos)
A_denso = np.zeros((n, n))
 
for i in range(m):
    for j in range(m):
        k = i * m + j          # índice global do ponto (i,j)
        A_denso[k, k] = -4.0
        if j + 1 < m: A_denso[k, k+1] = 1.0   # vizinho direito
        if j - 1 >= 0: A_denso[k, k-1] = 1.0  # vizinho esquerdo
        if i + 1 < m: A_denso[k, k+m] = 1.0   # vizinho abaixo
        if i - 1 >= 0: A_denso[k, k-m] = 1.0  # vizinho acima
 
# Lado direito: f(x,y) = 1 (fonte uniforme), escalado por h²
b_vec = h**2 * np.ones(n)
 
# --- Construção da matriz esparsa (CSR) ---
A_sparse = csr_matrix(A_denso)
 
# --- Memória ---
mb_denso   = A_denso.nbytes / (2**20)
mb_esparso = (A_sparse.data.nbytes + A_sparse.indices.nbytes +
              A_sparse.indptr.nbytes) / (2**20)
 
print(f"\nn = m² = {n}  (grade {m}×{m},  h = 1/{m+1})")
print(f"Não-zeros da matriz: {A_sparse.nnz}  de {n*n} entradas")
print(f"Esparsidade: {100*(1 - A_sparse.nnz/(n*n)):.1f}% de zeros")
 
print(f"\n{'Formato':<14} {'Memória (MB)':>14}")
print("-" * 30)
print(f"{'Denso':<14} {mb_denso:>14.4f}")
print(f"{'Esparso CSR':<14} {mb_esparso:>14.4f}")
print(f"{'Razão':<14} {mb_denso/mb_esparso:>13.1f}x")
 
# --- Resolução: Gauss denso ---
t0      = _time.perf_counter()
x_gauss = resolver_gauss(A_denso.copy(), b_vec.copy())
t_gauss = (_time.perf_counter() - t0) * 1000
 
res_gauss = np.linalg.norm(A_denso @ x_gauss - b_vec)
 
# --- Resolução: scipy spsolve ---
t0       = _time.perf_counter()
x_sparse = spsolve(A_sparse, b_vec)
t_sparse = (_time.perf_counter() - t0) * 1000
 
res_sparse = np.linalg.norm(A_denso @ x_sparse - b_vec)
 
# --- Comparação ---
print(f"\n{'Método':<16} {'Tempo (ms)':>12} {'Resíduo':>14}")
print("-" * 44)
print(f"{'Gauss denso':<16} {t_gauss:>12.4f} {res_gauss:>14.4e}")
print(f"{'scipy spsolve':<16} {t_sparse:>12.4f} {res_sparse:>14.4e}")
print(f"{'Aceleração':<16} {t_gauss/t_sparse:>11.1f}x")
 
print(f"\n||x_gauss - x_sparse||₂ = {np.linalg.norm(x_gauss - x_sparse):.4e}")

# ----------------------------------------------------------------------------------
# Q8.3 - Aplicação em grafo real
# ----------------------------------------------------------------------------------

print("\n" + "=" * 60)
print("Q8.3 - LU vetorizada vs LU com laços (n=100)")
print("=" * 60)
 
def fatoracao_lu_vetorizada(A):
    """LU de Doolittle sem laços Python: usa slicing NumPy no laço externo (k)."""
    A = A.copy().astype(float)
    n = A.shape[0]
    L = np.eye(n)
    for k in range(n):
        # vetor de multiplicadores para toda a coluna k abaixo da diagonal
        L[k+1:, k]    = A[k+1:, k] / A[k, k]
        # atualização do bloco restante em uma única operação vetorial
        A[k+1:, k+1:] -= np.outer(L[k+1:, k], A[k, k+1:])
        A[k+1:, k]    = 0.0
    return L, A   # A tornou-se U
 
n        = 100
rep      = 20
np.random.seed(42)
A_teste  = np.random.randn(n, n)
 
# --- Benchmark ---
t0 = _time.perf_counter()
for _ in range(rep):
    fatoracao_lu(A_teste.copy())
t_loop = (_time.perf_counter() - t0) / rep * 1000
 
t0 = _time.perf_counter()
for _ in range(rep):
    fatoracao_lu_vetorizada(A_teste.copy())
t_vet = (_time.perf_counter() - t0) / rep * 1000
 
# --- Verificação de corretude ---
L_v, U_v = fatoracao_lu_vetorizada(A_teste.copy())
L_l, U_l = fatoracao_lu(A_teste.copy())
erro_vet  = np.linalg.norm(L_v @ U_v - A_teste, 'fro')
erro_loop = np.linalg.norm(L_l @ U_l - A_teste, 'fro')
 
print(f"\n{'Implementação':<22} {'Tempo médio (ms)':>18} {'||LU-A||_F':>14}")
print("-" * 56)
print(f"{'LU com laços':<22} {t_loop:>18.4f} {erro_loop:>14.4e}")
print(f"{'LU vetorizada':<22} {t_vet:>18.4f} {erro_vet:>14.4e}")
print(f"\nGanho de desempenho: {t_loop/t_vet:.2f}x")
print("\nAmbas produzem ||LU - A||_F na ordem do epsilon de máquina.")
print("O ganho vem da substituição dos laços internos (sobre i e j)")
print("por operações BLAS nível-2 (outer product + slice assignment),")
print("executadas em C/Fortran otimizado internamente pelo NumPy.")

# ==================================================================================
# Fim do script
# ==================================================================================
# Relatório gerado por: Jeann Victor Batista
# ==================================================================================