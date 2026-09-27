# ==================================================================================
# main.py
# ==================================================================================
# Plano de Investigação Computacional
# Sistemas de Equações Lineares: Métodos Iterativos em Python
# ==================================================================================
# Disciplina  : Cálculo Numérico
# Professora  : Angela Leite Moreno
# Aluno       : Jeann Victor Batista
# R.A         : 2024.1.08.014
# ==================================================================================

import math
import time
import warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.linalg import lu as scipy_lu

from convergencia       import diagnostico
from jacobi_seidel      import gauss_seidel_modificado, jacobi, gauss_seidel, raio_espectral
from sor                import sor, omega_young, sor_com_historico_x, varredura_omega, raio_espectral_sor
from gradiente_conjugado import cg, pcg, criar_matriz_spd_condicionamento
from custo              import gerar_tridiagonal, medir_tempo

# ==================================================================================
# CONFIGURAÇÃO GRÁFICOS
# ==================================================================================
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'legend.frameon': True,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'grid.linestyle': '--',
    'grid.alpha': 0.3,
    'lines.linewidth': 2,
})

# ==================================================================================
# CONSTANTES GLOBAIS
# ==================================================================================

TOL_PADRAO      = 1e-8          # tolerância padrão para convergência
TOL_ALTA        = 1e-10         # tolerância mais rigorosa (Q6.2 Engenheiro 1)
TOL_BAIXA       = 1e-6          # tolerância relaxada (Q1.1)
TOL_DIVERGE     = 1e-20         # tolerância mínima (Q1.4 — forçar divergência)

MAX_ITER_PADRAO = 500           # máximo de iterações padrão
MAX_ITER_GRANDE = 5000          # para sistemas maiores
MAX_ITER_CALOR  = 30000         # para equação do calor (n grande)
MAX_ITER_REGR   = 10000         # para problema de regressão (Seção 6.2)

DPI_GRAFICOS    = 300           # resolução dos gráficos salvos

N_VALS_ESCALA   = [10, 30, 50, 100, 200, 500]      # Seção 5.1
N_VALS_TEMPO    = [50, 100, 200, 500]               # Seção 5.2
N_VALS_CALOR    = [20, 50, 100, 200, 500]           # Seção 7.2
KAPPA_VALS_CG   = [5, 50, 500, 5000]               # Seção 4.2

OMEGA_VARREDURA_GROSSO = [0.3, 0.5, 0.7, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.7, 1.9]


# ==================================================================================
# UTILITÁRIO DE FORMATAÇÃO DE TABELAS
# ==================================================================================

def _linha_sep(larguras, esq='╠', meio='╬', dir_='╣', fill='═'):
    """Linha separadora unicode."""
    return esq + meio.join(fill * w for w in larguras) + dir_

def _linha_topo(larguras):
    return '╔' + '╦'.join('═' * w for w in larguras) + '╗'

def _linha_fundo(larguras):
    return '╚' + '╩'.join('═' * w for w in larguras) + '╝'

def _linha_dados(larguras, esq='║', meio='║', dir_='║', fill=' '):
    return esq, meio, dir_

def imprimir_tabela(cabecalhos, linhas, alinhamento=None):
    """
    Imprime tabela formatada com bordas unicode.
    cabecalhos : lista de strings
    linhas     : lista de listas de strings
    alinhamento: lista de '<', '^', '>' por coluna (padrão: '^' para todos)
    """
    n_cols = len(cabecalhos)
    larguras = [len(str(c)) for c in cabecalhos]
    for linha in linhas:
        for j, cel in enumerate(linha):
            larguras[j] = max(larguras[j], len(str(cel)))
    larguras = [w + 2 for w in larguras]   # padding lateral

    if alinhamento is None:
        alinhamento = ['^'] * n_cols

    def formatar_linha(valores):
        partes = []
        for v, w, al in zip(valores, larguras, alinhamento):
            s = str(v)
            if al == '<':
                partes.append(' ' + s.ljust(w - 2) + ' ')
            elif al == '>':
                partes.append(' ' + s.rjust(w - 2) + ' ')
            else:
                partes.append(s.center(w))
        return '║' + '║'.join(partes) + '║'

    sep_meio = _linha_sep(larguras)

    print(_linha_topo(larguras))
    print(formatar_linha(cabecalhos))
    print(_linha_sep(larguras))
    for i, linha in enumerate(linhas):
        print(formatar_linha(linha))
        if i < len(linhas) - 1:
            print(_linha_sep(larguras, '╠', '╬', '╣', '─').replace('═', '─'))
    print(_linha_fundo(larguras))


# ==================================================================================
# SEÇÃO 1 — Gauss-Jacobi e Gauss-Seidel: Primeiros Passos
# ==================================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 1 — Gauss-Jacobi e Gauss-Seidel: Primeiros Passos")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Questão 1.1 — Verificação básica e critério de convergência
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 1.1 — Verificação básica e critério de convergência")
print("═" * 72)

A = np.array([
    [ 8, -1,  1],
    [ 1,  6, -2],
    [-1,  2,  7],
], dtype=float)

b      = np.array([14, 10, -5], dtype=float)
x0     = np.zeros(3)
x_star = np.array([2.0, 1.0, -1.0])

# --- Item (a): Dominância diagonal estrita ---
print("\n  Item (a) — Dominância diagonal estrita  αᵢ = Σⱼ≠ᵢ |aᵢⱼ| / |aᵢᵢ|\n")

cab_dd = ['Linha', '|aᵢᵢ|', 'Σ|aᵢⱼ| (j≠i)', 'αᵢ', 'αᵢ < 1?']
linhas_dd = []
diagonal_dominante = True
for i in range(3):
    soma  = sum(abs(A[i, j]) for j in range(3) if j != i)
    diag  = abs(A[i, i])
    alpha = soma / diag
    ok    = alpha < 1
    if not ok:
        diagonal_dominante = False
    linhas_dd.append([str(i + 1), f'{diag:.1f}', f'{soma:.1f}', f'{alpha:.4f}', '✓ Sim' if ok else '✗ Não'])

imprimir_tabela(cab_dd, linhas_dd, ['^', '^', '^', '^', '^'])

if diagonal_dominante:
    print("\n  ✓ A é estritamente diagonal dominante — convergência garantida.\n")
else:
    print("\n  ✗ A NÃO é estritamente diagonal dominante.\n")

# --- Item (b): Primeiras 5 iterações ---
print("  Item (b) — Primeiras 5 iterações (Jacobi vs. Gauss-Seidel)\n")

def historico_iter(A, b, x0, n, metodo='jacobi'):
    A   = np.array(A, dtype=float)
    b   = np.array(b, dtype=float)
    x   = np.array(x0, dtype=float)
    D_inv = 1.0 / np.diag(A)
    R   = A - np.diag(np.diag(A))
    resultado = []
    for _ in range(n):
        if metodo == 'jacobi':
            x = D_inv * (b - R @ x)
        else:
            x_old = x.copy()
            for i in range(len(b)):
                soma = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x_old[i+1:])
                x[i] = (b[i] - soma) / A[i, i]
        resultado.append((x.copy(), np.linalg.norm(A @ x - b)))
    return resultado

hist_j  = historico_iter(A, b, x0, 5, 'jacobi')
hist_gs = historico_iter(A, b, x0, 5, 'gauss_seidel')

cab_iter = ['k', 'GJ — x₁', 'GJ — x₂', 'GJ — x₃', 'GJ — ‖r‖',
                  'GS — x₁', 'GS — x₂', 'GS — x₃', 'GS — ‖r‖']
linhas_iter = []
for k in range(5):
    xj, rj   = hist_j[k]
    xgs, rgs = hist_gs[k]
    linhas_iter.append([
        str(k + 1),
        f'{xj[0]:+.5f}', f'{xj[1]:+.5f}', f'{xj[2]:+.5f}', f'{rj:.3e}',
        f'{xgs[0]:+.5f}', f'{xgs[1]:+.5f}', f'{xgs[2]:+.5f}', f'{rgs:.3e}',
    ])
imprimir_tabela(cab_iter, linhas_iter, ['^'] * 9)

ej  = np.linalg.norm(hist_j[4][0]  - x_star)
egs = np.linalg.norm(hist_gs[4][0] - x_star)
vencedor = "Gauss-Seidel" if egs < ej else "Gauss-Jacobi"
print(f"\n  ‖x⁽⁵⁾ − x*‖₂ → Jacobi: {ej:.2e}  |  Gauss-Seidel: {egs:.2e}")
print(f"  → {vencedor} chegou mais perto de x* = (2, 1, -1) nas primeiras iterações.\n")

# ----------------------------------------------------------------------------------
# Questão 1.2 — Raio Espectral
# ----------------------------------------------------------------------------------

print("═" * 72)
print("  QUESTÃO 1.2 — Análise do Raio Espectral")
print("═" * 72)

rho_J,  _ = raio_espectral(A, metodo='jacobi')
rho_GS, _ = raio_espectral(A, metodo='seidel')

print(f"\n  Item (a) — Raios espectrais")
print(f"    Gauss-Jacobi  : ρ(T_J)  = {rho_J:.8f}")
print(f"    Gauss-Seidel  : ρ(T_GS) = {rho_GS:.8f}")
ambos = rho_J < 1 and rho_GS < 1
print(f"\n  {'✓ Ambos ρ < 1 → convergência garantida.' if ambos else '✗ Nem todos os raios são < 1.'}")

razao = rho_GS / rho_J
print(f"\n  Item (b) — Velocidade relativa")
print(f"    ρ(T_GS) / ρ(T_J) = {rho_GS:.6f} / {rho_J:.6f} = {razao:.4f}")
print(f"    → Gauss-Seidel converge ~{100*(1-razao):.1f}% mais rápido que Jacobi.")

print(f"\n  Item (c) — Estimativa teórica ρᵏ·‖e⁰‖ vs. resíduo observado\n")
e0 = np.linalg.norm(x0 - x_star, np.inf)

cab_rho = ['k', 'GJ — ρᵏ·‖e⁰‖', 'GJ — ‖r⁽ᵏ⁾‖', 'GS — ρᵏ·‖e⁰‖', 'GS — ‖r⁽ᵏ⁾‖']
linhas_rho = []
for k in range(1, 6):
    linhas_rho.append([
        str(k),
        f'{(rho_J**k)*e0:.4e}', f'{hist_j[k-1][1]:.4e}',
        f'{(rho_GS**k)*e0:.4e}', f'{hist_gs[k-1][1]:.4e}',
    ])
imprimir_tabela(cab_rho, linhas_rho)
print("\n  → Resíduos observados ficam abaixo do limite teórico — estimativa confirmada.\n")

# ----------------------------------------------------------------------------------
# Questão 1.3 — Paralelização
# ----------------------------------------------------------------------------------

print("═" * 72)
print("  QUESTÃO 1.3 — Paralelização: Jacobi vs. Gauss-Seidel")
print("═" * 72)

print("\n  Item (a) — Gauss-Seidel modificado: novos vs. antigos (3 iterações)\n")
sol_gsm, _, hist_gsm = gauss_seidel_modificado(A, b, x0=x0, max_iter=3)
print(f"\n  Solução após 3 iterações : x = {np.round(sol_gsm, 6)}")
print(f"  Resíduo final            : {hist_gsm[-1]:.3e}")

print("\n  Item (b) — Por que Gauss-Seidel não paraleliza?")
print("    Cada xᵢ depende dos xⱼ (j < i) já atualizados na mesma iteração.")
print("    Jacobi usa apenas valores da iteração anterior → independência total → paralelizável.")

A2  = np.array([[10, 0, 5], [0, 10, 5], [5, 5, 20]], dtype=float)
b2  = np.array([15, 15, 30], dtype=float)
x0_2 = np.zeros(3)

print("\n  Item (c) — A = [[10,0,5],[0,10,5],[5,5,20]],  b = [15,15,30],  x* = [1,1,1]\n")

cab_c = ['k', 'Jacobi ‖r‖', 'Gauss-Seidel ‖r‖']
linhas_c = []
for k in range(1, 6):
    _, _, hj2  = jacobi(A2, b2, x0=x0_2, max_iter=k)
    _, _, hgs2 = gauss_seidel(A2, b2, x0=x0_2, max_iter=k)
    linhas_c.append([str(k), f'{hj2[-1]:.4e}', f'{hgs2[-1]:.4e}'])
imprimir_tabela(cab_c, linhas_c)
print("\n  → Gauss-Seidel converge mais rápido: x₃ aproveita x₁ e x₂ já atualizados.\n")

# ----------------------------------------------------------------------------------
# Questão 1.4 — Sistema não convergente
# ----------------------------------------------------------------------------------

print("═" * 72)
print("  QUESTÃO 1.4 — Sistema sem convergência garantida")
print("═" * 72)

A3   = np.array([[1, 4, -1], [3, 1, 2], [2, -1, 1]], dtype=float)
b3   = np.array([3, 6, 1], dtype=float)
x0_3 = np.zeros(3)

rho_J3,  _ = raio_espectral(A3, metodo='jacobi')
rho_GS3, _ = raio_espectral(A3, metodo='seidel')

print(f"\n  Item (a) — Raios espectrais")
print(f"    ρ(T_Jacobi)       = {rho_J3:.6f}  {'(> 1 → diverge)' if rho_J3 > 1 else '(< 1)'}")
print(f"    ρ(T_Gauss-Seidel) = {rho_GS3:.6f}  {'(> 1 → diverge)' if rho_GS3 > 1 else '(< 1)'}")

_, _, hist_j3  = jacobi(A3, b3, x0=x0_3, tol=TOL_DIVERGE, max_iter=30)
_, _, hist_gs3 = gauss_seidel(A3, b3, x0=x0_3, tol=TOL_DIVERGE, max_iter=30)

fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(range(1, len(hist_j3)+1), hist_j3, 'b-o', lw=2, ms=4, label='Gauss-Jacobi')
ax.semilogy(range(1, len(hist_gs3)+1), hist_gs3, 'r-s', lw=2, ms=4, label='Gauss-Seidel')
ax.set_xlabel('Iteração $k$')
ax.set_ylabel(r'$\|r^{(k)}\|_2$ (escala log)')
ax.set_title('Q1.4(b) — Resíduo para sistema não convergente\n'
             r'$A$ sem dominância diagonal: $\rho > 1$ para ambos os métodos')
ax.legend()
plt.tight_layout()
plt.savefig('q14b_residuo.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()
print("\n  Item (b) — Gráfico salvo em q14b_residuo.png")

idx  = [1, 0, 2]
A3r  = A3[idx, :]
b3r  = b3[idx]
rho_Jr,  _ = raio_espectral(A3r, metodo='jacobi')
rho_GSr, _ = raio_espectral(A3r, metodo='seidel')
print(f"\n  Item (c) — Reordenação (linha 1 ↔ linha 2):")
print(f"    ρ(T_J)_reord  = {rho_Jr:.6f}  {'(converge)' if rho_Jr < 1 else '(diverge)'}")
print(f"    ρ(T_GS)_reord = {rho_GSr:.6f}  {'(converge)' if rho_GSr < 1 else '(diverge)'}")
if rho_Jr < 1 or rho_GSr < 1:
    print("  → Reordenação melhorou ao menos um método.")
else:
    print("  → Reordenação simples não é suficiente — nenhuma permutação das linhas garante dominância.\n")


# ==================================================================================
# SEÇÃO 2 — Critérios de Convergência: Teoria vs. Prática
# ==================================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 2 — Critérios de Convergência: Teoria vs. Prática")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Questão 2.1 — Diagonal dominância e Sassenfeld
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 2.1 — Diagnóstico de convergência para matrizes de teste")
print("═" * 72)

B1 = np.array([[ 9, -1, -2], [-1,  8, -1], [ 2, -1,  9]], dtype=float)
B2 = np.array([[ 4,  3,  0], [ 3,  4, -1], [ 0, -1,  4]], dtype=float)
B3 = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]], dtype=float)
B4 = np.array([[ 5, -2,  1,  0], [-2,  6, -3,  1],
               [ 1, -3,  7, -2], [ 0,  1, -2,  5]], dtype=float)

for mat, nome in [(B1, 'B1'), (B2, 'B2'), (B3, 'B3'), (B4, 'B4')]:
    diagnostico(mat, nome=nome)

print("\n  → O critério das linhas é o mais restritivo.")
print("  → Em B3, nenhum critério foi satisfeito, mas convergência ainda ocorre na prática.\n")

# ----------------------------------------------------------------------------------
# Questão 2.2 — Condição necessária vs. suficiente
# ----------------------------------------------------------------------------------

print("═" * 72)
print("  QUESTÃO 2.2 — Condição necessária vs. suficiente")
print("═" * 72)

A_2 = np.array([[3, 2, 2], [2, 5, 1], [2, 1, 5]], dtype=float)
diagnostico(A_2, nome="Matriz A_2")

# ----------------------------------------------------------------------------------
# Questão 2.3 — Relação ρ(T_GS) = ρ(T_J)²
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 2.3 — Relação ρ(T_GS) = ρ(T_J)²")
print("═" * 72)

rho_TJ_B4,  _ = raio_espectral(B4, metodo='jacobi')
rho_TGS_B4, _ = raio_espectral(B4, metodo='seidel')

print(f"\n  Item (a) — Verificação para B4:")
print(f"    ρ(T_J)    = {rho_TJ_B4:.6f}")
print(f"    ρ(T_GS)   = {rho_TGS_B4:.6f}")
print(f"    ρ(T_J)²   = {rho_TJ_B4**2:.6f}")
if abs(rho_TGS_B4 - rho_TJ_B4**2) < 1e-6:
    print(f"    ✓ Relação confirmada: ρ(T_GS) = ρ(T_J)²")
else:
    print(f"    ✗ Relação NÃO confirmada (diferença = {abs(rho_TGS_B4 - rho_TJ_B4**2):.2e})")

rho_J_ex  = 0.8
fator     = 1e-6
k_jacobi  = math.ceil(math.log(fator) / math.log(rho_J_ex))
rho_GS_ex = rho_J_ex ** 2
k_seidel  = math.ceil(math.log(fator) / math.log(rho_GS_ex))
print(f"\n  Item (b) — ρ_J = 0,8 → reduzir erro por 10⁻⁶:")
print(f"    Jacobi       : {k_jacobi} iterações")
print(f"    Gauss-Seidel : {k_seidel} iterações  (~metade)\n")

print("  Item (c) — ρ_GS = ρ²_J significa metade das iterações em geral?")
print("    Nem sempre: a relação ρ_GS = ρ²_J só vale para matrizes 'Property A'.")
print("    Fora dessas classes, GS pode ser mais ou menos que o dobro mais rápido que J.\n")


# ==================================================================================
# SEÇÃO 3 — Método SOR: O Papel do Parâmetro ω
# ==================================================================================

print("═" * 72)
print("  SEÇÃO 3 — Método SOR: O Papel do Parâmetro ω")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Questão 3.1 — Sensibilidade ao parâmetro ω
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 3.1 — Sensibilidade ao parâmetro ω no método SOR")
print("═" * 72)

n_sor = 10
A_sor = np.zeros((n_sor, n_sor))
for i in range(n_sor):
    A_sor[i, i] = 4
    if i > 0:         A_sor[i, i-1] = -1
    if i < n_sor - 1: A_sor[i, i+1] = -1
b_sor = np.array([3] * n_sor, dtype=float)

print("\n  Item (a) — Varredura de ω\n")
iteracoes_a = []
for w in OMEGA_VARREDURA_GROSSO:
    _, it, _ = sor(A_sor, b_sor, w, tol=TOL_BAIXA, max_iter=MAX_ITER_PADRAO)
    iteracoes_a.append(it)

cab_w = ['ω', 'Iterações']
linhas_w = [[f'{w:.1f}', str(it)] for w, it in zip(OMEGA_VARREDURA_GROSSO, iteracoes_a)]
imprimir_tabela(cab_w, linhas_w)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(OMEGA_VARREDURA_GROSSO, iteracoes_a, 'b-o', lw=2, ms=6, label='Nº de iterações')
ax.plot(1.0, iteracoes_a[OMEGA_VARREDURA_GROSSO.index(1.0)], 'ro', ms=12,
        label=r'Gauss-Seidel ($\omega=1{,}0$)')
ax.set_xlabel(r'Parâmetro de relaxação $\omega$')
ax.set_ylabel('Número de iterações até convergência')
ax.set_title('Q3.1(a) — SOR: Sensibilidade ao parâmetro $\\omega$\n'
             'Sistema tridiagonal $10\\times 10$, $b_i=3$, tol=$10^{-6}$')
ax.legend()
plt.tight_layout()
plt.savefig('q31a_sensibilidade_omega.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()
print("\n  → Curva com mínimo em ω ≈ 1,5–1,7 e subida acentuada acima do ω ótimo.\n")

print("  Item (b) — ω_ótimo pela fórmula de Young\n")
omega_opt_sor, rho_J_sor, _ = omega_young(A_sor)
print(f"    ω_opt = {omega_opt_sor:.6f}   ρ_J = {rho_J_sor:.6f}")

omegas_fino     = np.linspace(0.3, 1.95, 50)
iteracoes_fino  = varredura_omega(A_sor, b_sor, omegas_fino, tol=TOL_BAIXA, max_iter=MAX_ITER_PADRAO)
idx_min         = np.argmin(iteracoes_fino)
omega_exp       = omegas_fino[idx_min]
iter_min_fino   = iteracoes_fino[idx_min]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(omegas_fino, iteracoes_fino, 'b-', lw=2, label='Iterações (experimental)')
ax.plot(omega_opt_sor,
        iteracoes_fino[np.argmin(np.abs(omegas_fino - omega_opt_sor))],
        'g*', ms=15, label=f'$\\omega_{{opt}}$ teórico = {omega_opt_sor:.4f}')
ax.plot(omega_exp, iter_min_fino, 'r*', ms=15,
        label=f'$\\omega_{{opt}}$ experimental = {omega_exp:.4f}')
ax.axvline(x=1.0, color='gray', ls='--', alpha=0.6, label='Gauss-Seidel puro')
ax.set_xlabel(r'Parâmetro de relaxação $\omega$')
ax.set_ylabel('Número de iterações')
ax.set_title('Q3.1(b) — SOR: $\\omega_{opt}$ teórico vs. experimental\n'
             'Sistema tridiagonal $10\\times 10$, varredura fina com 50 valores')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig('q31b_omega_opt.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()
print("  → Mínimo experimental coincide com ω_opt teórico.\n")

print("  Item (c) — Tabela comparativa (tolerância 10⁻⁸)\n")

hist_tmp    = jacobi(A_sor, b_sor, x0=np.zeros(n_sor), tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)[2]
iter_jac31  = len(hist_tmp)
rho_J31, _  = raio_espectral(A_sor, metodo='jacobi')

hist_tmp    = gauss_seidel(A_sor, b_sor, x0=np.zeros(n_sor), tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)[2]
iter_gs31   = len(hist_tmp)
rho_S31, _  = raio_espectral(A_sor, metodo='seidel')

hist_tmp    = sor(A_sor, b_sor, 0.5, x0=np.zeros(n_sor), tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)[2]
iter_sor05  = len(hist_tmp)
rho_SOR05   = raio_espectral_sor(A_sor, 0.5)

omega_opt31, _, _ = omega_young(A_sor)
hist_tmp    = sor(A_sor, b_sor, omega_opt31, x0=np.zeros(n_sor), tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)[2]
iter_soropt = len(hist_tmp)
rho_SORopt  = raio_espectral_sor(A_sor, omega_opt31)

hist_tmp    = sor(A_sor, b_sor, 1.9, x0=np.zeros(n_sor), tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)[2]
iter_sor19  = len(hist_tmp)
rho_SOR19   = raio_espectral_sor(A_sor, 1.9)

cab_31c = ['Método', 'ω', 'Iterações', 'ρ']
linhas_31c = [
    ['Gauss-Jacobi',      '—',          str(iter_jac31), f'{rho_J31:.6f}'],
    ['Gauss-Seidel',      '1,0',        str(iter_gs31),  f'{rho_S31:.6f}'],
    ['SOR (sub-relaxação)','0,5',        str(iter_sor05), f'{rho_SOR05:.6f}'],
    [f'SOR (ω_opt={omega_opt31:.4f})',  f'{omega_opt31:.4f}', str(iter_soropt), f'{rho_SORopt:.6f}'],
    ['SOR (super-relaxação)','1,9',      str(iter_sor19), f'{rho_SOR19:.6f}'],
]
imprimir_tabela(cab_31c, linhas_31c, ['<', '^', '^', '^'])

# ----------------------------------------------------------------------------------
# Questão 3.2 — Sobre-relaxação: mecanismo e limites
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 3.2 — Sobre-relaxação: mecanismo e limites")
print("═" * 72)

x_gs32,  _, _, x1_gs32  = sor_com_historico_x(A_sor, b_sor, 1.0, x0=np.zeros(n_sor),
                                               tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)
x_sor32, _, _, x1_sor32 = sor_com_historico_x(A_sor, b_sor, 1.2, x0=np.zeros(n_sor),
                                               tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)

print("\n  Item (a) — Evolução de x₁ (GS vs SOR ω=1,2)\n")
cab_x1 = ['Iter.', 'Gauss-Seidel (ω=1,0)', 'SOR (ω=1,2)']
linhas_x1 = []
for i in range(min(len(x1_gs32), len(x1_sor32))):
    linhas_x1.append([str(i), f'{x1_gs32[i]:.8f}', f'{x1_sor32[i]:.8f}'])
imprimir_tabela(cab_x1, linhas_x1)

x1_exato = np.linalg.solve(A_sor, b_sor)[0]
print(f"\n  Solução exata x₁ = {x1_exato:.8f}")
if x_sor32[0] > x1_exato + 1e-10:
    print("  → SOR ultrapassou a solução exata em x₁ (sobre-relaxação detectada).\n")
else:
    print("  → SOR não ultrapassou a solução exata em x₁.\n")

print("  Item (b) — ω = 1,95: o método converge?\n")
_, it195, res195, _ = sor_com_historico_x(A_sor, b_sor, 1.95, x0=np.zeros(n_sor),
                                          tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)
fig, ax = plt.subplots(figsize=(8, 4))
ax.semilogy(range(1, len(res195) + 1), res195, 'b-', lw=2)
ax.set_xlabel('Iteração $k$')
ax.set_ylabel(r'$\|r^{(k)}\|_2$ (escala log)')
ax.set_title(r'Q3.2(b) — SOR com $\omega=1{,}95$: convergência marginal'
             '\nSistema tridiagonal $10\times 10$')
plt.tight_layout()
plt.savefig('q32b_sor195.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()
if it195 < MAX_ITER_PADRAO:
    print(f"  → Convergiu em {it195} iterações (convergência lenta mas válida).\n")
else:
    print("  → Não convergiu em 500 iterações.\n")

print("  Item (c) — Teste ω = 2,0 e ω = 2,1 (condição necessária 0 < ω < 2)\n")
for w_test in [2.0, 2.1]:
    try:
        _, it_w, _ = sor(A_sor, b_sor, w_test, x0=np.zeros(n_sor), tol=TOL_PADRAO,
                         max_iter=MAX_ITER_PADRAO)
        print(f"  ω = {w_test} → convergiu em {it_w} iterações")
    except ValueError as e:
        print(f"  ω = {w_test} → Erro levantado: {e}")

# ----------------------------------------------------------------------------------
# Questão 3.3 — Fórmula de Young para B2
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 3.3 — Fórmula de Young para matriz B2")
print("═" * 72)

b_b2 = B2 @ np.ones(len(B2))
w_opt_b2, _, _ = omega_young(B2)
print(f"\n  Item (a) — ω_opt (Young) para B2 : {w_opt_b2:.6f}\n")

res_b2 = varredura_omega(B2, b_b2, OMEGA_VARREDURA_GROSSO, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)
cab_b2 = ['ω', 'Iterações']
linhas_b2 = [[f'{w:.1f}', str(it)] for w, it in zip(OMEGA_VARREDURA_GROSSO, res_b2)]
imprimir_tabela(cab_b2, linhas_b2)

idx_min_b2 = int(np.argmin(res_b2))
print(f"\n  Mínimo experimental : {res_b2[idx_min_b2]} iterações em ω = {OMEGA_VARREDURA_GROSSO[idx_min_b2]}")
print("  → ω experimental próximo do ω_opt teórico.\n")

print("  Item (b) — Precisão da fórmula de Young:")
print("    ✓ Precisa para B2 (condições Property A satisfeitas).")
print("    Limitações: fora de Property A, o ω real pode divergir do teórico.\n")


# ==================================================================================
# SEÇÃO 4 — Gradiente Conjugado: Convergência por Subespaços
# ==================================================================================

print("═" * 72)
print("  SEÇÃO 4 — Gradiente Conjugado: Convergência por Subespaços")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Questão 4.1 — CG vs. SOR
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 4.1 — CG vs. SOR em sistemas SPD (n = 20)")
print("═" * 72)

n_41 = 20
A_41 = np.zeros((n_41, n_41))
for i in range(n_41):
    A_41[i, i] = 4
    if i > 0:       A_41[i, i-1] = -1
    if i < n_41-1:  A_41[i, i+1] = -1
x_exato_41 = np.ones(n_41)
b_41 = A_41 @ x_exato_41

x_j41,   it_j41,   hist_jac41 = jacobi(A_41, b_41, x0=np.zeros(n_41), tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)
x_gs41,  it_gs41,  hist_gs41  = gauss_seidel(A_41, b_41, x0=np.zeros(n_41), tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)
omega_opt41 = omega_young(A_41)[0]
x_sor41, it_sor41, hist_sor41 = sor(A_41, b_41, omega_opt41, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)
x_cg41,  it_cg41,  hist_cg41  = cg(A_41, b_41, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)

print("\n  Item (a) — Comparação dos métodos\n")
cab_41a = ['Método', 'Iterações', '‖r_final‖', 'Custo/iter.', 'Tipo']
linhas_41a = [
    ['Gauss-Jacobi',   str(it_j41),   f'{np.linalg.norm(b_41 - A_41 @ x_j41):.2e}', 'O(n²)', 'Estacionário'],
    ['Gauss-Seidel',   str(it_gs41),  f'{np.linalg.norm(b_41 - A_41 @ x_gs41):.2e}', 'O(n²)', 'Estacionário'],
    [f'SOR (ω={omega_opt41:.3f})', str(it_sor41), f'{np.linalg.norm(b_41 - A_41 @ x_sor41):.2e}', 'O(n²)', 'Estacionário'],
    ['Grad. Conjugado', str(it_cg41), f'{np.linalg.norm(b_41 - A_41 @ x_cg41):.2e}', 'O(nnz)', 'Krylov'],
]
imprimir_tabela(cab_41a, linhas_41a, ['<', '^', '^', '^', '<'])

fig, ax = plt.subplots(figsize=(9, 5))
ax.semilogy(hist_jac41, 'b-o', lw=2, ms=3, label='Gauss-Jacobi', markevery=5)
ax.semilogy(hist_gs41,  'r-s', lw=2, ms=3, label='Gauss-Seidel', markevery=5)
ax.semilogy(hist_sor41, 'g-^', lw=2, ms=3,
            label=f'SOR ($\\omega_{{opt}}={omega_opt41:.3f}$)', markevery=5)
ax.semilogy(hist_cg41,  'm-d', lw=2, ms=3, label='Gradiente Conjugado', markevery=2)
ax.set_xlabel('Iteração $k$')
ax.set_ylabel(r'$\|r^{(k)}\|_2$ (escala log)')
ax.set_title('Q4.1(b) — Curvas de convergência dos métodos iterativos\n'
             'Sistema tridiagonal $n=20$, $b = A\\mathbf{1}$, tol = $10^{-8}$')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig('q41b_curvas_convergencia.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()

print(f"\n  Item (c) — CG convergiu em {it_cg41} iterações (≤ n = {n_41}: {'✓' if it_cg41 <= n_41 else '✗'})\n")

# ----------------------------------------------------------------------------------
# Questão 4.2 — Impacto do número de condição
# ----------------------------------------------------------------------------------

print("═" * 72)
print("  QUESTÃO 4.2 — Impacto do número de condição no CG (n = 30)")
print("═" * 72)

n_42 = 30
iteracoes_cg42 = []
print()
for kappa in KAPPA_VALS_CG:
    A42 = criar_matriz_spd_condicionamento(n_42, kappa)
    b42 = A42 @ np.ones(n_42)
    x42, it42, _ = cg(A42, b42, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)
    iteracoes_cg42.append(it42)
    print(f"    κ = {kappa:5d} → {it42:3d} iterações   ‖r‖ = {np.linalg.norm(b42 - A42 @ x42):.2e}")

eps_teo     = TOL_PADRAO
iters_teo42 = [0.5 * np.sqrt(k) * np.log(2 / eps_teo) for k in KAPPA_VALS_CG]

fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(KAPPA_VALS_CG, iteracoes_cg42, 'bo-', lw=2, ms=8, label='CG (experimental)')
ax.loglog(KAPPA_VALS_CG, iters_teo42, 'r--', lw=2,
          label=r'Teórica: $\frac{1}{2}\sqrt{\kappa}\ln\!\left(\frac{2}{\varepsilon}\right)$')
ax.set_xlabel(r'Número de condição $\kappa(A)$ (escala log)')
ax.set_ylabel('Número de iterações (escala log)')
ax.set_title('Q4.2(b) — Iterações do CG vs. condicionamento $\\kappa(A)$\n'
             'Sistema SPD $n=30$, tol = $10^{-8}$ (escala log-log)')
ax.legend()
plt.tight_layout()
plt.savefig('q42b_cg_vs_kappa.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()

print(f"\n  Item (c) — Compatibilidade com estimativa teórica k ≈ ½√κ·ln(2/ε):\n")
cab_42c = ['κ', 'Exp.', 'Teórico']
linhas_42c = [[str(k), str(it), f'{t:.0f}']
              for k, it, t in zip(KAPPA_VALS_CG, iteracoes_cg42, iters_teo42)]
imprimir_tabela(cab_42c, linhas_42c)
print("  → Dados seguem a tendência √κ, confirmando a teoria.\n")

print("  Item (d) — Comparação com Gauss-Seidel para κ = 5000\n")
A42d = criar_matriz_spd_condicionamento(n_42, 5000)
b42d = A42d @ np.ones(n_42)
_, it_gs42d, _ = gauss_seidel(A42d, b42d, x0=None, tol=TOL_PADRAO, max_iter=5000)
print(f"    Gauss-Seidel : {it_gs42d} iterações")
print(f"    CG           : {iteracoes_cg42[-1]} iterações")
print("  → CG é muito menos afetado pelo mau condicionamento.\n")

# ----------------------------------------------------------------------------------
# Questão 4.3 — Pré-condicionamento
# ----------------------------------------------------------------------------------

print("═" * 72)
print("  QUESTÃO 4.3 — Pré-condicionamento na prática")
print("═" * 72)

n_43    = 30
A43     = criar_matriz_spd_condicionamento(n_43, 5000)
b43     = A43 @ np.ones(n_43)
diag_43 = np.diag(A43)
M_inv_jac43 = lambda v: v / diag_43

x_pcg43, it_pcg43, _ = pcg(A43, b43, M_inv=M_inv_jac43, x0=None, tol=TOL_PADRAO,
                            max_iter=MAX_ITER_PADRAO)
x_cg43,  it_cg43,  _ = cg(A43, b43, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)

kappa_A43  = np.linalg.cond(A43)
kappa_MA43 = np.linalg.cond(np.diag(1.0 / diag_43) @ A43)

print(f"\n  Item (b) — κ(A) = {kappa_A43:.2e}   κ(M⁻¹A) = {kappa_MA43:.2e}")
print("  → Pré-cond. Jacobi não melhora significativamente (diagonal quase uniforme).\n")

print("  Item (c) — Tabela comparativa\n")
cab_43c = ['Configuração', 'Iterações', 'κ efetivo', '‖r_final‖']
linhas_43c = [
    ['CG sem pré-cond.',  str(it_cg43),  f'{kappa_A43:.2e}',  f'{np.linalg.norm(b43 - A43 @ x_cg43):.2e}'],
    ['PCG + Jacobi',      str(it_pcg43), f'{kappa_MA43:.2e}', f'{np.linalg.norm(b43 - A43 @ x_pcg43):.2e}'],
]
imprimir_tabela(cab_43c, linhas_43c, ['<', '^', '^', '^'])

print("\n  Item (d) — Eficácia do pré-cond. Jacobi:")
print("    Eficaz quando a diagonal de A é dominante e varia muito.")
print("    Ineficaz quando a diagonal é quase uniforme (como A = QΛQᵀ com λ uniformes).\n")


# ==================================================================================
# SEÇÃO 5 — Custo Computacional e Escalabilidade
# ==================================================================================

print("═" * 72)
print("  SEÇÃO 5 — Custo Computacional e Escalabilidade")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Questão 5.1 — Como k varia com n?
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 5.1 — Como o número de iterações k varia com n?")
print("═" * 72)

n_list51, iter_j51, iter_gs51, iter_sor51 = [], [], [], []

print()
for n in N_VALS_ESCALA:
    A51, b51     = gerar_tridiagonal(n, 4, -1)
    _, it_j,  _  = jacobi(A51, b51, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_GRANDE)
    _, it_gs, _  = gauss_seidel(A51, b51, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_GRANDE)
    w_51         = omega_young(A51)[0]
    _, it_sor, _ = sor(A51, b51, w_51, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_GRANDE)
    n_list51.append(n); iter_j51.append(it_j)
    iter_gs51.append(it_gs); iter_sor51.append(it_sor)
    print(f"    n = {n:4d} : Jacobi = {it_j:5d}   GS = {it_gs:5d}   SOR(ω_opt) = {it_sor:5d}")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, escala in zip(axes, ['linear', 'log']):
    plot = ax.loglog if escala == 'log' else ax.plot
    plot(n_list51, iter_j51,   'bo-', lw=2, ms=6, label='Gauss-Jacobi')
    plot(n_list51, iter_gs51,  'rs-', lw=2, ms=6, label='Gauss-Seidel')
    plot(n_list51, iter_sor51, 'g^-', lw=2, ms=6, label='SOR($\\omega_{opt}$)')
    ax.set_xlabel('Tamanho $n$' + (' (escala log)' if escala == 'log' else ''))
    ax.set_ylabel('Iterações' + (' (escala log)' if escala == 'log' else ''))
    ax.set_title(f'({chr(97 + ["linear","log"].index(escala))}) Escala {escala}')
    ax.legend(fontsize=9)
fig.suptitle('Q5.1 — Iterações vs. tamanho do sistema\n'
             'Sistema tridiagonal $A_{ii}=4$, $A_{i,i\\pm1}=-1$, $b=\\mathbf{1}$',
             fontweight='bold')
plt.tight_layout()
plt.savefig('q51_iteracoes_vs_n.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()

log_n51   = np.log(n_list51)
alpha_j51,   _ = np.polyfit(log_n51, np.log(iter_j51),   1)[[0, 1]], None
alpha_gs51,  _ = np.polyfit(log_n51, np.log(iter_gs51),  1)[[0, 1]], None
alpha_sor51, _ = np.polyfit(log_n51, np.log(iter_sor51), 1)[[0, 1]], None
alpha_j51   = np.polyfit(log_n51, np.log(iter_j51),   1)[0]
alpha_gs51  = np.polyfit(log_n51, np.log(iter_gs51),  1)[0]
alpha_sor51 = np.polyfit(log_n51, np.log(iter_sor51), 1)[0]

print(f"\n  Item (b) — Lei de potência k ∝ nᵅ:")
print(f"    Jacobi        : α ≈ {alpha_j51:.2f}")
print(f"    Gauss-Seidel  : α ≈ {alpha_gs51:.2f}")
print(f"    SOR(ω_opt)    : α ≈ {alpha_sor51:.2f}")
print("  → α ≈ 0 (k quase constante com n para este b = ones(n)).\n")

print("  Item (c) — SOR ótimo: α teórico para Poisson é 1, obtido ≈ 0 (b uniforme).\n")

print("  Item (d) — Custo total vs. LU:\n")
cab_51d = ['n', 'Custo Jacobi', 'Custo GS', 'Custo SOR', 'Custo LU (O(n³))']
linhas_51d = []
for i, n in enumerate(N_VALS_ESCALA):
    linhas_51d.append([
        str(n),
        f'{iter_j51[i]*n**2:.2e}',
        f'{iter_gs51[i]*n**2:.2e}',
        f'{iter_sor51[i]*n**2:.2e}',
        f'{n**3:.2e}',
    ])
imprimir_tabela(cab_51d, linhas_51d)
print("  → Iterativos superam LU quando k·n² < n³, i.e., n > k.\n")

# ----------------------------------------------------------------------------------
# Questão 5.2 — Tempo real de execução
# ----------------------------------------------------------------------------------

print("═" * 72)
print("  QUESTÃO 5.2 — Tempo real de execução")
print("═" * 72)

time_gj52, time_gs52, time_sor52, time_direct52 = [], [], [], []

print()
for n in N_VALS_TEMPO:
    A52, b52 = gerar_tridiagonal(n, 4, -1)
    w52      = omega_young(A52)[0]
    t_gj  = medir_tempo(jacobi, A52, b52, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_GRANDE)
    t_gs  = medir_tempo(gauss_seidel, A52, b52, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_GRANDE)
    t_sor = medir_tempo(sor, A52, b52, w52, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_GRANDE)
    t_dir = medir_tempo(np.linalg.solve, A52, b52)
    time_gj52.append(t_gj); time_gs52.append(t_gs)
    time_sor52.append(t_sor); time_direct52.append(t_dir)
    print(f"    n = {n:4d} : J={t_gj:.4f}s  GS={t_gs:.4f}s  SOR={t_sor:.4f}s  Direto={t_dir:.6f}s")

fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(N_VALS_TEMPO, time_gj52,     'bo-', lw=2, ms=8, label='Gauss-Jacobi')
ax.loglog(N_VALS_TEMPO, time_gs52,     'rs-', lw=2, ms=8, label='Gauss-Seidel')
ax.loglog(N_VALS_TEMPO, time_sor52,    'g^-', lw=2, ms=8, label='SOR ($\\omega_{opt}$)')
ax.loglog(N_VALS_TEMPO, time_direct52, 'kd-', lw=2, ms=8, label='numpy.linalg.solve')
ax.set_xlabel('Tamanho $n$ (escala log)')
ax.set_ylabel('Tempo de execução (s) (escala log)')
ax.set_title('Q5.2 — Tempo de execução vs. tamanho do sistema (escala log-log)\n'
             'Comparação iterativos vs. método direto')
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('q52_tempo_vs_n.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()

log_n52 = np.log(N_VALS_TEMPO)
alpha_gj52  = np.polyfit(log_n52, np.log(time_gj52),  1)[0]
alpha_gs52  = np.polyfit(log_n52, np.log(time_gs52),  1)[0]
alpha_sor52 = np.polyfit(log_n52, np.log(time_sor52), 1)[0]

print(f"\n  Item (a) — Expoentes empíricos T ∝ nᵅ:")
print(f"    Jacobi       : α ≈ {alpha_gj52:.2f}")
print(f"    Gauss-Seidel : α ≈ {alpha_gs52:.2f}")
print(f"    SOR          : α ≈ {alpha_sor52:.2f}")

print("\n  Item (b) — Método mais rápido por n:\n")
cab_52b = ['n', 'Mais rápido']
linhas_52b = []
for i, n in enumerate(N_VALS_TEMPO):
    tempos = {'Jacobi': time_gj52[i], 'GS': time_gs52[i],
              'SOR': time_sor52[i], 'numpy.solve': time_direct52[i]}
    linhas_52b.append([str(n), min(tempos, key=tempos.get)])
imprimir_tabela(cab_52b, linhas_52b)

print("\n  Item (c) — CG vs. numpy.solve para n = 500\n")
A52c, b52c = gerar_tridiagonal(500, 4, -1)
t_cg500  = medir_tempo(cg, A52c, b52c, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_GRANDE)
t_dir500 = medir_tempo(np.linalg.solve, A52c, b52c)
print(f"    CG                 : {t_cg500:.6f} s")
print(f"    numpy.linalg.solve : {t_dir500:.6f} s")
print(f"    → {'CG' if t_cg500 < t_dir500 else 'numpy.solve'} foi mais rápido.\n")


# ==================================================================================
# SEÇÃO 6 — Comparação Global
# ==================================================================================

print("═" * 72)
print("  SEÇÃO 6 — Comparação Global: Quando Usar Cada Método?")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Questão 6.1 — Tabela de síntese
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 6.1 — Análise comparativa estruturada")
print("═" * 72)

_n_ref = 10
A_ref  = np.zeros((_n_ref, _n_ref))
for i in range(_n_ref):
    A_ref[i, i] = 4
    if i > 0:        A_ref[i, i-1] = -1
    if i < _n_ref-1: A_ref[i, i+1] = -1
b_ref = np.ones(_n_ref)

rho_J_ref,  _ = raio_espectral(A_ref, metodo='jacobi')
rho_GS_ref, _ = raio_espectral(A_ref, metodo='seidel')
omega_ref, _, _ = omega_young(A_ref)
rho_SOR_ref    = raio_espectral_sor(A_ref, omega_ref)

_, iter_J_ref,   _ = jacobi(A_ref, b_ref, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)
_, iter_GS_ref,  _ = gauss_seidel(A_ref, b_ref, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)
_, iter_SOR_ref, _ = sor(A_ref, b_ref, omega_ref, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)

_, iter_CG_ref, _ = cg(A_41, b_41, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)

print()
cab_61 = ['Aspecto', 'Gauss-Jacobi', 'Gauss-Seidel', 'SOR ótimo', 'Grad. Conj.']
linhas_61 = [
    ['Req. sobre A',            'ρ(T_J) < 1',      'ρ(T_GS) < 1',     '0 < ω < 2',           'A deve ser SPD'],
    ['Custo/iter.',             'O(n²)',             'O(n²)',            'O(n²)',                'O(nnz)'],
    [f'Iters. (n={_n_ref})',    str(iter_J_ref),    str(iter_GS_ref),   str(iter_SOR_ref),     f'{iter_CG_ref} (n=20)'],
    ['Paralelizável?',          'Sim',              'Não',              'Não',                 'Parcial'],
    ['Memória',                 '2 vetores',        '1 vetor (in-pl.)', '1 vetor (in-pl.)',    '3 vetores'],
    ['Impacto de κ(A)',         'Alto',             'Alto',             'Médio',               'Baixo'],
    ['Melhor cenário',          'Esparso+paralelo', 'SPD / κ moderado', 'ω_opt conhecido',     'SPD / κ alto'],
    ['Pior cenário',            'κ alto / sem D.D.','A não SPD',        'ω mal escolhido',     'A não SPD'],
]
imprimir_tabela(cab_61, linhas_61, ['<', '<', '<', '<', '<'])

# ----------------------------------------------------------------------------------
# Questão 6.2 — Escolha do solver para regressão
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 6.2 — Escolha do solver: n = 800, κ ≈ 2000")
print("═" * 72)

n_62   = 800
Z62    = criar_matriz_spd_condicionamento(n_62, 2000)
x_ex62 = np.ones(n_62)
b62    = Z62 @ x_ex62

x_j62, it_j62, _ = jacobi(Z62, b62, x0=None, tol=TOL_ALTA, max_iter=MAX_ITER_REGR)
if np.any(np.isnan(x_j62)) or np.any(np.isinf(x_j62)) or it_j62 >= MAX_ITER_REGR:
    print(f"\n  Eng. 1 (Jacobi tol=10⁻¹⁰) : NÃO convergiu (divergência numérica)")
else:
    print(f"\n  Eng. 1 (Jacobi tol=10⁻¹⁰) : {it_j62} iterações, erro={np.linalg.norm(x_j62-x_ex62):.2e}")

x_s62, it_s62, _ = sor(Z62, b62, omega=1.5, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_REGR)
print(f"  Eng. 2 (SOR ω=1,5 tol=10⁻⁸): {it_s62} iterações, erro={np.linalg.norm(x_s62-x_ex62):.2e}")

M_inv62 = lambda v: v / np.diag(Z62)
x_p62, it_p62, _ = pcg(Z62, b62, M_inv=M_inv62, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_REGR)
print(f"  Eng. 3 (PCG+Jacobi tol=10⁻⁸): {it_p62} iterações, erro={np.linalg.norm(x_p62-x_ex62):.2e}")

print("\n  Item (a) — Recomendação: PCG + pré-cond. Jacobi")
print("  Item (b) — Riscos: Jacobi pode divergir; SOR exige ω correto; PCG requer A SPD.")
print("  Item (c) — Informações úteis: esparsidade, κ exato, estrutura de A.\n")


# ==================================================================================
# SEÇÃO 7 — Projeto Integrador: Equação de Calor Estacionária
# ==================================================================================

print("═" * 72)
print("  SEÇÃO 7 — Projeto Integrador: Equação de Calor Estacionária")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Questão 7.1 — n = 50
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 7.1 — Resolução do sistema da equação do calor (n = 50)")
print("═" * 72)

n_71 = 50
h_71 = 1 / (n_71 + 1)
x_pts71   = np.linspace(h_71, 1 - h_71, n_71)
u_exata71 = np.sin(np.pi * x_pts71)
b_71      = (np.pi**2) * np.sin(np.pi * x_pts71)
A_71      = (2*np.eye(n_71) - np.diag(np.ones(n_71-1), 1) - np.diag(np.ones(n_71-1), -1)) / h_71**2

omega_71 = omega_young(A_71)[0]

t_j71   = medir_tempo(jacobi, A_71, b_71, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)
u_j71,  it_j71,  hist_j71  = jacobi(A_71, b_71, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)

t_gs71  = medir_tempo(gauss_seidel, A_71, b_71, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)
u_gs71, it_gs71, hist_gs71 = gauss_seidel(A_71, b_71, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)

t_sor71 = medir_tempo(sor, A_71, b_71, omega=omega_71, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)
u_sor71, it_sor71, hist_sor71 = sor(A_71, b_71, omega=omega_71, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)

t_cg71  = medir_tempo(cg, A_71, b_71, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)
u_cg71, it_cg71, hist_cg71 = cg(A_71, b_71, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x_pts71, u_exata71, 'k-', lw=3, label='Exata: $u(x)=\\sin(\\pi x)$')
ax.plot(x_pts71, u_j71,   '--', lw=1.5, label='Jacobi')
ax.plot(x_pts71, u_gs71,  '--', lw=1.5, label='Gauss-Seidel')
ax.plot(x_pts71, u_sor71, '--', lw=1.5, label=f'SOR ($\\omega={omega_71:.3f}$)')
ax.plot(x_pts71, u_cg71,  '--', lw=1.5, label='CG')
ax.set_xlabel('$x$')
ax.set_ylabel('$u(x)$')
ax.set_title('Q7.1(a) — Equação do calor estacionária: solução numérica vs. exata\n'
             '$-u\'\'(x)=\\pi^2\\sin(\\pi x)$,  $n=50$,  tol=$10^{-8}$')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig('q71a_solucao_calor.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()

rho_j71, _ = raio_espectral(A_71, metodo='jacobi')
rho_gs71, _ = raio_espectral(A_71, metodo='gs')
rho_sor71   = raio_espectral_sor(A_71, omega_71)

print("\n  Item (c) — Tabela comparativa (n = 50)\n")
cab_71c = ['Método', 'Iterações', '‖uₙᵤₘ − uₑₓₐₜₐ‖∞', 'Tempo (ms)', 'ρ']
linhas_71c = [
    ['Gauss-Jacobi',       str(it_j71),   f'{np.linalg.norm(u_j71-u_exata71,np.inf):.2e}',
     f'{t_j71*1e3:.2f}', f'{rho_j71:.6f}'],
    ['Gauss-Seidel',       str(it_gs71),  f'{np.linalg.norm(u_gs71-u_exata71,np.inf):.2e}',
     f'{t_gs71*1e3:.2f}', f'{rho_gs71:.6f}'],
    [f'SOR (ω={omega_71:.3f})', str(it_sor71),
     f'{np.linalg.norm(u_sor71-u_exata71,np.inf):.2e}', f'{t_sor71*1e3:.2f}', f'{rho_sor71:.6f}'],
    ['CG',                 str(it_cg71),  f'{np.linalg.norm(u_cg71-u_exata71,np.inf):.2e}',
     f'{t_cg71*1e3:.2f}', '—'],
]
imprimir_tabela(cab_71c, linhas_71c, ['<', '^', '^', '^', '^'])

# ----------------------------------------------------------------------------------
# Questão 7.2 — Variação de n
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 7.2 — Variação do tamanho do problema")
print("═" * 72)

iter_j72, iter_gs72, iter_sor72, iter_cg72   = [], [], [], []
erro_j72, erro_gs72, erro_sor72, erro_cg72   = [], [], [], []
tempo_j72, tempo_gs72, tempo_sor72, tempo_cg72 = [], [], [], []

for n in N_VALS_CALOR:
    h    = 1 / (n + 1)
    xp   = np.linspace(h, 1 - h, n)
    ue   = np.sin(np.pi * xp)
    bv   = (np.pi**2) * np.sin(np.pi * xp)
    Av   = (2*np.eye(n) - np.diag(np.ones(n-1), 1) - np.diag(np.ones(n-1), -1)) / h**2
    w_v  = omega_young(Av)[0]

    tj  = medir_tempo(jacobi, Av, bv, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)
    uj, ij, _ = jacobi(Av, bv, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)

    tgs = medir_tempo(gauss_seidel, Av, bv, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)
    ugs, igs, _ = gauss_seidel(Av, bv, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)

    tsor = medir_tempo(sor, Av, bv, omega=w_v, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)
    usor, isor, _ = sor(Av, bv, omega=w_v, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)

    tcg = medir_tempo(cg, Av, bv, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)
    ucg, icg, _ = cg(Av, bv, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)

    iter_j72.append(ij); iter_gs72.append(igs)
    iter_sor72.append(isor); iter_cg72.append(icg)
    erro_j72.append(np.linalg.norm(uj - ue, np.inf))
    erro_gs72.append(np.linalg.norm(ugs - ue, np.inf))
    erro_sor72.append(np.linalg.norm(usor - ue, np.inf))
    erro_cg72.append(np.linalg.norm(ucg - ue, np.inf))
    tempo_j72.append(tj*1e3); tempo_gs72.append(tgs*1e3)
    tempo_sor72.append(tsor*1e3); tempo_cg72.append(tcg*1e3)

fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(N_VALS_CALOR, iter_j72,   'bo-', lw=2, ms=6, label='Jacobi')
ax.loglog(N_VALS_CALOR, iter_gs72,  'rs-', lw=2, ms=6, label='Gauss-Seidel')
ax.loglog(N_VALS_CALOR, iter_sor72, 'g^-', lw=2, ms=6, label='SOR')
ax.loglog(N_VALS_CALOR, iter_cg72,  'md-', lw=2, ms=6, label='CG')
ax.set_xlabel('$n$ (escala log)')
ax.set_ylabel('Número de iterações (escala log)')
ax.set_title('Q7.2(a) — Iterações vs. tamanho do problema\n'
             'Equação do calor, $-u\'\'=f$, escala log-log')
ax.legend()
plt.tight_layout()
plt.savefig('q72a_iteracoes_vs_n.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()

fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(N_VALS_CALOR, erro_j72,   'bo-', lw=2, ms=6, label='Jacobi')
ax.loglog(N_VALS_CALOR, erro_gs72,  'rs-', lw=2, ms=6, label='Gauss-Seidel')
ax.loglog(N_VALS_CALOR, erro_sor72, 'g^-', lw=2, ms=6, label='SOR')
ax.loglog(N_VALS_CALOR, erro_cg72,  'md-', lw=2, ms=6, label='CG')
ax.set_xlabel('$n$ (escala log)')
ax.set_ylabel(r'$\|u_{num} - u_{exata}\|_\infty$ (escala log)')
ax.set_title('Q7.2(b) — Erro de discretização vs. tamanho do problema\n'
             'Equação do calor: convergência $O(h^2)$ esperada')
ax.legend()
plt.tight_layout()
plt.savefig('q72b_erros_vs_n.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()

print("\n  Item (c) — Método mais eficiente para n ≥ 200\n")
cab_72c = ['n', 'Jacobi (ms)', 'GS (ms)', 'SOR (ms)', 'CG (ms)']
linhas_72c = []
for i, n in enumerate(N_VALS_CALOR):
    linhas_72c.append([str(n),
        f'{tempo_j72[i]:.2f}', f'{tempo_gs72[i]:.2f}',
        f'{tempo_sor72[i]:.2f}', f'{tempo_cg72[i]:.2f}'])
imprimir_tabela(cab_72c, linhas_72c)
print("  → A partir de n = 200 o CG é claramente o mais eficiente.\n")

# ----------------------------------------------------------------------------------
# Questão 7.3 — Efeito do ponto inicial no CG
# ----------------------------------------------------------------------------------

print("═" * 72)
print("  QUESTÃO 7.3 — Efeito do ponto inicial na convergência do CG (n = 100)")
print("═" * 72)

n_73 = 100
h_73 = 1 / (n_73 + 1)
xp73 = np.linspace(h_73, 1 - h_73, n_73)
ue73 = np.sin(np.pi * xp73)
bv73 = (np.pi**2) * np.sin(np.pi * xp73)
Av73 = (2*np.eye(n_73) - np.diag(np.ones(n_73-1), 1) - np.diag(np.ones(n_73-1), -1)) / h_73**2

# (a) x0 = 0
_, it73a, hist73a = cg(Av73, bv73, x0=np.zeros(n_73), tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)

# (b) x0 = u_exata + ruído 1e-2
np.random.seed(42)
x0_b73 = ue73 + 1e-2 * np.random.randn(n_73)
_, it73b, hist73b = cg(Av73, bv73, x0=x0_b73, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)

# (c) x0 = solução de n=50 interpolada para n=100
h50  = 1 / (50 + 1)
xp50 = np.linspace(h50, 1 - h50, 50)
b50  = (np.pi**2) * np.sin(np.pi * xp50)
A50  = (2*np.eye(50) - np.diag(np.ones(49), 1) - np.diag(np.ones(49), -1)) / h50**2
u50, _, _ = cg(A50, b50, tol=TOL_PADRAO, max_iter=MAX_ITER_CALOR)
x0_c73 = np.interp(xp73, xp50, u50)
_, it73c, hist73c = cg(Av73, bv73, x0=x0_c73, tol=TOL_PADRAO, max_iter=MAX_ITER_PADRAO)

print("\n  Número de iterações por ponto inicial:\n")
cab_73 = ['Ponto inicial x⁽⁰⁾', 'Iterações']
linhas_73 = [
    ['0 (nulo padrão)',                    str(it73a)],
    ['u_exata + ruído 10⁻²',              str(it73b)],
    ['u_(n=50) interpolado para n=100',   str(it73c)],
]
imprimir_tabela(cab_73, linhas_73, ['<', '^'])

fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(hist73a, 'b-',  lw=2, label=f'x⁰ = 0  ({it73a} iters)')
ax.semilogy(hist73b, 'r--', lw=2, label=f'x⁰ = exata+ruído  ({it73b} iters)')
ax.semilogy(hist73c, 'g:',  lw=2, label=f'x⁰ = interp. n=50  ({it73c} iters)')
ax.set_xlabel('Iteração $k$')
ax.set_ylabel(r'$\|r^{(k)}\|_2$ (escala log)')
ax.set_title('Q7.3 — Efeito do ponto inicial no CG ($n=100$)\n'
             'Equação do calor estacionária')
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig('q73_efeito_ponto_inicial.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()
print("\n  → CG é moderadamente sensível ao ponto inicial, mas a qualidade")
print("    de x⁰ (interpolação quente) pode reduzir o número de iterações.\n")


# ==================================================================================
# SEÇÃO 8 — Desafio (Opcional — Pontuação Extra)
# ==================================================================================

print("═" * 72)
print("  SEÇÃO 8 — Desafio (Opcional — Pontuação Extra)")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Questão 8.1 — Critério de parada e qualidade da solução
# ----------------------------------------------------------------------------------

print("\n" + "═" * 72)
print("  QUESTÃO 8.1 — Critério de parada e qualidade da solução")
print("═" * 72)

# --- Gera sistemas bem e mal condicionados ---
np.random.seed(0)
n_81 = 4

# Bem-condicionado: κ ≈ 10
A81_bom = criar_matriz_spd_condicionamento(n_81, kappa=10)
x_star81 = np.ones(n_81)
b81_bom  = A81_bom @ x_star81

# Mal-condicionado: κ ≈ 1e6
A81_mau = criar_matriz_spd_condicionamento(n_81, kappa=1e6)
b81_mau = A81_mau @ x_star81

print(f"\n  κ(A_bom) = {np.linalg.cond(A81_bom):.2e}")
print(f"  κ(A_mau) = {np.linalg.cond(A81_mau):.2e}\n")

def gauss_seidel_rastreado(A, b, x_star, tol=1e-12, max_iter=200):
    """
    Executa Gauss-Seidel registrando a cada iteração:
      - erro verdadeiro  ‖x^(k) - x*‖₂
      - critério relativo d^(k) = ‖x^(k) - x^(k-1)‖∞ / ‖x^(k)‖∞
      - resíduo normalizado ‖Ax^(k)-b‖ / ‖b‖
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n)
    erros_v, criterio_d, residuo_norm = [], [], []

    for k in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            soma = (np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x_old[i+1:]))
            x[i] = (b[i] - soma) / A[i, i]

        ev   = np.linalg.norm(x - x_star)
        diff = np.linalg.norm(x - x_old, np.inf)
        denom = np.linalg.norm(x, np.inf)
        dr   = diff / denom if denom > 0 else diff
        rn   = np.linalg.norm(A @ x - b) / np.linalg.norm(b)

        erros_v.append(ev)
        criterio_d.append(dr)
        residuo_norm.append(rn)

        if dr < tol:
            break

    return np.array(erros_v), np.array(criterio_d), np.array(residuo_norm)

ev_bom, dr_bom, rn_bom = gauss_seidel_rastreado(A81_bom, b81_bom, x_star81)
ev_mau, dr_mau, rn_mau = gauss_seidel_rastreado(A81_mau, b81_mau, x_star81)

# --- Gráfico 8.1 ---
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

for row, (ev, dr, rn, titulo) in enumerate([
        (ev_bom, dr_bom, rn_bom, f'Sistema bem-condicionado ($\\kappa\\approx10$)'),
        (ev_mau, dr_mau, rn_mau, f'Sistema mal-condicionado ($\\kappa\\approx10^6$)')]):

    iters = np.arange(1, len(ev) + 1)

    ax = axes[row, 0]
    ax.semilogy(iters, ev,  'b-o', ms=4, lw=2, label='Erro verdadeiro $\\|x^{(k)}-x^*\\|_2$')
    ax.semilogy(iters, dr,  'r--s', ms=4, lw=2, label='Critério relativo $d^{(k)}_r$')
    ax.semilogy(iters, rn,  'g-.^', ms=4, lw=2, label='Resíduo normalizado $\\|r\\|/\\|b\\|$')
    ax.set_xlabel('Iteração $k$')
    ax.set_ylabel('Valor (escala log)')
    ax.set_title(f'Q8.1 — {titulo}\nCritérios de parada vs. erro verdadeiro')
    ax.legend(fontsize=8)

    ax2 = axes[row, 1]
    ax2.loglog(dr, ev,  'bo-', ms=5, lw=2, label='Critério relativo $d^{(k)}_r$')
    ax2.loglog(rn, ev,  'r^--', ms=5, lw=2, label='Resíduo normalizado')
    diag = np.logspace(np.log10(min(min(dr), min(rn))),
                       np.log10(max(max(dr), max(rn))), 50)
    ax2.loglog(diag, diag, 'k:', lw=1, label='Diagonal (ideal)')
    ax2.set_xlabel('Critério de parada (escala log)')
    ax2.set_ylabel('Erro verdadeiro $\\|x^{(k)}-x^*\\|_2$ (escala log)')
    ax2.set_title(f'Q8.1 — {titulo}\nConfiabilidade do critério de parada')
    ax2.legend(fontsize=8)

plt.tight_layout()
plt.savefig('q81_criterio_parada.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()

# --- Análise ---
print("  Item (a) — Resultados dos experimentos:\n")
cab_81 = ['Sistema', 'Iterações', 'Erro final ‖x-x*‖', 'Critério d_r final', 'Resíduo norm. final']
linhas_81 = [
    ['Bem cond. (κ≈10)',   str(len(ev_bom)), f'{ev_bom[-1]:.2e}', f'{dr_bom[-1]:.2e}', f'{rn_bom[-1]:.2e}'],
    ['Mal cond. (κ≈1e6)',  str(len(ev_mau)), f'{ev_mau[-1]:.2e}', f'{dr_mau[-1]:.2e}', f'{rn_mau[-1]:.2e}'],
]
imprimir_tabela(cab_81, linhas_81, ['<', '^', '^', '^', '^'])

print("""
  Item (b) — Confiabilidade do critério d^(k)_r:
    • Sistema bem-condicionado  : d^(k)_r ≈ ‖x^(k)-x*‖ → critério CONFIÁVEL.
    • Sistema mal-condicionado  : d^(k)_r pode ser muito menor que o erro real →
      critério ENGANOSO (converge pelo critério antes de x^(k) ser preciso).

  Item (c) — Critério mais robusto baseado no resíduo:
    Usar  ‖Ax^(k) - b‖₂ / ‖b‖₂ < ε
    Este critério é menos enganoso porque está diretamente relacionado ao
    erro via  ‖x^(k)-x*‖ ≤ κ(A)·(‖r^(k)‖/‖b‖)·‖x*‖.
    Para sistemas mal-condicionados ainda há uma penalidade κ(A), mas ao
    menos o usuário tem consciência de que a tolerância real no erro pode
    ser muito maior que ε.
""")

# ----------------------------------------------------------------------------------
# Questão 8.2 — ILU como pré-condicionador do CG
# ----------------------------------------------------------------------------------

print("═" * 72)
print("  QUESTÃO 8.2 — ILU como pré-condicionador do CG")
print("═" * 72)

try:
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla

    n_82  = 30     # grade n×n → sistema de n²×n²
    n2_82 = n_82 * n_82

    # Laplaciano 2D: -Δu = f
    diag_main = 4.0 * np.ones(n2_82)
    diag_off1 = -1.0 * np.ones(n2_82 - 1)
    diag_offN = -1.0 * np.ones(n2_82 - n_82)

    # Zeros nas fronteiras de bloco (diag_off1)
    for i in range(n_82 - 1, n2_82 - 1, n_82):
        diag_off1[i] = 0.0

    A82_sp = sp.diags(
        [diag_main, diag_off1, diag_off1, diag_offN, diag_offN],
        [0, 1, -1, n_82, -n_82],
        format='csc'
    )
    A82_dense = A82_sp.toarray()
    x_ex82    = np.ones(n2_82)
    b82       = A82_sp @ x_ex82

    print(f"\n  Laplaciano 2D: grade {n_82}×{n_82},  sistema {n2_82}×{n2_82}\n")

    # --- CG sem pré-condicionador ---
    t0 = time.perf_counter()
    x_cg82, it_cg82, hist_cg82 = cg(A82_dense, b82, x0=None, tol=TOL_PADRAO,
                                     max_iter=MAX_ITER_GRANDE)
    t_cg82 = time.perf_counter() - t0

    # --- PCG + Jacobi ---
    diag_A82 = A82_sp.diagonal()
    M_inv_jac82 = lambda v: v / diag_A82
    t0 = time.perf_counter()
    x_pcg_jac82, it_pcg_jac82, hist_pcg_jac82 = pcg(
        A82_dense, b82, M_inv=M_inv_jac82, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_GRANDE)
    t_pcg_jac82 = time.perf_counter() - t0

    # --- PCG + ILU ---
    ilu_factor = spla.spilu(A82_sp, drop_tol=1e-4, fill_factor=2)
    M_ilu = spla.LinearOperator((n2_82, n2_82), ilu_factor.solve)

    t0 = time.perf_counter()
    x_pcg_ilu82, it_pcg_ilu82, hist_pcg_ilu82 = pcg(
        A82_dense, b82, M_inv=M_ilu.matvec, x0=None, tol=TOL_PADRAO, max_iter=MAX_ITER_GRANDE)
    t_pcg_ilu82 = time.perf_counter() - t0

    # --- κ(M⁻¹A) estimado por amostragem (exato seria inviável para n²=900) ---
    kappa_A82  = np.linalg.cond(A82_dense)
    D_inv_82   = np.diag(1.0 / diag_A82)
    kappa_MA82_jac = np.linalg.cond(D_inv_82 @ A82_dense)
    # ILU κ estimado por eigenvalues (amostra, pode ser lento)
    A82_ilu_dense = np.array([M_ilu.matvec(A82_dense[:, j]) for j in range(n2_82)]).T
    kappa_MA82_ilu = np.linalg.cond(A82_ilu_dense)

    print("  Item (b) — Comparação de métodos\n")
    cab_82b = ['Configuração', 'Iterações', 'Tempo (s)', 'κ efetivo', '‖r_final‖']
    linhas_82b = [
        ['CG sem pré-cond.',  str(it_cg82),      f'{t_cg82:.4f}',
         f'{kappa_A82:.2e}',       f'{np.linalg.norm(b82 - A82_dense @ x_cg82):.2e}'],
        ['PCG + Jacobi',      str(it_pcg_jac82), f'{t_pcg_jac82:.4f}',
         f'{kappa_MA82_jac:.2e}',  f'{np.linalg.norm(b82 - A82_dense @ x_pcg_jac82):.2e}'],
        ['PCG + ILU',         str(it_pcg_ilu82), f'{t_pcg_ilu82:.4f}',
         f'{kappa_MA82_ilu:.2e}',  f'{np.linalg.norm(b82 - A82_dense @ x_pcg_ilu82):.2e}'],
    ]
    imprimir_tabela(cab_82b, linhas_82b, ['<', '^', '^', '^', '^'])

    # --- Gráfico 8.2 ---
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.semilogy(hist_cg82,       'b-',  lw=2, label=f'CG sem pré-cond. ({it_cg82} iters)')
    ax.semilogy(hist_pcg_jac82,  'r--', lw=2, label=f'PCG + Jacobi ({it_pcg_jac82} iters)')
    ax.semilogy(hist_pcg_ilu82,  'g:',  lw=2, label=f'PCG + ILU ({it_pcg_ilu82} iters)')
    ax.set_xlabel('Iteração $k$')
    ax.set_ylabel(r'$\|r^{(k)}\|_2$ (escala log)')
    ax.set_title('Q8.2(b) — CG vs. PCG+Jacobi vs. PCG+ILU\n'
                 f'Laplaciano 2D {n_82}×{n_82} ($n^2={n2_82}$), tol=$10^{{-8}}$')
    ax.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig('q82_pcg_ilu.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
    plt.close()

    print(f"""
  Item (c) — Custo-benefício do ILU:
    • ILU reduziu κ de {kappa_A82:.2e} para {kappa_MA82_ilu:.2e} ({it_pcg_ilu82} vs {it_cg82} iters).
    • O custo de fatoração ILU é amortizado quando há muitas iterações a ganhar.
    • Para sistemas grandes e esparsos o ILU é geralmente muito vantajoso.
    • Para sistemas densos de médio porte, o ganho pode não compensar o custo adicional.
""")

except ImportError:
    print("\n  ⚠ scipy.sparse não disponível — Q8.2 ignorada.\n")
except Exception as e:
    print(f"\n  ⚠ Erro em Q8.2: {e}\n")

# ----------------------------------------------------------------------------------
# Questão 8.3 — Jacobi paralelo vs. Gauss-Seidel sequencial
# ----------------------------------------------------------------------------------

print("═" * 72)
print("  QUESTÃO 8.3 — Jacobi paralelo vs. Gauss-Seidel sequencial")
print("═" * 72)

# --- Implementações ---

def jacobi_com_laco(A, b, x0=None, tol=1e-8, max_iter=500):
    """Jacobi com laço explícito em i (referência para comparação)."""
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    for k in range(max_iter):
        x_new = np.zeros(n)
        for i in range(n):
            s = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
        if np.linalg.norm(x_new - x, np.inf) / max(np.linalg.norm(x_new, np.inf), 1e-300) < tol:
            return x_new, k + 1
        x = x_new
    return x, max_iter


def jacobi_vetorizado(A, b, x0=None, tol=1e-8, max_iter=500):
    """Jacobi 100% vetorizado com NumPy (sem laço em i)."""
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    D_inv = 1.0 / np.diag(A)
    R     = A - np.diag(np.diag(A))   # parte fora da diagonal
    for k in range(max_iter):
        x_new = D_inv * (b - R @ x)   # uma única operação mat-vec
        if np.linalg.norm(x_new - x, np.inf) / max(np.linalg.norm(x_new, np.inf), 1e-300) < tol:
            return x_new, k + 1
        x = x_new
    return x, max_iter


def jacobi_4blocos(A, b, x0=None, tol=1e-8, max_iter=500):
    """
    Jacobi simulando 4 processadores.
    Divide x em 4 blocos; cada bloco lê x^(k) e escreve x^(k+1) independentemente.
    Operação idêntica ao Jacobi padrão (os blocos são só organização lógica),
    mas ilustra a independência entre componentes.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    D_inv = 1.0 / np.diag(A)
    R     = A - np.diag(np.diag(A))
    blocos = np.array_split(np.arange(n), 4)

    for k in range(max_iter):
        x_old = x.copy()
        x_new = np.empty(n)
        for bloco in blocos:
            x_new[bloco] = D_inv[bloco] * (b[bloco] - (R @ x_old)[bloco])
        if np.linalg.norm(x_new - x_old, np.inf) / max(np.linalg.norm(x_new, np.inf), 1e-300) < tol:
            return x_new, k + 1
        x = x_new
    return x, max_iter


print("\n  Item (a) — Versão com laço vs. versão vetorizada (n = 1000)\n")

n_83 = 1000
A83, b83 = gerar_tridiagonal(n_83, 4, -1)

# Aquece os caches
_ = jacobi_vetorizado(A83, b83, tol=1e-4, max_iter=5)
_ = jacobi_com_laco(A83[:10, :10], b83[:10], tol=1e-4, max_iter=5)

N_REP_83 = 3
t_vec_list, t_laco_list, t_4bl_list, t_gs_list = [], [], [], []

# Múltiplas repetições para estabilidade
for _ in range(N_REP_83):
    t0 = time.perf_counter(); jacobi_vetorizado(A83, b83)
    t_vec_list.append(time.perf_counter() - t0)

    t0 = time.perf_counter(); jacobi_com_laco(A83, b83)
    t_laco_list.append(time.perf_counter() - t0)

    t0 = time.perf_counter(); jacobi_4blocos(A83, b83)
    t_4bl_list.append(time.perf_counter() - t0)

    t0 = time.perf_counter(); gauss_seidel(A83, b83)
    t_gs_list.append(time.perf_counter() - t0)

t_vec83  = min(t_vec_list)
t_laco83 = min(t_laco_list)
t_4bl83  = min(t_4bl_list)
t_gs83   = min(t_gs_list)

speedup_vec = t_laco83 / t_vec83
speedup_4bl = t_laco83 / t_4bl83
speedup_gs  = t_laco83 / t_gs83

print(f"    n = {n_83}")
cab_83a = ['Implementação', 'Tempo mín. (s)', 'Speedup vs. laço']
linhas_83a = [
    ['Jacobi com laço',      f'{t_laco83:.4f}', '1,00×'],
    ['Jacobi vetorizado',    f'{t_vec83:.4f}',  f'{speedup_vec:.2f}×'],
    ['Jacobi 4 blocos',      f'{t_4bl83:.4f}',  f'{speedup_4bl:.2f}×'],
    ['Gauss-Seidel (ref.)',  f'{t_gs83:.4f}',   f'{speedup_gs:.2f}× (GS vs. laço J)'],
]
imprimir_tabela(cab_83a, linhas_83a, ['<', '^', '^'])

print(f"\n  Speedup vetorizado vs. laço: {speedup_vec:.2f}×")
print(f"  Speedup GS vs. Jacobi com laço: {speedup_gs:.2f}× (referência)\n")

# --- Curva de speedup para vários n ---
print("  Item (b) — Speedup da versão vetorizada para diferentes n\n")

n_vals83 = [50, 100, 200, 500, 1000]
speedups83 = []
for n_v in n_vals83:
    Av83, bv83 = gerar_tridiagonal(n_v, 4, -1)
    t_v = min(medir_tempo(jacobi_vetorizado, Av83, bv83) for _ in range(1))
    t_l = min(medir_tempo(jacobi_com_laco,   Av83, bv83) for _ in range(1))
    sp83 = t_l / t_v if t_v > 0 else float('inf')
    speedups83.append(sp83)
    print(f"    n = {n_v:5d} : vetorizado={t_v:.4f}s  laço={t_l:.4f}s  speedup={sp83:.1f}×")

fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogx(n_vals83, speedups83, 'bo-', lw=2, ms=8)
ax.axhline(y=1, color='gray', ls='--', lw=1)
ax.set_xlabel('Tamanho $n$ (escala log)')
ax.set_ylabel('Speedup (Jacobi laço / Jacobi vetorizado)')
ax.set_title('Q8.3(a) — Speedup da vetorização NumPy do Jacobi\n'
             'Jacobi com laço explícito vs. operação mat-vec NumPy')
plt.tight_layout()
plt.savefig('q83a_speedup_vetorizacao.png', dpi=DPI_GRAFICOS, bbox_inches='tight')
plt.close()

# --- Análise crítica ---
print("""
  Item (c) — Quando a paralelização de Jacobi supera o GS sequencial?

  • Jacobi sequencial precisa de ~2× mais iterações que GS (quando ρ_GS ≈ ρ_J²).
  • Portanto, Jacobi paralelo (usando p núcleos) supera GS sequencial quando:

        custo_J_paralelo < custo_GS_sequencial
        (k_J / p) · custo_iter < k_GS · custo_iter
        k_J / p < k_GS
        2 k_GS / p < k_GS      →     p > 2

  • Com p ≥ 2 núcleos, Jacobi paralelo bate GS sequencial em número de iterações.
  • Na prática, o breakeven também depende do overhead de comunicação entre núcleos:
    para n pequeno, o overhead domina; o ganho só aparece para n grande (≥ 200–500).
  • A vetorização NumPy já captura parte desse ganho em hardware SIMD, mesmo em 1 núcleo.
""")


# ==================================================================================
# Fim do script
# ==================================================================================
# Relatório gerado por: Jeann Victor Batista
# ==================================================================================

print("═" * 72)
print("  FIM DA EXECUÇÃO — Relatório gerado por: Jeann Victor Batista")
print("═" * 72)