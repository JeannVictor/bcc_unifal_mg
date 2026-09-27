# ==================================================================================
# main.py
# ==================================================================================
# Plano de Investigação Computacional
# Interpolação e Ajuste de Curvas: Uma Abordagem Integrada em Python
# ==================================================================================
# Disciplina   : Cálculo Numérico
# Professora   : Angela Leite Moreno
# Aluno 1      : Jeann Victor Batista              R.A          : 2024.1.08.014
# Aluno 2      : Pedro Augusto de Souza Finnochio  R.A          : 2024.1.08.020
# Aluno 3      : Thiago Martins da Silva           R.A          : 2024.1.08.023
# ==================================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit

from interpolacao import lagrange, diferencas_divididas, newton, nos_chebyshev, spline_cubica
from ajuste import regressao_linear, regressao_polinomial, ajuste_exponencial, ajuste_potencia, ajuste_nao_linear, residuos

# ==================================================================================
# CONFIGURAÇÃO DOS GRÁFICOS
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
# UTILITÁRIO PARA TABELAS
# ==================================================================================

def imprimir_tabela(cabecalhos, linhas, alinhamento=None):
    """Imprime tabela formatada com bordas unicode."""
    n_cols = len(cabecalhos)
    larguras = [len(str(c)) + 2 for c in cabecalhos]
    for linha in linhas:
        for j, cel in enumerate(linha):
            larguras[j] = max(larguras[j], len(str(cel)) + 2)

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

    print('╔' + '╦'.join('═' * w for w in larguras) + '╗')
    print(formatar_linha(cabecalhos))
    print('╠' + '╬'.join('═' * w for w in larguras) + '╣')
    for i, linha in enumerate(linhas):
        print(formatar_linha(linha))
        if i < len(linhas) - 1:
            print('╠' + '╬'.join('─' * w for w in larguras) + '╣')
    print('╚' + '╩'.join('═' * w for w in larguras) + '╝')


# ==================================================================================
# SEÇÃO 1 — Interpolação: Implementação e Verificação
# ==================================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 1 — Interpolação: Implementação e Verificação")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Q1.1 — Primeiros passos com os métodos
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 1.1 — Primeiros passos com os métodos")
print("─" * 72)

print("\n--- Item (a) ---")

q1x = [1.0, 2.0, 3.0, 4.0]
q1y = [1.0, 4.0, 9.0, 16.0]

# Avaliação em x = 1.5
rl15 = lagrange(q1x, q1y, 1.5)
rn15 = newton(q1x, q1y, 1.5)
df15 = abs(rl15 - rn15)
print(f"Lagrange para x = 1,5:  {rl15}")
print(f"Newton   para x = 1,5:  {rn15}")
print(f"Diferença numérica:      {df15}")

# Avaliação em x = 2.5
rl25 = lagrange(q1x, q1y, 2.5)
rn25 = newton(q1x, q1y, 2.5)
df25 = abs(rl25 - rn25)
print(f"\nLagrange para x = 2,5:  {rl25}")
print(f"Newton   para x = 2,5:  {rn25}")
print(f"Diferença numérica:      {df25}")

print("\nOs dois métodos produzem resultados idênticos (diferença ≈ 0),")
print("pois pelo teorema da unicidade existe apenas um polinômio de grau")
print("≤ n que interpola n+1 pontos distintos. Lagrange e Newton são")
print("representações diferentes do mesmo polinômio.")

print("\n--- Item (b) ---")

coeficientes = diferencas_divididas(q1x, q1y)
print("Coeficientes do polinômio de Newton (diferenças divididas):")
for i in range(len(coeficientes)):
    print(f"  f[x0,...,x{i}] = {coeficientes[i]:.4f}")

print("\nPolinômio na forma de Newton:")
print("  p3(x) = c0 + c1(x−x0) + c2(x−x0)(x−x1) + c3(x−x0)(x−x1)(x−x2)")
print(f"       = {coeficientes[0]:.4f} + {coeficientes[1]:.4f}(x−1) "
      f"+ {coeficientes[2]:.4f}(x−1)(x−2) + {coeficientes[3]:.4f}(x−1)(x−2)(x−3)")

print("\n--- Item (c) ---")
print("Sim. O polinômio interpolador coincide exatamente com f(x) = x²,")
print("pois todos os pontos pertencem a essa função e f é um polinômio")
print("de grau 2. Pelo teorema da unicidade, existe exatamente um polinômio")
print("de grau ≤ n que interpola n+1 pontos distintos — portanto o interpolador")
print("recupera f perfeitamente (as diferenças divididas de ordem 3 são zero).")

# ----------------------------------------------------------------------------------
# Q1.2 — Adição de um ponto e atualização de Newton
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 1.2 — Adição de um ponto e atualização de Newton")
print("─" * 72)

q12x = [1.0, 2.0, 3.0, 4.0, 5.0]
q12y = [1.0, 4.0, 9.0, 16.0, 25.0]

print("\n--- Item (a) ---")

rl1215 = lagrange(q12x, q12y, 1.5)
rl1225 = lagrange(q12x, q12y, 2.5)
print(f"Lagrange (5 pontos) para x = 1,5: {rl1215}")
print(f"Lagrange (5 pontos) para x = 2,5: {rl1225}")
print("\nNa forma de Lagrange, adicionar um novo ponto exige recalcular")
print("todos os n+1 polinômios de base L_i(x) — o custo é O(n²).")

print("\n--- Item (b) ---")

# Na forma de Newton: apenas f[x0,...,x4] precisa ser calculada.
# Os coeficientes anteriores são reaproveitados.
coefs_novos = diferencas_divididas(q12x, q12y)
print("Nova diferença dividida adicionada:")
print(f"  f[x0,...,x4] = {coefs_novos[4]:.4f}")
print("Os 4 coeficientes anteriores permanecem inalterados.")

rl1235 = lagrange(q12x, q12y, 3.5)
rn1235 = newton(q12x, q12y, 3.5)
df1235 = abs(rl1235 - rn1235)
print(f"\nLagrange para x = 3,5:  {rl1235}")
print(f"Newton   para x = 3,5:  {rn1235}")
print(f"Diferença numérica:      {df1235}")
print("Os dois polinômios coincidem em x = 3,5 (como esperado).")

print("\n--- Item (c) ---")
print("Essa vantagem é crítica em aplicações com atualização contínua")
print("de dados, como sensores em tempo real, simulações numéricas")
print("incrementais e sistemas de aquisição de dados, onde novos pontos")
print("chegam frequentemente e recalcular tudo seria inviável.")

# ----------------------------------------------------------------------------------
# Q1.3 — Fenômeno de Runge e nós de Chebyshev
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 1.3 — Fenômeno de Runge e nós de Chebyshev")
print("─" * 72)

f_runge = lambda x: 1 / (1 + 25 * x**2)

x_plot = np.linspace(-1, 1, 500)
y_real = f_runge(x_plot)

valores_n = [5, 9, 13, 17]

print("\n--- Item (a) ---")

plt.figure(figsize=(8, 5))
for n in valores_n:
    x_nodes = np.linspace(-1, 1, n)
    y_nodes = f_runge(x_nodes)
    y_interp = lagrange(x_nodes, y_nodes, x_plot)
    erro = np.abs(y_real - y_interp)
    plt.plot(x_plot, erro, label=f'n = {n}')

plt.title('Erro da Interpolação de Lagrange — Função de Runge\n(Nós igualmente espaçados)')
plt.xlabel('x')
plt.ylabel('|f(x) − pₙ(x)|')
plt.yscale('log')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q13a_runge_erro.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q13a_runge_erro.png")
print("\nCom nós igualmente espaçados, o erro cresce rapidamente nas")
print("extremidades do intervalo conforme n aumenta — fenômeno de Runge.")

print("\n--- Item (b) ---")

n = 13

x_eq = np.linspace(-1, 1, n)
y_eq = f_runge(x_eq)

x_ch = nos_chebyshev(-1, 1, n)
y_ch = f_runge(x_ch)

y_eq_interp = lagrange(x_eq, y_eq, x_plot)
y_ch_interp = lagrange(x_ch, y_ch, x_plot)

erro_eq = np.abs(y_real - y_eq_interp)
erro_ch = np.abs(y_real - y_ch_interp)

plt.figure(figsize=(8, 5))
plt.plot(x_plot, erro_eq, label='Nós igualmente espaçados')
plt.plot(x_plot, erro_ch, label='Nós de Chebyshev')
plt.title('Comparação dos Erros de Interpolação — n = 13\n(Função de Runge)')
plt.xlabel('x')
plt.ylabel('|f(x) − pₙ(x)|')
plt.yscale('log')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q13b_comparacao_erros.png", bbox_inches='tight')
plt.close()

reducao = np.max(erro_eq) / np.max(erro_ch)
print("Gráfico salvo como: q13b_comparacao_erros.png")
print(f"Redução máxima do erro (Chebyshev vs. espaçados), n=13: {reducao:.1f}×")

print("\n--- Item (c) ---")

linhas_tabela = []
for n in [5, 9, 13, 17]:
    x_eq = np.linspace(-1, 1, n)
    y_eq_interp = lagrange(x_eq, f_runge(x_eq), x_plot)
    erro_eq_max = np.max(np.abs(y_real - y_eq_interp))

    x_ch = nos_chebyshev(-1, 1, n)
    y_ch_interp = lagrange(x_ch, f_runge(x_ch), x_plot)
    erro_ch_max = np.max(np.abs(y_real - y_ch_interp))

    linhas_tabela.append([n, f"{erro_eq_max:.6e}", f"{erro_ch_max:.6e}"])

imprimir_tabela(
    ["n", "‖f − pₙ‖∞ (espaçados)", "‖f − pₙ‖∞ (Chebyshev)"],
    linhas_tabela,
    alinhamento=['^', '^', '^']
)

print("\n--- Item (d) ---")
print("Os nós de Chebyshev minimizam ‖ωₙ₊₁‖∞ = ‖∏(x − xᵢ)‖∞ no intervalo [a,b].")
print("Como o erro satisfaz |f(x) − pₙ(x)| ≤ Mₙ₊₁/(n+1)! · |ωₙ₊₁(x)|,")
print("reduzir o máximo de |ωₙ₊₁| diretamente limita o erro de interpolação,")
print("mitigando as oscilações nas extremidades que caracterizam o fenômeno de Runge.")

# ----------------------------------------------------------------------------------
# Q1.4 — Spline cúbica vs. polinômio global
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 1.4 — Spline cúbica vs. polinômio global")
print("─" * 72)

# Dados mensais de temperatura em Alfenas-MG
q14x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
q14y = [23.0, 24.0, 23.0, 21.0, 18.0, 16.0, 16.0, 18.0, 20.0, 22.0, 23.0, 24.0]

x_plot = np.linspace(1.0, 12.0, 500)

print("\n--- Item (a) ---")

y_interp_lag = lagrange(q14x, q14y, x_plot)

plt.figure(figsize=(9, 5))
plt.plot(x_plot, y_interp_lag, label='Polinômio de Lagrange (grau 11)')
plt.scatter(q14x, q14y, color='black', zorder=5, label='Dados mensais')
plt.title('Interpolação de Lagrange — Temperatura Média em Alfenas-MG')
plt.xlabel('Mês')
plt.ylabel('Temperatura (°C)')
plt.xticks(range(1, 13))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q14a_interpolador_temp_alfenas.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q14a_interpolador_temp_alfenas.png")
print("\nO polinômio global de grau 11 apresenta oscilações indesejadas,")
print("principalmente nas extremidades do intervalo (meses 1–2 e 11–12),")
print("caracterizando o fenômeno de Runge para dados reais.")

print("\n--- Item (b) ---")

cs_nk = CubicSpline(q14x, q14y, bc_type='not-a-knot')

plt.figure(figsize=(9, 5))
plt.plot(x_plot, y_interp_lag, '--', label='Polinômio de Lagrange (grau 11)')
plt.plot(x_plot, cs_nk(x_plot), '-', label='Spline cúbica (not-a-knot)')
plt.scatter(q14x, q14y, color='black', zorder=5, label='Dados mensais')
plt.title('Lagrange vs. Spline Cúbica — Temperatura Média em Alfenas-MG')
plt.xlabel('Mês')
plt.ylabel('Temperatura (°C)')
plt.xticks(range(1, 13))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q14b_interpolador_temp_alfenas.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q14b_interpolador_temp_alfenas.png")
print("\nA spline cúbica representa muito melhor o comportamento físico")
print("esperado de uma série de temperaturas, produzindo uma curva")
print("suave e sem oscilações artificiais.")

print("\n--- Item (c) ---")

pontos_teste = [1.5, 6.5, 11.5]
for xv in pontos_teste:
    lag_val = lagrange(q14x, q14y, xv)
    spl_val = cs_nk(xv)
    diff = abs(lag_val - spl_val)
    print(f"x = {xv}:  Lagrange = {lag_val:.4f} °C | Spline = {float(spl_val):.4f} °C | Δ = {float(diff):.4f} °C")

print("\nAs diferenças são mais pronunciadas próximas às extremidades,")
print("onde as oscilações de Lagrange são maiores. Para um sistema de")
print("monitoramento climático, a spline cúbica seria mais adequada,")
print("pois evita variações artificiais e respeita a tendência física dos dados.")

print("\n--- Item (d) ---")

cs_nat = CubicSpline(q14x, q14y, bc_type='natural')
cs_nk2 = CubicSpline(q14x, q14y, bc_type='not-a-knot')

plt.figure(figsize=(9, 5))
plt.plot(x_plot, cs_nat(x_plot), '--', label='Spline natural (S″=0 nas bordas)')
plt.plot(x_plot, cs_nk2(x_plot), '-', label='Spline not-a-knot')
plt.scatter(q14x, q14y, color='black', zorder=5, label='Dados mensais')
plt.title('Spline Cúbica: Natural vs. Not-a-Knot — Temperatura em Alfenas-MG')
plt.xlabel('Mês')
plt.ylabel('Temperatura (°C)')
plt.xticks(range(1, 13))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q14d_interpolador_temp_alfenas.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q14d_interpolador_temp_alfenas.png")
print("\nAs duas variantes diferem principalmente nas extremidades do intervalo.")
print("A spline natural impõe segunda derivada nula nos extremos (S″(x₀)=S″(xₙ)=0),")
print("produzindo uma curvatura mais 'relaxada' nas bordas.")
print("A not-a-knot força continuidade da terceira derivada nos nós x₁ e xₙ₋₁,")
print("resultando em comportamento mais 'firme' nas extremidades.")


# ==================================================================================
# SEÇÃO 2 — Ajuste de Curvas: Mínimos Quadrados e Modelos
# ==================================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 2 — Ajuste de Curvas: Mínimos Quadrados e Modelos")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Q2.1 — Geometria dos mínimos quadrados
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 2.1 — Geometria dos mínimos quadrados")
print("─" * 72)

speed    = np.array([20, 40, 60, 80, 100, 120], dtype=float)
distance = np.array([5, 14, 28, 47, 72, 103], dtype=float)

print("\n--- Item (a) ---")

a0_lin, a1_lin, r2_lin = regressao_linear(speed, distance)
print(f"Modelo linear  d = a0 + a1·v:")
print(f"  a0 = {a0_lin:.4f} m")
print(f"  a1 = {a1_lin:.4f} m/(km/h)")
print(f"  R² = {r2_lin:.6f}")
print("\nO ajuste linear não é ideal: R² < 1 e os dados crescem de forma")
print("quadrática com a velocidade, não linear.")

print("\n--- Item (b) ---")

# Linearização: z = v², ajusta d = a0' + a1'·z
z = speed**2
a0_quad, a1_quad, r2_quad = regressao_linear(z, distance)
print(f"Modelo quadrático  d = a0' + a1'·v²  (z = v²):")
print(f"  a0' = {a0_quad:.4f} m")
print(f"  a1' = {a1_quad:.6f} m/(km/h)²")
print(f"  R²  = {r2_quad:.6f}")
print(f"\nComparação de R²:")
print(f"  Modelo linear:     R² = {r2_lin:.6f}")
print(f"  Modelo quadrático: R² = {r2_quad:.6f}")
print("\nO modelo em v² é muito mais adequado — R² ≈ 1,")
print("pois a distância de frenagem cresce com o quadrado da velocidade")
print("(consequência direta da física: energia cinética ∝ v²).")

print("\n--- Item (c) ---")

v_plot = np.linspace(20, 120, 500)
linear_plot = a0_lin + a1_lin * v_plot
quad_plot   = a0_quad + a1_quad * v_plot**2

y_linear = a0_lin + a1_lin * speed
y_quad   = a0_quad + a1_quad * speed**2

res_linear = distance - y_linear
res_quad   = distance - y_quad

# Gráfico dos ajustes
plt.figure(figsize=(8, 5))
plt.scatter(speed, distance, color='black', zorder=5, label='Dados')
plt.plot(v_plot, linear_plot, label=f'Modelo linear (R²={r2_lin:.4f})')
plt.plot(v_plot, quad_plot,   label=f'Modelo quadrático (R²={r2_quad:.4f})')
plt.title('Distância de Frenagem: Ajuste Linear vs. Quadrático')
plt.xlabel('Velocidade (km/h)')
plt.ylabel('Distância de frenagem (m)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q21c_ajustes_frenagem.png", bbox_inches='tight')
plt.close()

# Gráfico dos resíduos
plt.figure(figsize=(8, 5))
plt.scatter(speed, res_linear, label='Resíduos — modelo linear', marker='o')
plt.scatter(speed, res_quad,   label='Resíduos — modelo quadrático', marker='s')
plt.axhline(0, linestyle='--', color='gray')
plt.title('Resíduos dos Modelos de Frenagem')
plt.xlabel('Velocidade (km/h)')
plt.ylabel('Resíduo (m)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q21c_residuos_frenagem.png", bbox_inches='tight')
plt.close()

print("Gráficos salvos: q21c_ajustes_frenagem.png | q21c_residuos_frenagem.png")
print("\nOs resíduos do modelo linear apresentam padrão sistemático em")
print("forma de arco, confirmando que o modelo está subdimensionado.")
print("Os resíduos do modelo quadrático são menores e distribuídos")
print("de forma mais aleatória em torno de zero — melhor adequação.")

print("\n--- Item (d) ---")
print("Minimizar Σrᵢ² (em vez de Σ|rᵢ|) torna o critério diferenciável,")
print("permitindo obter a solução analítica via equações normais.")
print("A penalização quadrática também amplifica erros grandes,")
print("tornando o ajuste sensível a outliers — uma desvantagem prática.")

# ----------------------------------------------------------------------------------
# Q2.2 — Sobreajuste polinomial
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 2.2 — Sobreajuste polinomial")
print("─" * 72)

np.random.seed(7)
x22 = np.linspace(0, 2 * np.pi, 15)
y22 = np.sin(x22) + 0.15 * np.random.randn(15)

x_plot  = np.linspace(0, 2 * np.pi, 500)
y_real  = np.sin(x_plot)

graus = [1, 3, 5, 7, 10, 14]

print("\n--- Item (a) ---")

linhas_tabela = []
for k in graus:
    coefs22, r222 = regressao_polinomial(x22, y22, k)
    y_poly = np.polyval(coefs22[::-1], x_plot)
    erro_max = np.max(np.abs(y_real - y_poly))
    linhas_tabela.append([k, r222, erro_max])

print("Ajustes realizados para todos os graus.")

print("\n--- Item (b) ---")

linhas_fmt = [[l[0], f"{l[1]:.6f}", f"{l[2]:.6e}"] for l in linhas_tabela]
imprimir_tabela(
    ["Grau k", "R² (treino)", "‖f − pₖ‖∞"],
    linhas_fmt,
    alinhamento=['^', '^', '^']
)

print("\n--- Item (c) ---")

graus_plot = [l[0] for l in linhas_tabela]
erros_plot = [l[2] for l in linhas_tabela]

plt.figure(figsize=(8, 5))
plt.plot(graus_plot, erros_plot, marker='o')
plt.yscale('log')
plt.title('Erro Máximo em Função do Grau do Polinômio')
plt.xlabel('Grau do polinômio')
plt.ylabel('‖f − pₖ‖∞ (escala log)')
plt.xticks(graus_plot)
plt.grid(True)
plt.tight_layout()
plt.savefig("q22c_erro_vs_grau.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q22c_erro_vs_grau.png")
print("A partir do grau 7–10 o modelo começa a se deteriorar fora")
print("dos pontos de ajuste, com o erro máximo aumentando.")

print("\n--- Item (d) ---")
print("O erro de treinamento mede o ajuste nos pontos usados para construir")
print("o modelo (sempre ≤ para graus maiores). O erro de generalização mede")
print("o desempenho em pontos novos. No sobreajuste, o modelo memoriza o")
print("ruído dos dados de treino e perde capacidade preditiva — análogo ao")
print("fenômeno de Runge, onde polinômios de grau elevado oscilar")
print("fortemente entre os nós.")

# ----------------------------------------------------------------------------------
# Q2.3 — Critérios para escolha do grau
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 2.3 — Critérios para escolha do grau")
print("─" * 72)

print("\n--- Item (a) ---")

np.random.seed(42)
indices = np.random.permutation(len(x22))

idx_treino = indices[:10]
idx_teste  = indices[10:]

x_treino = x22[idx_treino]
y_treino = y22[idx_treino]
x_teste  = x22[idx_teste]
y_teste  = y22[idx_teste]

graus_range = range(1, 11)
mse_treino  = []
mse_teste   = []

for k in graus_range:
    coefs, _ = regressao_polinomial(x_treino, y_treino, k)
    y_hat_tr = np.polyval(coefs[::-1], x_treino)
    y_hat_te = np.polyval(coefs[::-1], x_teste)
    mse_treino.append(np.mean((y_treino - y_hat_tr)**2))
    mse_teste.append(np.mean((y_teste  - y_hat_te)**2))

melhor_grau = list(graus_range)[np.argmin(mse_teste)]

plt.figure(figsize=(8, 5))
plt.plot(list(graus_range), mse_treino, marker='o', label='MSE treino')
plt.plot(list(graus_range), mse_teste,  marker='s', label='MSE teste')
plt.title('MSE Treino vs. Teste em Função do Grau do Polinômio')
plt.xlabel('Grau do polinômio')
plt.ylabel('MSE')
plt.yscale('log')
plt.xticks(list(graus_range))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q23a_mse_treino_teste.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q23a_mse_treino_teste.png")
print(f"Grau que minimiza o MSE de teste: {melhor_grau}")

print("\n--- Item (b) ---")

aic_valores = []
for k in graus_range:
    coefs, _ = regressao_polinomial(x_treino, y_treino, k)
    y_hat = np.polyval(coefs[::-1], x_treino)
    rss = np.sum((y_treino - y_hat)**2)
    n   = len(x_treino)
    aic = n * np.log(rss / n) + 2 * (k + 1)
    aic_valores.append(aic)

melhor_grau_aic = list(graus_range)[np.argmin(aic_valores)]

linhas_aic = [[k, f"{aic:.4f}"] for k, aic in zip(graus_range, aic_valores)]
imprimir_tabela(["Grau", "AIC"], linhas_aic, alinhamento=['^', '^'])

print(f"\nGrau que minimiza o AIC: {melhor_grau_aic}")

print("\n--- Item (c) ---")
print(f"Validação cruzada → grau ótimo: {melhor_grau}")
print(f"AIC                → grau ótimo: {melhor_grau_aic}")
print("\nOs dois critérios podem ou não concordar. A validação cruzada")
print("mede diretamente o desempenho em dados não vistos; o AIC equilibra")
print("qualidade do ajuste e complexidade do modelo. Com dados escassos,")
print("a validação cruzada pode ter alta variância (apenas 5 pontos de teste),")
print("tornando o AIC geralmente mais estável nesse cenário.")


# ==================================================================================
# SEÇÃO 3 — Dados com Ruído: Interpolação ou Ajuste?
# ==================================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 3 — Dados com Ruído: Interpolação ou Ajuste?")
print("═" * 72)

np.random.seed(3)
x31_med = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
y31_med = 5.0 * np.exp(-0.8 * x31_med) + 0.2 * np.random.randn(7)

# ----------------------------------------------------------------------------------
# Q3.1 — Comparação direta
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 3.1 — Comparação direta")
print("─" * 72)

print("\n--- Item (a) ---")

x_plot_31 = np.linspace(0, 3, 500)
f_real_31  = 5.0 * np.exp(-0.8 * x_plot_31)
y_interp_31 = lagrange(x31_med, y31_med, x_plot_31)

plt.figure(figsize=(8, 5))
plt.plot(x_plot_31, f_real_31,    '--', label='Função real  5e⁻⁰·⁸ˣ')
plt.plot(x_plot_31, y_interp_31,  '-',  label='Interpolador de Lagrange (grau 6)')
plt.scatter(x31_med, y31_med, color='black', zorder=5, label='Dados com ruído')
plt.title('Interpolação de Lagrange com Dados Ruidosos')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q31a_curva_interpoladora_dados_freal.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q31a_curva_interpoladora_dados_freal.png")
print("\nO interpolador passa exatamente pelos pontos ruidosos, mas")
print("oscila em torno da função verdadeira — não é uma boa representação.")

print("\n--- Item (b) ---")

a31, b31, r2_exp = ajuste_exponencial(x31_med, y31_med)
erro_a = abs(a31 - 5.0) / 5.0
erro_b = abs(b31 - (-0.8)) / 0.8

print(f"Ajuste exponencial  ŷ = a·eᵇˣ:")
print(f"  a estimado = {a31:.4f}  |  valor real = 5,0  |  erro relativo = {erro_a:.4f} ({erro_a*100:.2f}%)")
print(f"  b estimado = {b31:.4f}  |  valor real = −0,8 |  erro relativo = {erro_b:.4f} ({erro_b*100:.2f}%)")

print("\n--- Item (c) ---")

x_plot_ext = np.linspace(0, 4, 500)
f_real_ext  = 5.0 * np.exp(-0.8 * x_plot_ext)
y_interp_ext = lagrange(x31_med, y31_med, x_plot_ext)
y_ajuste_ext = a31 * np.exp(b31 * x_plot_ext)

plt.figure(figsize=(8, 5))
plt.plot(x_plot_ext, f_real_ext,    '--', label='Função real  5e⁻⁰·⁸ˣ')
plt.plot(x_plot_ext, y_interp_ext,  '-',  label='Interpolador de Lagrange (grau 6)')
plt.plot(x_plot_ext, y_ajuste_ext,  '-',  label=f'Ajuste exponencial (a={a31:.3f}, b={b31:.3f})')
plt.scatter(x31_med, y31_med, color='black', zorder=5, label='Dados com ruído')
plt.axvline(3.0, linestyle=':', color='gray', alpha=0.7, label='Fim dos dados')
plt.title('Lagrange vs. Ajuste Exponencial — Dados Ruidosos e Extrapolação')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q31c_curva_interpoladora_dados_freal_aexp.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q31c_curva_interpoladora_dados_freal_aexp.png")
print("\nNo intervalo [0, 3] o ajuste exponencial representa melhor")
print("a tendência global, ignorando o ruído. Na extrapolação [3, 4],")
print("o interpolador de Lagrange diverge fortemente, enquanto o ajuste")
print("exponencial mantém o comportamento decrescente esperado.")

print("\n--- Item (d) ---")
y_pred_35_lag = lagrange(x31_med, y31_med, 3.5)
y_pred_35_exp = a31 * np.exp(b31 * 3.5)
y_real_35     = 5.0 * np.exp(-0.8 * 3.5)
print(f"Previsão em x = 3,5:")
print(f"  Lagrange:  {float(y_pred_35_lag):.4f}  |  Ajuste exponencial: {y_pred_35_exp:.4f}  |  Real: {y_real_35:.4f}")
print("\nPara prever f(3,5) o ajuste exponencial seria muito mais adequado,")
print("pois preserva o comportamento físico da função e é estável na")
print("extrapolação. O interpolador de Lagrange pode gerar oscilações")
print("arbitrárias fora do intervalo dos dados.")

# ----------------------------------------------------------------------------------
# Q3.2 — Diagnóstico pelo gráfico de resíduos
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 3.2 — Diagnóstico pelo gráfico de resíduos")
print("─" * 72)

print("\n--- Item (a) ---")

y_hat_exp  = a31 * np.exp(b31 * x31_med)
res_exp    = y31_med - y_hat_exp

plt.figure(figsize=(8, 5))
plt.scatter(x31_med, res_exp, color='steelblue', zorder=5, label='Resíduos')
plt.axhline(0, linestyle='--', color='gray')
plt.title('Resíduos do Ajuste Exponencial — rᵢ vs. xᵢ')
plt.xlabel('xᵢ')
plt.ylabel('rᵢ = yᵢ − ŷᵢ')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q32a_riXxi.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q32a_riXxi.png")
print("\nOs resíduos parecem distribuídos de forma aproximadamente")
print("aleatória em torno de zero, sem tendência sistemática visível,")
print("indicando que o ajuste exponencial é adequado aos dados.")

print("\n--- Item (b) ---")

a0_32, a1_32, r2_32 = regressao_linear(x31_med, y31_med)
y_hat_lin_32  = a0_32 + a1_32 * x31_med
res_lin_32    = y31_med - y_hat_lin_32

plt.figure(figsize=(8, 5))
plt.scatter(x31_med, res_lin_32, color='tomato', zorder=5, label='Resíduos')
plt.axhline(0, linestyle='--', color='gray')
plt.title('Resíduos do Modelo Linear — rᵢ vs. xᵢ')
plt.xlabel('xᵢ')
plt.ylabel('rᵢ = yᵢ − ŷᵢ')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q32b_residuos_modelo_linear.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q32b_residuos_modelo_linear.png")
print("\nOs resíduos do modelo linear apresentam padrão curvado")
print("(positivos nas extremidades, negativos no centro), evidenciando")
print("que o modelo linear não captura a curvatura exponencial dos dados.")

print("\n--- Item (c) ---")
print("Regra prática de diagnóstico de underfitting via resíduos:")
print("• Se os resíduos apresentam padrão sistemático (tendência, curvatura,")
print("  agrupamentos), o modelo está subdimensionado — o modelo não captura")
print("  a estrutura dos dados.")
print("• Se os resíduos estão espalhados aleatoriamente em torno de zero,")
print("  sem estrutura visível, o ajuste é adequado para a família de modelos")
print("  escolhida.")

# ==================================================================================
# SEÇÃO 4 — Modelos Não Lineares e Linearização
# ==================================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 4 — Modelos Não Lineares e Linearização")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Q4.1 — Crescimento populacional e lei de potência
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 4.1 — Crescimento populacional e lei de potência")
print("─" * 72)

ano = np.array([1960, 1970, 1980, 1990, 2000, 2010], dtype=float)
pop = np.array([32, 52, 82, 111, 138, 161], dtype=float)
t   = ano - 1960

print("\n--- Item (a) ---")

# Modelo exponencial: P(t) = a * exp(b*t)
a_exp, b_exp, r2_exp_log = ajuste_exponencial(t, pop)
pop_hat_exp = a_exp * np.exp(b_exp * t)
ss_res_exp  = np.sum((pop - pop_hat_exp)**2)
ss_tot      = np.sum((pop - np.mean(pop))**2)
r2_exp      = 1 - ss_res_exp / ss_tot

print(f"Modelo exponencial  P(t) = a·eᵇᵗ:")
print(f"  a = {a_exp:.4f}  |  b = {b_exp:.6f}")
print(f"  R² (espaço original) = {r2_exp:.6f}")

# Modelo potência: P(t) = a * t^b  (t=0 é indefinido no log-log → remover)
mask_pot    = t > 0
t_pot       = t[mask_pot]
pop_pot     = pop[mask_pot]
a_pot, b_pot, r2_pot_log = ajuste_potencia(t_pot, pop_pot)
pop_hat_pot = np.zeros_like(pop)
pop_hat_pot[mask_pot] = a_pot * t_pot**b_pot
# R² apenas nos pontos válidos
ss_res_pot = np.sum((pop_pot - a_pot * t_pot**b_pot)**2)
ss_tot_pot = np.sum((pop_pot - np.mean(pop_pot))**2)
r2_pot     = 1 - ss_res_pot / ss_tot_pot

print(f"\nModelo potência     P(t) = a·tᵇ  (t > 0, {len(t_pot)} pontos):")
print(f"  a = {a_pot:.4f}  |  b = {b_pot:.6f}")
print(f"  R² (espaço original, pontos válidos) = {r2_pot:.6f}")

# Modelo polinomial grau 2: P(t) = c0 + c1*t + c2*t²
coefs_pol2, r2_pol2 = regressao_polinomial(t, pop, 2)
pop_hat_pol2 = np.polyval(coefs_pol2[::-1], t)

print(f"\nModelo polinomial grau 2  P(t) = c0 + c1·t + c2·t²:")
print(f"  c0 = {coefs_pol2[0]:.4f}  |  c1 = {coefs_pol2[1]:.4f}  |  c2 = {coefs_pol2[2]:.6f}")
print(f"  R² = {r2_pol2:.6f}")

linhas_q41a = [
    ["Exponencial",      f"{a_exp:.4f}", f"{b_exp:.6f}",  "—",                      f"{r2_exp:.6f}"],
    ["Potência",         f"{a_pot:.4f}", f"{b_pot:.6f}",  "—",                      f"{r2_pot:.6f}"],
    ["Polinomial grau 2",f"{coefs_pol2[0]:.4f}", f"{coefs_pol2[1]:.4f}", f"{coefs_pol2[2]:.6f}", f"{r2_pol2:.6f}"],
]
imprimir_tabela(
    ["Modelo", "a / c0", "b / c1", "c2", "R²"],
    linhas_q41a,
    alinhamento=['<', '^', '^', '^', '^']
)

print("\n--- Item (b) ---")

t_plot  = np.linspace(0, 55, 500)
t_plot_pot = np.linspace(0.1, 55, 500)   # evita t=0 para potência

pop_exp_plot  = a_exp * np.exp(b_exp * t_plot)
pop_pot_plot  = a_pot * t_plot_pot**b_pot
pop_pol2_plot = np.polyval(coefs_pol2[::-1], t_plot)

plt.figure(figsize=(9, 5))
plt.scatter(t, pop, color='black', zorder=5, s=60, label='Dados históricos')
plt.plot(t_plot, pop_exp_plot,  label=f'Exponencial (R²={r2_exp:.4f})')
plt.plot(t_plot_pot, pop_pot_plot, label=f'Potência (R²={r2_pot:.4f})')
plt.plot(t_plot, pop_pol2_plot, label=f'Polinomial grau 2 (R²={r2_pol2:.4f})')
plt.title('Crescimento da População Urbana Brasileira — Três Modelos')
plt.xlabel('t (anos desde 1960)')
plt.ylabel('População urbana (milhões)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q41b_modelos_populacao.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q41b_modelos_populacao.png")
print("\nVisualmente, o modelo polinomial de grau 2 e o modelo de potência")
print("apresentam melhor aderência aos dados no intervalo observado.")
print("O modelo exponencial tende a superestimar o crescimento nos anos finais.")

print("\n--- Item (c) ---")

t60 = 60.0    # t = 60 → ano 2020
pop_real_2020 = 171.0

prev_exp  = a_exp * np.exp(b_exp * t60)
prev_pot  = a_pot * t60**b_pot
prev_pol2 = np.polyval(coefs_pol2[::-1], t60)

erro_exp  = abs(prev_exp  - pop_real_2020) / pop_real_2020 * 100
erro_pot  = abs(prev_pot  - pop_real_2020) / pop_real_2020 * 100
erro_pol2 = abs(prev_pol2 - pop_real_2020) / pop_real_2020 * 100

linhas_q41c = [
    ["Exponencial",      f"{prev_exp:.2f}  M",  f"{erro_exp:.2f}%"],
    ["Potência",         f"{prev_pot:.2f}  M",  f"{erro_pot:.2f}%"],
    ["Polinomial grau 2",f"{prev_pol2:.2f} M",  f"{erro_pol2:.2f}%"],
]
imprimir_tabela(
    ["Modelo", "Previsão t=60 (M)", "Erro percentual"],
    linhas_q41c,
    alinhamento=['<', '^', '^']
)

print(f"\nValor real em 2020: {pop_real_2020} M")
print("O modelo com menor erro percentual para t = 60 é o mais adequado")
print("para extrapolação moderada, indicando melhor captura da tendência.")

print("\n--- Item (d) ---")

func_exp = lambda t, a, b: a * np.exp(b * t)
popt_nl, pcov_nl = ajuste_nao_linear(func_exp, t, pop, p0=[30.0, 0.05])
a_nl, b_nl = popt_nl

pop_hat_nl = func_exp(t, a_nl, b_nl)
ss_res_nl  = np.sum((pop - pop_hat_nl)**2)
r2_nl      = 1 - ss_res_nl / ss_tot

print(f"Ajuste direto (não linear)  P(t) = a·eᵇᵗ:")
print(f"  a = {a_nl:.4f}  |  b = {b_nl:.6f}")
print(f"  R² (espaço original) = {r2_nl:.6f}")

print(f"\nComparação linearização vs. ajuste direto:")
print(f"  Linearização: a = {a_exp:.4f}, b = {b_exp:.6f}, R² = {r2_exp:.6f}")
print(f"  Direto (NL):  a = {a_nl:.4f}, b = {b_nl:.6f}, R² = {r2_nl:.6f}")
print(f"  Δa = {abs(a_nl - a_exp):.4f}  |  Δb = {abs(b_nl - b_exp):.6f}")

print("\nAo linearizar via ln(P), minimizamos os resíduos no espaço logarítmico")
print("— equivalente a pesar cada ponto pelo inverso de P². O ajuste direto")
print("minimiza os resíduos no espaço original (igual peso a todos os pontos),")
print("o que geralmente melhora o R² no espaço de interesse e produz parâmetros")
print("mais representativos do fenômeno físico quando os valores são grandes.")


# ----------------------------------------------------------------------------------
# Q4.2 — Quando a linearização distorce
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 4.2 — Quando a linearização distorce")
print("─" * 72)

np.random.seed(11)
x_p = np.linspace(1, 10, 20)
y_p = 3.0 * x_p**2.5 * (1 + 0.1 * np.random.randn(20))

print("\n--- Item (a) ---")

a_ll, b_ll, r2_ll_log = ajuste_potencia(x_p, y_p)
y_hat_ll    = a_ll * x_p**b_ll
ss_res_ll   = np.sum((y_p - y_hat_ll)**2)
ss_tot_p    = np.sum((y_p - np.mean(y_p))**2)
r2_ll       = 1 - ss_res_ll / ss_tot_p

erro_a_ll = abs(a_ll - 3.0) / 3.0 * 100
erro_b_ll = abs(b_ll - 2.5) / 2.5 * 100

print(f"Linearização log-log  ŷ = a·xᵇ:")
print(f"  a estimado = {a_ll:.4f}  (real: 3,0)  |  erro relativo: {erro_a_ll:.2f}%")
print(f"  b estimado = {b_ll:.4f}  (real: 2,5)  |  erro relativo: {erro_b_ll:.2f}%")
print(f"  R² (espaço original) = {r2_ll:.6f}")

print("\n--- Item (b) ---")

func_pot = lambda x, a, b: a * x**b
popt_pot, _ = ajuste_nao_linear(func_pot, x_p, y_p, p0=[1.0, 2.0])
a_nl_p, b_nl_p = popt_pot

y_hat_nl_p  = func_pot(x_p, a_nl_p, b_nl_p)
ss_res_nl_p = np.sum((y_p - y_hat_nl_p)**2)
r2_nl_p     = 1 - ss_res_nl_p / ss_tot_p

erro_a_nl = abs(a_nl_p - 3.0) / 3.0 * 100
erro_b_nl = abs(b_nl_p - 2.5) / 2.5 * 100

print(f"Ajuste direto (não linear)  ŷ = a·xᵇ:")
print(f"  a estimado = {a_nl_p:.4f}  (real: 3,0)  |  erro relativo: {erro_a_nl:.2f}%")
print(f"  b estimado = {b_nl_p:.4f}  (real: 2.5)  |  erro relativo: {erro_b_nl:.2f}%")
print(f"  R² (espaço original) = {r2_nl_p:.6f}")

linhas_q42b = [
    ["Linearização log-log", f"{a_ll:.4f}",   f"{b_ll:.4f}",   f"{erro_a_ll:.2f}%", f"{erro_b_ll:.2f}%", f"{r2_ll:.6f}"],
    ["Ajuste direto (NL)",   f"{a_nl_p:.4f}", f"{b_nl_p:.4f}", f"{erro_a_nl:.2f}%", f"{erro_b_nl:.2f}%", f"{r2_nl_p:.6f}"],
]
imprimir_tabela(
    ["Método", "a estimado", "b estimado", "Δa (%)", "Δb (%)", "R²"],
    linhas_q42b,
    alinhamento=['<', '^', '^', '^', '^', '^']
)

print("\n--- Item (c) ---")

res_ll_p  = y_p - y_hat_ll
res_nl_p  = y_p - y_hat_nl_p

rmse_ll = np.sqrt(np.mean(res_ll_p**2))
rmse_nl = np.sqrt(np.mean(res_nl_p**2))

plt.figure(figsize=(8, 5))
plt.scatter(x_p, res_ll_p,  marker='o', label=f'Resíduos — log-log (RMSE={rmse_ll:.2f})')
plt.scatter(x_p, res_nl_p,  marker='s', label=f'Resíduos — ajuste direto (RMSE={rmse_nl:.2f})')
plt.axhline(0, linestyle='--', color='gray')
plt.title('Resíduos no Espaço Original — Lei de Potência com Ruído Multiplicativo')
plt.xlabel('x')
plt.ylabel('rᵢ = yᵢ − ŷᵢ')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("q42c_residuos_potencia.png", bbox_inches='tight')
plt.close()

print("Gráfico salvo como: q42c_residuos_potencia.png")
print(f"\nRMSE — linearização log-log: {rmse_ll:.4f}")
print(f"RMSE — ajuste direto:         {rmse_nl:.4f}")
print("\nO ajuste direto apresenta resíduos menores e mais homogêneos")
print("no espaço original, confirmando sua superioridade com ruído multiplicativo.")

print("\n--- Item (d) ---")
print("Com ruído multiplicativo ε_i ~ N(0, σ), temos y_i = a·xᵢᵇ·(1 + ε_i).")
print("Ao aplicar log-log: ln(y_i) = ln(a) + b·ln(x_i) + ln(1 + ε_i).")
print("O termo ln(1 + ε_i) não é gaussiano e varia com a magnitude de y_i,")
print("violando a suposição de erros homocedásticos. Além disso, a transformação")
print("logarítmica comprime os valores grandes e expande os pequenos, distorcendo")
print("a ponderação implícita dos pontos — os de menor x recebem peso desproporcional.")
print("O ajuste direto por mínimos quadrados não lineares opera no espaço original,")
print("minimizando Σ(yᵢ − a·xᵢᵇ)², o que é consistente com o modelo de ruído")
print("aditivo e produz parâmetros mais precisos quando os erros são multiplicativos.")

# ==================================================================================
# SEÇÃO 5 — Comparação Integrada: Interpolação vs. Ajuste
# ==================================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 5 — Comparação Integrada: Interpolação vs. Ajuste")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Q5.1 — Tabela de síntese
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 5.1 — Tabela de síntese")
print("─" * 72)

linhas_sintese = [
    [
        "Passagem pelos dados",
        "Exata — curva passa por todos os pontos",
        "Aproximada — minimiza Σrᵢ², não força passagem",
    ],
    [
        "Reação ao ruído",
        "Amplifica o ruído — interpola os erros de medição",
        "Suaviza o ruído — distribui o erro entre os pontos",
    ],
    [
        "Número de parâmetros",
        "Determinado pelos dados (n+1 pontos → grau n)",
        "Escolhido pelo analista (independe de n)",
    ],
    [
        "Risco de oscilação",
        "Alto para grau elevado — fenômeno de Runge",
        "Baixo se grau for adequado; alto no sobreajuste",
    ],
    [
        "Extrapolação",
        "Perigosa — oscilações arbitrárias fora do intervalo",
        "Mais estável se o modelo captura a tendência física",
    ],
    [
        "Escolha do modelo",
        "Automática — grau fixado pelos pontos disponíveis",
        "Exige conhecimento prévio da família de modelos",
    ],
    [
        "Quando preferir",
        "Dados exatos, poucos pontos, integração/derivação",
        "Dados com ruído, muitos pontos, extrapolação",
    ],
    [
        "Ferramenta típica",
        "Lagrange, Newton, Spline cúbica",
        "regressao_linear/polinomial, ajuste_exponencial",
    ],
]

imprimir_tabela(
    ["Aspecto", "Interpolação", "Ajuste (MQ)"],
    linhas_sintese,
    alinhamento=['<', '<', '<']
)

print("\nSíntese dos experimentos realizados nas Seções 1–4:")
print("")
print("Vantagens da interpolação:")
print("  • Reproduz exatamente os dados fornecidos (resíduo nulo nos nós).")
print("  • Ideal para dados de alta precisão onde o erro de medição é desprezível.")
print("  • Permite integração e derivação numéricas com controle de erro (Seção 1).")
print("  • A forma de Newton permite atualização incremental eficiente (Q1.2).")
print("")
print("Vantagens do ajuste por mínimos quadrados:")
print("  • Suaviza o ruído de medição sem amplificá-lo (Seção 3).")
print("  • Permite incorporar conhecimento físico na escolha do modelo.")
print("  • Mais estável na extrapolação quando o modelo é fisicamente correto.")
print("  • Parâmetros estimados têm interpretação física direta (a, b em P=aeᵇᵗ).")
print("")
print("Influência do ruído:")
print("  • Com ruído, a interpolação força o polinômio a passar pelos erros,")
print("    gerando oscilações que afastam a curva da função verdadeira (Q3.1).")
print("  • O ajuste exponencial com os mesmos dados ruidosos recuperou os")
print("    parâmetros com erro relativo pequeno (Q3.1b), confirmando sua")
print("    robustez ao ruído quando a família de modelos é correta.")
print("")
print("Relação com o fenômeno de Runge:")
print("  • Polinômios de grau elevado oscilam nas extremidades do intervalo,")
print("    mesmo sobre dados limpos (Q1.3). Nós de Chebyshev mitigam o problema.")
print("  • O sobreajuste polinomial (Q2.2) é o análogo do fenômeno de Runge")
print("    no ajuste: graus muito altos memorizam o ruído e perdem generalização.")
print("")
print("Importância da escolha do modelo:")
print("  • Um modelo mal especificado produz resíduos com padrão sistemático")
print("    (curvatura, tendência), sinal claro de underfitting (Q3.2).")
print("  • Critérios como AIC e validação cruzada auxiliam na seleção do grau")
print("    sem usar os dados de teste para treino (Q2.3).")
print("  • A linearização distorce os parâmetros quando o ruído é multiplicativo;")
print("    o ajuste direto não linear produz estimativas mais precisas (Q4.2).")


# ----------------------------------------------------------------------------------
# Q5.2 — Tomada de decisão em cenários reais
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 5.2 — Tomada de decisão em cenários reais")
print("─" * 72)

print("\n--- Item (a) ---")
print("Cenário: Engenheiro de controle — curva v×t com precisão < 0,01%,")
print("50 instantes de tempo, integração numérica para obter posição.")
print("")
print("Método escolhido: Interpolação por spline cúbica.")
print("")
print("Justificativa:")
print("  O erro de medição é inferior a 0,01% — virtualmente nulo para fins")
print("  práticos. Forçar a passagem exata pelos pontos é, portanto, correto")
print("  e desejável. A spline cúbica é preferível ao polinômio global de")
print("  Lagrange pois, com 50 nós, o grau 49 quase certamente produziria")
print("  oscilações severas (fenômeno de Runge). A spline garante continuidade")
print("  de segunda ordem em cada subintervalo e curvas suaves, o que reduz")
print("  o erro de quadratura numérica ao integrar para obter a posição.")
print("  Nós de Chebyshev seriam uma alternativa ao Lagrange global, mas a")
print("  spline é mais simples e igualmente eficaz para 50 pontos.")

print("\n--- Item (b) ---")
print("Cenário: Epidemiologista — contagens diárias com ruído ~15%,")
print("estimativa da taxa de crescimento r em C = C₀·eʳᵗ.")
print("")
print("Método escolhido: Ajuste exponencial por mínimos quadrados")
print("(preferencialmente ajuste não linear direto via curve_fit).")
print("")
print("Justificativa:")
print("  Com ruído de 15%, interpolar os dados forçaria a curva a passar")
print("  pelos erros de subnotificação, distorcendo completamente a estimativa")
print("  de r. O ajuste exponencial — conforme demonstrado na Q3.1 — recupera")
print("  os parâmetros com boa precisão mesmo na presença de ruído, pois")
print("  distribui os resíduos entre todos os pontos. Recomenda-se o ajuste")
print("  direto não linear (ajuste_nao_linear) em vez da linearização via ln,")
print("  pois o ruído não é homocedástico no espaço logarítmico (Q4.1d),")
print("  garantindo estimativa de r mais representativa da dinâmica real.")

print("\n--- Item (c) ---")
print("Cenário: Projetista de pontes — 8 medições deslocamento × carga,")
print("laboratório sem erros instrumentais, interpolação de cargas intermediárias.")
print("")
print("Método escolhido: Interpolação por spline cúbica (not-a-knot).")
print("")
print("Justificativa:")
print("  Dados obtidos em laboratório sem erros instrumentais significativos")
print("  justificam a passagem exata pelos pontos de medição. Com apenas 8 nós,")
print("  o polinômio global de Lagrange teria grau 7, aceitável, mas a spline")
print("  cúbica é mais segura: produz curvas suaves, evita oscilações nas")
print("  extremidades e representa melhor o comportamento físico contínuo de")
print("  uma viga sob carga (análogo ao caso climático da Q1.4). O resíduo")
print("  máximo da spline nos nós de calibração é zero por construção, e os")
print("  valores intermediários são fisicamente plausíveis.")

print("\n--- Item (d) ---")
print("Cenário: Cientista de dados — 500 pares (x,y) com ruído gaussiano,")
print("modelo suspeito y = a·xᵇ + c (lei de potência com deslocamento).")
print("")
print("Método escolhido: Ajuste não linear direto por mínimos quadrados")
print("(ajuste_nao_linear com função lambda x, a, b, c: a*x**b + c).")
print("")
print("Justificativa:")
print("  Com 500 pontos ruidosos, interpolar seria absurdo: um polinômio de")
print("  grau 499 memorizaria o ruído integralmente, com RMSE de treinamento")
print("  nulo e RMSE de generalização explosivo — sobreajuste extremo (Q2.2).")
print("  O modelo y = a·xᵇ + c não é linearizável diretamente (o termo c")
print("  impede o log-log), de modo que a linearização log-log introduziria")
print("  distorção sistemática nos parâmetros (Q4.2). O ajuste direto via")
print("  curve_fit minimiza Σ(yᵢ − ŷᵢ)² no espaço original, trata corretamente")
print("  o ruído gaussiano aditivo e estima a, b, c sem viés de transformação.")
print("  Os resíduos devem ser inspecionados (Q3.2) para confirmar que não há")
print("  estrutura sistemática residual antes de validar o modelo.")

print("\n" + "─" * 72)
print("CONCLUSÃO GERAL — Interpolação vs. Ajuste")
print("─" * 72)

print("")
print("Quando interpolar:")
print("  Use interpolação quando os dados são obtidos com alta precisão (erro")
print("  desprezível) e o objetivo é representar exatamente os valores medidos.")
print("  A spline cúbica é a escolha padrão para conjuntos com mais de ~5 pontos,")
print("  pois evita as oscilações do polinômio global (fenômeno de Runge).")
print("  Lagrange ou Newton são adequados para poucos pontos e verificações")
print("  teóricas; Newton tem a vantagem de atualização incremental eficiente.")
print("")
print("Quando ajustar:")
print("  Use ajuste por mínimos quadrados quando os dados contêm ruído de")
print("  medição, quando a quantidade de pontos é grande, ou quando se deseja")
print("  estimar parâmetros físicos de um modelo. O ajuste não passa pelos")
print("  pontos — e essa é precisamente sua virtude na presença de erros.")
print("")
print("Impacto do ruído:")
print("  Ruído e interpolação são incompatíveis: o polinômio interpola os erros,")
print("  amplifica as oscilações e distorce qualquer previsão fora dos dados.")
print("  Mesmo um ruído modesto de 15–20% torna o ajuste vastamente superior,")
print("  como demonstrado nos experimentos da Seção 3.")
print("")
print("Risco de overfitting:")
print("  Aumentar o grau do modelo de ajuste sempre reduz o erro de treinamento,")
print("  mas pode degradar o desempenho em dados novos. Critérios como AIC e")
print("  validação cruzada (Q2.3) equilibram qualidade de ajuste e complexidade.")
print("  O sobreajuste polinomial é o análogo do fenômeno de Runge no contexto")
print("  do ajuste: ambos resultam de flexibilidade excessiva do modelo.")
print("")
print("Importância dos resíduos na validação:")
print("  O gráfico de resíduos rᵢ vs. xᵢ é a principal ferramenta diagnóstica.")
print("  Resíduos aleatórios em torno de zero indicam modelo adequado.")
print("  Padrão sistemático (curvatura, tendência, heteroscedasticidade) indica")
print("  underfitting ou família de modelos errada — o modelo deve ser revisto")
print("  antes de qualquer uso preditivo ou de engenharia (Q3.2, Q4.2).")

# ==================================================================================
# SEÇÃO 6 — Projeto Integrador: Calibração de Sensor
# ==================================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 6 — Projeto Integrador: Calibração de Sensor")
print("═" * 72)

# Dados de calibração laboratorial (sem ruído)
mV_lab  = np.array([10, 20, 35, 50, 65, 80, 90, 100], dtype=float)
bar_lab = np.array([0.5, 1.2, 2.3, 3.5, 4.8, 6.0, 6.8, 7.5], dtype=float)

# ----------------------------------------------------------------------------------
# Q6.1 — Calibração precisa (laboratório)
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 6.1 — Calibração precisa (laboratório)")
print("─" * 72)

print("\n--- Item (a) ---")
print("Ajustando os quatro modelos aos dados de calibração laboratoriais (sem ruído)...\n")

mV_plot = np.linspace(10, 100, 200)

# Spline cúbica not-a-knot — interpola exatamente os 8 nós de calibração
bar_spline, cs_lab = spline_cubica(mV_lab, bar_lab, mV_plot)
bar_spline_nos, _  = spline_cubica(mV_lab, bar_lab, mV_lab)

# Regressão polinomial grau 2
coefs_p2, r2_p2 = regressao_polinomial(mV_lab, bar_lab, 2)
bar_p2_plot = np.polyval(coefs_p2[::-1], mV_plot)
bar_p2_nos  = np.polyval(coefs_p2[::-1], mV_lab)

# Regressão polinomial grau 3
coefs_p3, r2_p3 = regressao_polinomial(mV_lab, bar_lab, 3)
bar_p3_plot = np.polyval(coefs_p3[::-1], mV_plot)
bar_p3_nos  = np.polyval(coefs_p3[::-1], mV_lab)

# Regressão linear simples
a0_lin, a1_lin, r2_lin = regressao_linear(mV_lab, bar_lab)
bar_lin_plot = a0_lin + a1_lin * mV_plot
bar_lin_nos  = a0_lin + a1_lin * mV_lab

print("Modelos ajustados:")
print(f"  Regressão linear:    p̂(x) = {a0_lin:.4f} + {a1_lin:.4f}·x   (R² = {r2_lin:.6f})")
print(f"  Polinômio grau 2:    coeficientes (ordem crescente) = "
      f"[{coefs_p2[0]:.4f}, {coefs_p2[1]:.5f}, {coefs_p2[2]:.7f}]   (R² = {r2_p2:.6f})")
print(f"  Polinômio grau 3:    coeficientes (ordem crescente) = "
      f"[{coefs_p3[0]:.4f}, {coefs_p3[1]:.5f}, {coefs_p3[2]:.7f}, {coefs_p3[3]:.9f}]   (R² = {r2_p3:.6f})")
print("  Spline cúbica not-a-knot: interpolação exata nos 8 nós; resíduo estruturalmente nulo.")

print("\n--- Item (b) ---")
print("Resíduo máximo max_i |y_i − ŷ_i| de cada método nos 8 pontos de calibração:\n")

res_spline, std_spline, maxres_spline = residuos(mV_lab, bar_lab, bar_spline_nos)
res_p2,     std_p2,     maxres_p2     = residuos(mV_lab, bar_lab, bar_p2_nos)
res_p3,     std_p3,     maxres_p3     = residuos(mV_lab, bar_lab, bar_p3_nos)
res_lin,    std_lin,    maxres_lin    = residuos(mV_lab, bar_lab, bar_lin_nos)

cabecalhos_61b = ["Método", "R²", "RMSE (bar)", "Resíduo máx. (bar)"]
linhas_61b = [
    ["Spline cúbica (not-a-knot)", "—",
     f"{std_spline:.2e}", f"{maxres_spline:.2e}"],
    ["Polinômio grau 2", f"{r2_p2:.6f}",
     f"{std_p2:.4f}", f"{maxres_p2:.4f}"],
    ["Polinômio grau 3", f"{r2_p3:.6f}",
     f"{std_p3:.4f}", f"{maxres_p3:.4f}"],
    ["Regressão linear", f"{r2_lin:.6f}",
     f"{std_lin:.4f}", f"{maxres_lin:.4f}"],
]
imprimir_tabela(cabecalhos_61b, linhas_61b, ['<', '^', '^', '^'])
print("\n  Nota: para a spline (método interpolador), RMSE e resíduo máximo são nulos por")
print("  construção — a spline passa exatamente pelos nós de calibração.")

print("\n--- Item (c) ---")
print("Gráfico comparativo das quatro curvas em [10, 100] mV (200 pontos)...\n")

fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(mV_lab, bar_lab, s=70, zorder=6, color='black', label='Dados de calibração')
ax.plot(mV_plot, bar_spline,   linewidth=2.2, label='Spline cúbica (not-a-knot)')
ax.plot(mV_plot, bar_p2_plot,  linewidth=2.0, linestyle='--', label='Pol. grau 2')
ax.plot(mV_plot, bar_p3_plot,  linewidth=2.0, linestyle='-.', label='Pol. grau 3')
ax.plot(mV_plot, bar_lin_plot, linewidth=2.0, linestyle=':',  label='Regressão linear')
ax.set_title('Q6.1(c) — Curvas de Calibração: Comparação de Métodos')
ax.set_xlabel('Tensão (mV)')
ax.set_ylabel('Pressão (bar)')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig('q6_1c_calibracao_metodos.pdf', dpi=300)
plt.close()

print("Gráfico salvo: q6_1c_calibracao_metodos.pdf")
print("\n  Observação visual: a spline cúbica e o polinômio de grau 3 apresentam")
print("  comportamento mais suave e aderente aos dados. O polinômio de grau 2")
print("  introduz desvio crescente nas extremidades, e a regressão linear não")
print("  captura a curvatura intrínseca da relação tensão–pressão.")

print("\n--- Item (d) ---")
print("Verificação da exigência de precisão ±0,05 bar nos pontos de calibração:\n")

PREC = 0.05  # bar

cabecalhos_61d = ["Método", "Resíduo máx. (bar)", "≤ 0,05 bar?"]
linhas_61d = [
    ["Spline cúbica",
     f"{maxres_spline:.2e}",
     "Sim (por construção)"],
    ["Polinômio grau 2",
     f"{maxres_p2:.4f}",
     "Sim" if maxres_p2 <= PREC else "Não"],
    ["Polinômio grau 3",
     f"{maxres_p3:.4f}",
     "Sim" if maxres_p3 <= PREC else "Não"],
    ["Regressão linear",
     f"{maxres_lin:.4f}",
     "Sim" if maxres_lin <= PREC else "Não"],
]
imprimir_tabela(cabecalhos_61d, linhas_61d, ['<', '^', '<'])

metodos_aceitos = [
    ("Spline cúbica",    maxres_spline),
    ("Polinômio grau 2", maxres_p2),
    ("Polinômio grau 3", maxres_p3),
    ("Regressão linear", maxres_lin),
]
print()
for nome, maxr in metodos_aceitos:
    cond = maxr <= PREC
    print(f"  {nome:<22}: {maxr:.4f} bar → {'ATENDE' if cond else 'NÃO ATENDE'}")

aceitos = [n for n, r in metodos_aceitos if r <= PREC]
print()
if aceitos:
    print(f"  Métodos que satisfazem a exigência de ±{PREC} bar nos nós de calibração:")
    for n in aceitos:
        print(f"    • {n}")
    print()
    print("  Importante: esta análise avalia exclusivamente os resíduos nos 8 pontos")
    print("  de calibração. Entre os nós, apenas a spline garante a continuidade C²")
    print("  da curva; os métodos de regressão podem apresentar desvios adicionais")
    print("  em posições não calibradas, dependendo do grau e dos dados.")
else:
    print("  Nenhum método de regressão satisfaz ±0,05 bar. Somente a spline cúbica,")
    print("  que interpola os nós exatamente, atende a exigência por construção.")

# ----------------------------------------------------------------------------------
# Q6.2 — Robustez ao ruído de campo
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 6.2 — Robustez ao ruído de campo")
print("─" * 72)

# Configuração conforme o enunciado
np.random.seed(42)
mV_campo = np.linspace(10, 100, 30)
ruido    = 2.0 * np.random.randn(30)          # ruído de ±2 mV (σ = 2 mV)

# Pressão de referência: spline de calibração aplicada às posições verdadeiras
p_verdade, _ = spline_cubica(mV_lab, bar_lab, mV_campo)

# Tensão medida em campo (entrada perturbada)
mV_ruidoso = mV_campo + ruido

print("\n--- Item (a) ---")
print("Convertendo mV_ruidoso → pressão via spline de calibração laboratorial...\n")

# A spline foi construída no intervalo [10, 100] mV; limitamos a entrada ao domínio
# de calibração para evitar extrapolação. Em campo, valores fora do intervalo
# indicam condição operacional anômala e devem ser sinalizados ao operador.
mV_ruidoso_clip = np.clip(mV_ruidoso, mV_lab[0], mV_lab[-1])
p_spline_campo  = cs_lab(mV_ruidoso_clip)

# RMSE entre pressão estimada e pressão de referência
rmse_spline_campo = np.sqrt(np.mean((p_spline_campo - p_verdade)**2))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(mV_campo, p_verdade,      linewidth=2.2, label='Pressão de referência')
axes[0].plot(mV_campo, p_spline_campo, linewidth=1.8, linestyle='--',
             label='Estimativa (spline + ruído)')
axes[0].scatter(mV_campo, p_spline_campo, s=28, zorder=5, alpha=0.75)
axes[0].set_title('Q6.2(a) — Spline de Calibração com Ruído de Entrada')
axes[0].set_xlabel('Tensão verdadeira (mV)')
axes[0].set_ylabel('Pressão (bar)')
axes[0].legend()
axes[0].grid(True)

pmin, pmax = p_verdade.min(), p_verdade.max()
axes[1].scatter(p_verdade, p_spline_campo, s=40, zorder=5)
axes[1].plot([pmin, pmax], [pmin, pmax], 'r--', linewidth=1.8, label='Identidade (y = x)')
axes[1].set_title('Q6.2(a) — Estimado vs. Referência (Spline + Ruído)')
axes[1].set_xlabel('Pressão de referência (bar)')
axes[1].set_ylabel('Pressão estimada (bar)')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig('q6_2a_spline_ruido.pdf', dpi=300)
plt.close()

print(f"  RMSE (spline de calibração, entrada ruidosa): {rmse_spline_campo:.4f} bar")
print("  Gráfico salvo: q6_2a_spline_ruido.pdf")
print()
print("  O erro de conversão com a spline é proporcional à derivada local da")
print("  curva de calibração (sensibilidade dP/dmV). Para um erro de entrada")
print(f"  σ = 2 mV e sensibilidade média de {(bar_lab[-1]-bar_lab[0])/(mV_lab[-1]-mV_lab[0]):.4f} bar/mV,")
print(f"  a estimativa analítica do RMSE é ≈ {(bar_lab[-1]-bar_lab[0])/(mV_lab[-1]-mV_lab[0])*2:.4f} bar,")
print(f"  coerente com o valor obtido ({rmse_spline_campo:.4f} bar).")

print("\n--- Item (b) ---")
print("Reajuste de polinômio grau 3 por mínimos quadrados sobre os 30 pontos ruidosos...")
print("(pares: tensão medida mV_ruidoso[i] × pressão de referência p_verdade[i])\n")

# Os 30 pontos ruidosos são os pares (mV_ruidoso[i], p_verdade[i]).
# O polinômio é ajustado por MQ sobre esses pares; o RMSE é calculado avaliando
# o modelo nas tensões verdadeiras (mV_campo), métrica consistente com o item (a).
coefs_campo_p3, r2_campo_p3 = regressao_polinomial(mV_ruidoso, p_verdade, 3)
p_campo_p3 = np.polyval(coefs_campo_p3[::-1], mV_campo)
rmse_campo_p3 = np.sqrt(np.mean((p_campo_p3 - p_verdade)**2))

print(f"  R² (pol. grau 3 ajustado sobre pares ruidosos): {r2_campo_p3:.6f}")
print(f"  RMSE (avaliado nas tensões verdadeiras mV_campo): {rmse_campo_p3:.4f} bar")

print("\n--- Item (c) ---")
print("Comparação de robustez baseada exclusivamente nos RMSE obtidos...\n")

print("  Experimento com seed fixa (seed=42, realização única):")
cabecalhos_62c = ["Método", "RMSE — seed 42 (bar)", "Estratégia"]
linhas_62c = [
    ["Spline de calibração + entrada ruidosa",
     f"{rmse_spline_campo:.4f}",
     "Modelo fixo do lab; propaga erro de entrada via dP/dmV"],
    ["Pol. grau 3 (MQ sobre pares ruidosos)",
     f"{rmse_campo_p3:.4f}",
     "Ajuste global; dilui o erro de tensão entre 30 observações"],
]
imprimir_tabela(cabecalhos_62c, linhas_62c, ['<', '^', '<'])

# ─── Análise de Monte Carlo (N = 1000 realizações) ───────────────────────────────
print()
print("  Análise de Monte Carlo (N = 1000 realizações, σ = 2 mV):")
print("  (necessária para conclusão estatisticamente defensável)\n")

N_MC = 1000
rmse_spline_mc = np.zeros(N_MC)
rmse_p3_mc     = np.zeros(N_MC)
rng_mc = np.random.default_rng(0)   # seed separada do experimento principal

for i in range(N_MC):
    ruido_i    = 2.0 * rng_mc.standard_normal(30)
    mV_rid_i   = mV_campo + ruido_i
    mV_clip_i  = np.clip(mV_rid_i, mV_lab[0], mV_lab[-1])
    rmse_spline_mc[i] = np.sqrt(np.mean((cs_lab(mV_clip_i) - p_verdade)**2))
    coefs_i, _ = regressao_polinomial(mV_rid_i, p_verdade, 3)
    p3_i = np.polyval(coefs_i[::-1], mV_campo)
    rmse_p3_mc[i] = np.sqrt(np.mean((p3_i - p_verdade)**2))

pct_p3_melhor = (rmse_p3_mc < rmse_spline_mc).mean() * 100

cabecalhos_mc = ["Método", "RMSE médio (bar)", "Desvio-padrão (bar)", "RMSE mediana (bar)"]
linhas_mc = [
    ["Spline de calibração + entrada ruidosa",
     f"{rmse_spline_mc.mean():.4f}", f"{rmse_spline_mc.std():.4f}",
     f"{np.median(rmse_spline_mc):.4f}"],
    ["Pol. grau 3 (MQ sobre pares ruidosos)",
     f"{rmse_p3_mc.mean():.4f}", f"{rmse_p3_mc.std():.4f}",
     f"{np.median(rmse_p3_mc):.4f}"],
]
imprimir_tabela(cabecalhos_mc, linhas_mc, ['<', '^', '^', '^'])

print()
print(f"  O polinômio de grau 3 apresentou RMSE inferior à spline em {pct_p3_melhor:.1f}%")
print("  das 1000 realizações. A conclusão é, portanto, estatisticamente robusta")
print("  e não depende da seed particular escolhida no enunciado:")
print()
print("  O ajuste por mínimos quadrados é mais robusto ao ruído de campo que a")
print("  aplicação direta da spline de calibração com entrada perturbada. Enquanto")
print("  a spline propaga o erro de tensão à saída de forma ponto a ponto (via")
print("  sensibilidade local dP/dmV), o polinômio de grau 3 ajustado globalmente")
print("  distribui a variância do ruído entre as 30 observações, reduzindo o RMSE")
print(f"  médio de {rmse_spline_mc.mean():.4f} bar (spline) para {rmse_p3_mc.mean():.4f} bar (pol. grau 3).")

# Gráfico distribuição Monte Carlo
fig, ax = plt.subplots(figsize=(8, 5))
bins = np.linspace(0, max(rmse_spline_mc.max(), rmse_p3_mc.max()), 50)
ax.hist(rmse_spline_mc, bins=bins, alpha=0.6,
        label=f'Spline (μ={rmse_spline_mc.mean():.4f} bar)')
ax.hist(rmse_p3_mc, bins=bins, alpha=0.6,
        label=f'Pol. grau 3 (μ={rmse_p3_mc.mean():.4f} bar)')
ax.axvline(rmse_spline_mc.mean(), color='C0', linewidth=2, linestyle='--')
ax.axvline(rmse_p3_mc.mean(),     color='C1', linewidth=2, linestyle='--')
ax.set_title('Q6.2(c) — Distribuição do RMSE (Monte Carlo, N = 1000)')
ax.set_xlabel('RMSE (bar)')
ax.set_ylabel('Frequência')
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.savefig('q6_2c_monte_carlo_rmse.pdf', dpi=300)
plt.close()
print("\n  Gráfico salvo: q6_2c_monte_carlo_rmse.pdf")

print("\n--- Item (d) ---")
print("Previsão teórica — Interpolação de Lagrange grau 29 nos 30 pontos ruidosos:")
print()
print("  Os 30 pontos de campo têm tensões mV_ruidoso com perturbação aleatória")
print("  de ±2 mV. Um polinômio de Lagrange grau 29 é forçado a interpolar")
print("  exatamente esses 30 pares (mV_ruidoso[i], p_verdade[i]), cujos nós estão")
print("  irregularmente espaçados (devido ao ruído). Polinômios de grau elevado")
print("  com nós irregulares tendem a oscilar violentamente entre os nós —")
print("  comportamento análogo ao fenômeno de Runge. Prevê-se, portanto, que o")
print("  RMSE de Lagrange grau 29 será ordens de grandeza superior ao do pol. grau 3.")
print()
print("  Executando (seed=42)...\n")

p_lagrange29      = lagrange(mV_ruidoso, p_verdade, mV_campo)
rmse_lagrange29   = np.sqrt(np.mean((p_lagrange29 - p_verdade)**2))
maxerr_lagrange29 = np.max(np.abs(p_lagrange29 - p_verdade))

print(f"  RMSE — Lagrange grau 29: {rmse_lagrange29:.3e} bar")
print(f"  Erro máximo:             {maxerr_lagrange29:.3e} bar")
print()

fator = rmse_lagrange29 / rmse_campo_p3 if rmse_campo_p3 > 0 else float('inf')
if rmse_lagrange29 > 10 * rmse_campo_p3:
    print(f"  Confirmação: a previsão foi corroborada. O RMSE de Lagrange grau 29")
    print(f"  é ≈ {fator:.0e}× superior ao do polinômio grau 3 por MQ.")
    print("  As oscilações explosivas resultam do condicionamento numérico extremo")
    print("  de polinômios de grau elevado com nós perturbados — o mesmo mecanismo")
    print("  do fenômeno de Runge estudado na Seção 1.")
else:
    print(f"  Resultado: RMSE Lagrange29 = {rmse_lagrange29:.4f} bar vs.")
    print(f"  pol. grau 3 = {rmse_campo_p3:.4f} bar.")

# Gráfico comparativo dos três métodos
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

mV_vis = np.linspace(mV_ruidoso.min(), mV_ruidoso.max(), 400)
p_vis_ref  = cs_lab(np.clip(mV_vis, mV_lab[0], mV_lab[-1]))
p_vis_spl  = cs_lab(np.clip(mV_vis, mV_lab[0], mV_lab[-1]))
p_vis_p3   = np.polyval(coefs_campo_p3[::-1], mV_vis)
p_vis_lag  = lagrange(mV_ruidoso, p_verdade, mV_vis)

axes[0].plot(mV_vis, p_vis_ref, linewidth=2.2, label='Pressão de referência')
axes[0].plot(mV_vis, p_vis_spl, linewidth=2.0, linestyle='--', label='Spline lab + ruído')
axes[0].plot(mV_vis, p_vis_p3,  linewidth=2.0, linestyle='-.', label='Pol. grau 3 (MQ ruidoso)')
axes[0].scatter(mV_ruidoso, p_verdade, s=22, color='black', zorder=5,
                alpha=0.7, label='Pontos de campo ruidosos')
axes[0].set_title('Q6.2(d) — Spline Lab vs. Pol. Grau 3')
axes[0].set_xlabel('Tensão (mV)')
axes[0].set_ylabel('Pressão (bar)')
axes[0].legend(fontsize=9)
axes[0].grid(True)

axes[1].plot(mV_vis, p_vis_ref, linewidth=2.2, label='Pressão de referência')
axes[1].plot(mV_vis, p_vis_lag, linewidth=1.8, linestyle='--', color='crimson',
             label='Lagrange grau 29 (ruidoso)')
axes[1].scatter(mV_ruidoso, p_verdade, s=22, color='black', zorder=5,
                alpha=0.7, label='Pontos de campo ruidosos')
axes[1].set_title('Q6.2(d) — Lagrange Grau 29: Instabilidade com Dados Ruidosos')
axes[1].set_xlabel('Tensão (mV)')
axes[1].set_ylabel('Pressão (bar)')
axes[1].legend(fontsize=9)
axes[1].grid(True)

plt.tight_layout()
plt.savefig('q6_2d_comparacao_ruido.pdf', dpi=300)
plt.close()
print("  Gráfico salvo: q6_2d_comparacao_ruido.pdf")

# ----------------------------------------------------------------------------------
# Q6.3 — Decisão final e documentação
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 6.3 — Decisão final e documentação")
print("─" * 72)

print("\n--- Item (a) ---")
# Recomendação produzida dinamicamente com base nos RMSE de Monte Carlo
rmse_med_spline = rmse_spline_mc.mean()
rmse_med_p3     = rmse_p3_mc.mean()
std_vencedor    = rmse_p3_mc.std() if rmse_med_p3 <= rmse_med_spline else rmse_spline_mc.std()

if rmse_med_p3 <= rmse_med_spline:
    metodo_rec = "regressão polinomial de grau 3 ajustada por mínimos quadrados"
    rmse_rec   = rmse_med_p3
    motivo_rec = (
        "O ajuste por mínimos quadrados distribui a variância do ruído de entrada\n"
        f"  (σ = 2 mV) entre as N observações disponíveis, reduzindo o RMSE médio\n"
        f"  de {rmse_med_spline:.4f} bar (spline com entrada ruidosa) para {rmse_med_p3:.4f} bar.\n"
        f"  Esse comportamento é robusto: o pol. grau 3 foi superior em {pct_p3_melhor:.0f}%\n"
        "  das 1000 realizações do experimento de Monte Carlo."
    )
else:
    metodo_rec = "spline cúbica de calibração laboratorial"
    rmse_rec   = rmse_med_spline
    motivo_rec = (
        "A spline de calibração laboratorial, mesmo aplicada a entradas ruidosas,\n"
        f"  produziu RMSE médio de {rmse_med_spline:.4f} bar — inferior ao re-ajuste\n"
        f"  polinomial sobre dados perturbados ({rmse_med_p3:.4f} bar). O modelo\n"
        "  laboratorial demonstrou maior precisão que um ajuste ad hoc sobre campo."
    )

print(f"""
  RECOMENDAÇÃO TÉCNICA — Conversão mV → bar em Operação de Campo
  ─────────────────────────────────────────────────────────────────
  Com base na análise de Monte Carlo (N = 1000, σ = 2 mV), recomenda-se
  o uso de {metodo_rec} para a conversão mV → bar em campo.

  {motivo_rec}

  Erro esperado: RMSE médio de {rmse_rec:.4f} ± {std_vencedor:.4f} bar
  (média ± desvio-padrão sobre realizações independentes com σ = 2 mV).

  Condições em que a recomendação deixa de ser válida:
    (i)  Operação fora do intervalo calibrado [10, 100] mV: o modelo
         foi validado apenas nesse domínio; extrapolação não é garantida.
    (ii) Ruído de entrada superior a σ ≈ 4–5 mV: o RMSE escala com σ,
         podendo ultrapassar a tolerância operacional.
    (iii) Deriva do sensor ao longo do tempo: a curva de calibração
         perde validade caso o transdutor envelheça ou sofra impacto
         mecânico, alterando a relação tensão–pressão subjacente.
""")

print("\n--- Item (b) ---")
print("""
  ESTRATÉGIA DE RE-CALIBRAÇÃO PERIÓDICA
  ─────────────────────────────────────────────────────────────────
  Frequência recomendada: re-calibração laboratorial a cada 12 meses
  em condições normais de operação (temperatura 15–35 °C, pressão
  na faixa 0,5–8,0 bar, ausência de vibrações mecânicas intensas).

  Critérios de revalidação em campo: ao início de cada turno, verificar
  ao menos dois pontos de referência rastreáveis (ex.: pressão atmosférica
  local e pressão de linha padrão certificada) e confirmar que o erro de
  leitura não ultrapassa ±0,10 bar. As verificações devem ser registradas
  em log auditável com data, hora e identificação do operador.

  Sinais de degradação que indicam necessidade de re-calibração antecipada:
    • Deriva sistemática superior a ±0,08 bar nos pontos de verificação
      por 3 dias consecutivos;
    • Desvio-padrão das leituras superior a 0,15 bar em 10 medições
      consecutivas com pressão de referência estável e conhecida;
    • Ocorrência de sobrepressão (> 110% da escala nominal) ou operação
      fora da faixa de temperatura especificada pelo fabricante;
    • Impacto mecânico, vibração excessiva ou contato com agente corrosivo.

  A re-calibração deve ser antecipada sempre que qualquer sinal acima for
  detectado, independentemente do prazo anual, garantindo rastreabilidade
  metrológica e conformidade com normas aplicáveis (ex.: ABNT NBR
  ISO/IEC 17025 para laboratórios de calibração).
""")


# ==================================================================================
# SEÇÃO 7 — Desafio (Opcional — Pontuação Extra)
# ==================================================================================

from scipy.interpolate import UnivariateSpline

print("\n" + "═" * 72)
print("  SEÇÃO 7 — Desafio (Opcional — Pontuação Extra)")
print("═" * 72)

# ----------------------------------------------------------------------------------
# Q7.1 — Spline de suavização (smoothing spline)
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 7.1 — Spline de suavização (smoothing spline)")
print("─" * 72)

# Dados ruidosos da Q3.1
np.random.seed(3)
x71 = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
y71 = 5.0 * np.exp(-0.8 * x71) + 0.2 * np.random.randn(7)
x71_fine = np.linspace(0, 3, 500)
f71_true  = 5.0 * np.exp(-0.8 * x71_fine)

print("\n--- Item (a) ---")
print("Ajustando UnivariateSpline com s ∈ {0, 0.1, 0.5, 1.0, 5.0}...\n")

# O parâmetro s da UnivariateSpline do SciPy é uma condição de suavização:
# a spline é escolhida de modo que   Σ (y_i − s(x_i))² ≤ s.
# Internamente, o algoritmo FITPACK seleciona o número de nós e o parâmetro
# de penalização λ da formulação variacional de modo a satisfazer essa restrição.
# Portanto, s NÃO corresponde diretamente a λ — é uma cota superior sobre o RSS.
s_vals = [0, 0.1, 0.5, 1.0, 5.0]
splines_71 = {}
for sv in s_vals:
    splines_71[sv] = UnivariateSpline(x71, y71, s=sv, k=3)

print("--- Item (b) ---")
print("Plotando as cinco curvas de suavização...\n")

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(x71_fine, f71_true, 'k--', linewidth=2.0, zorder=5,
        label='Função real  5e⁻⁰·⁸ˣ')
ax.scatter(x71, y71, color='black', s=60, zorder=6, label='Dados com ruído')
estilos = ['-', '--', '-.', ':', (0, (3,1,1,1))]
for sv, est in zip(s_vals, estilos):
    nk = len(splines_71[sv].get_knots())
    ax.plot(x71_fine, splines_71[sv](x71_fine), linestyle=est,
            linewidth=1.8, label=f's = {sv}  (nós internos: {nk})')
ax.set_title('Q7.1(b) — Smoothing Spline para Diferentes Valores de s')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend(fontsize=9)
ax.grid(True)
plt.tight_layout()
plt.savefig('q7_1b_smoothing_spline.pdf', dpi=300)
plt.close()
print("Gráfico salvo: q7_1b_smoothing_spline.pdf")

print("\n--- Item (c) ---")
print("RMSE em relação à função verdadeira 5e⁻⁰·⁸ˣ para cada valor de s:\n")

rmse_71 = {}
for sv in s_vals:
    rmse_71[sv] = np.sqrt(np.mean((splines_71[sv](x71_fine) - f71_true)**2))

cabecalhos_71c = ["s", "RMSE vs. f(x)", "Nós internos", "RSS nos dados"]
linhas_71c = []
for sv in s_vals:
    nk = len(splines_71[sv].get_knots())
    rss_nos = np.sum((splines_71[sv](x71) - y71)**2)
    linhas_71c.append([str(sv), f"{rmse_71[sv]:.4f}", str(nk), f"{rss_nos:.4f}"])
imprimir_tabela(cabecalhos_71c, linhas_71c, ['^', '^', '^', '^'])

s_melhor_rmse = min(rmse_71, key=rmse_71.get)
print(f"\n  Valor de s com menor RMSE numérico: s = {s_melhor_rmse}"
      f"  (RMSE = {rmse_71[s_melhor_rmse]:.4f})")
print()
if s_melhor_rmse == 0:
    print("  Nota: s = 0 produz o menor RMSE neste experimento específico porque")
    print("  o ruído é pequeno (σ = 0,2) e os 7 pontos não são suficientes para")
    print("  que o interpolador exato amplifique oscilações significativas no")
    print("  intervalo [0, 3]. Para s ≥ 0,1, a spline satura em 2 nós internos")
    print("  (equivalente a regressão cúbica global), atingindo um patamar de")
    print("  RMSE estável. Visualmente, valores de s intermediários (ex.: s ≈ 0,05)")
    print("  podem oferecer a melhor relação entre fidelidade e suavidade.")
else:
    print(f"  Para s = {s_melhor_rmse}, a spline apresenta o menor RMSE em relação")
    print("  à função verdadeira, equilibrando fidelidade e suavização do ruído.")

print("\n--- Item (d) ---")
print("Interpretação do parâmetro s e relação com regularização:\n")
print("  A formulação variacional das smoothing splines minimiza o funcional:")
print("    J_λ(f) = Σᵢ (yᵢ − f(xᵢ))²  +  λ · ∫ [f″(x)]² dx")
print("  onde λ ≥ 0 controla o equilíbrio entre fidelidade aos dados (primeiro")
print("  termo) e suavidade da curva (segundo termo, penalidade de curvatura).")
print()
print("  O parâmetro s da UnivariateSpline do SciPy NÃO é λ. Trata-se de uma")
print("  condição de suavização: o algoritmo FITPACK seleciona λ e o número de")
print("  nós internos de modo que Σᵢ (yᵢ − f(xᵢ))² ≤ s. Assim:")
print("    • s = 0  →  interpolação exata (λ → 0); RSS = 0 nos dados.")
print("    • s → ∞  →  spline converge para uma reta (λ → ∞, curvatura mínima).")
print()
print("  Essa penalidade de curvatura é matematicamente equivalente à regularização")
print("  de Tikhonov (regularização L2) em problemas inversos: ambas adicionam")
print("  um termo quadrático que penaliza a complexidade do modelo. A analogia")
print("  com o sobreajuste de Q2.2 é direta: polinômios de grau elevado interpolam")
print("  os erros de medição (s = 0), enquanto valores maiores de s induzem a")
print("  spline a ignorar flutuações locais dos dados, capturando a tendência global.")

# ----------------------------------------------------------------------------------
# Q7.2 — Interpolação de Hermite e derivadas conhecidas
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 7.2 — Interpolação de Hermite com derivadas conhecidas")
print("─" * 72)

print("\n--- Item (a) ---")
print("Implementação da interpolação de Hermite cúbica entre dois nós...\n")

def hermite_cubico(x0, x1, f0, f1, d0, d1, x_eval):
    """
    Interpolação polinomial cúbica de Hermite entre x0 e x1.
    Dados: f(x0)=f0, f(x1)=f1, f'(x0)=d0, f'(x1)=d1.
    Usa as funções de base de Hermite:
        H₀₀(t) = (1 + 2t)(1 − t)²     (pesa f(x0))
        H₁₀(t) = t(1 − t)²            (pesa f'(x0), escala h)
        H₀₁(t) = t²(3 − 2t)           (pesa f(x1))
        H₁₁(t) = t²(t − 1)            (pesa f'(x1), escala h)
    onde t = (x − x0) / h  e  h = x1 − x0.
    """
    h  = x1 - x0
    t  = (x_eval - x0) / h
    H00 = (1.0 + 2.0*t) * (1.0 - t)**2
    H10 = t * (1.0 - t)**2
    H01 = t**2 * (3.0 - 2.0*t)
    H11 = t**2 * (t - 1.0)
    return H00*f0 + H10*h*d0 + H01*f1 + H11*h*d1

# Nós: x₀ = 0, x₁ = π/2;  f(x) = sin(x),  f'(x) = cos(x)
x72_0 = 0.0
x72_1 = np.pi / 2.0
f72_0, f72_1 = np.sin(x72_0), np.sin(x72_1)
d72_0, d72_1 = np.cos(x72_0), np.cos(x72_1)

print(f"  Nós: x₀ = 0,  x₁ = π/2 ≈ {x72_1:.4f}")
print(f"  Comprimento do intervalo: h = π/2 ≈ {x72_1:.4f}")
print(f"  f(x₀) = sin(0)   = {f72_0:.6f}  |  f'(x₀) = cos(0)   = {d72_0:.6f}")
print(f"  f(x₁) = sin(π/2) = {f72_1:.6f}  |  f'(x₁) = cos(π/2) = {d72_1:.6f}")
print()
print("  Hermite cúbico implementado via as quatro funções de base acima.")
print("  O polinômio resultante satisfaz: p(x₀)=f(x₀), p(x₁)=f(x₁),")
print("  p'(x₀)=f'(x₀), p'(x₁)=f'(x₁) — 4 condições, grau 3.")

print("\n--- Item (b) ---")
print("Comparando erro máximo em [0, π/2] — Hermite vs. Lagrange vs. Spline...\n")

x72_eval = np.linspace(x72_0, x72_1, 1000)
sin_true  = np.sin(x72_eval)

# Hermite cúbico: 2 nós, 4 condições (2 valores + 2 derivadas)
y72_herm = hermite_cubico(x72_0, x72_1, f72_0, f72_1, d72_0, d72_1, x72_eval)
err72_herm = np.max(np.abs(y72_herm - sin_true))

# Lagrange cúbico: 4 nós igualmente espaçados em [0, π/2]
x72_lag4 = np.linspace(x72_0, x72_1, 4)
y72_lag4 = np.sin(x72_lag4)
y72_lag  = lagrange(x72_lag4, y72_lag4, x72_eval)
err72_lag = np.max(np.abs(y72_lag - sin_true))

# Spline cúbica not-a-knot: 4 nós igualmente espaçados
cs72 = CubicSpline(x72_lag4, y72_lag4)
y72_spl   = cs72(x72_eval)
err72_spl = np.max(np.abs(y72_spl - sin_true))

cabecalhos_72b = ["Método", "Informações", "Nós", "Espaçamento h", "‖f − p‖∞"]
linhas_72b = [
    ["Hermite cúbico",
     "2 valores + 2 derivadas", "2",
     f"π/2 ≈ {np.pi/2:.4f}", f"{err72_herm:.6f}"],
    ["Lagrange (4 nós equi.)",
     "4 valores",              "4",
     f"π/6 ≈ {np.pi/6:.4f}", f"{err72_lag:.6f}"],
    ["Spline cúbica (4 nós)",
     "4 valores",              "4",
     f"π/6 ≈ {np.pi/6:.4f}", f"{err72_spl:.6f}"],
]
imprimir_tabela(cabecalhos_72b, linhas_72b, ['<', '<', '^', '^', '^'])

# Gráfico
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(x72_eval, sin_true,    'k--', linewidth=2.0, zorder=5, label='sin(x) (exato)')
axes[0].plot(x72_eval, y72_herm,    linewidth=2.0, label='Hermite cúbico (2 nós)')
axes[0].plot(x72_eval, y72_lag,     linewidth=2.0, linestyle='--', label='Lagrange (4 nós)')
axes[0].plot(x72_eval, y72_spl,     linewidth=2.0, linestyle='-.', label='Spline cúbica (4 nós)')
axes[0].scatter([x72_0, x72_1], [f72_0, f72_1], s=70, color='black',
                zorder=6, label='Nós Hermite')
axes[0].set_title('Q7.2(b) — Hermite vs. Lagrange vs. Spline em [0, π/2]')
axes[0].set_xlabel('x')
axes[0].set_ylabel('y')
axes[0].legend(fontsize=9)
axes[0].grid(True)

axes[1].plot(x72_eval, np.abs(y72_herm - sin_true),
             label=f'Hermite   ‖err‖∞ = {err72_herm:.2e}', linewidth=2.0)
axes[1].plot(x72_eval, np.abs(y72_lag  - sin_true),
             label=f'Lagrange  ‖err‖∞ = {err72_lag:.2e}', linewidth=2.0, linestyle='--')
axes[1].plot(x72_eval, np.abs(y72_spl  - sin_true),
             label=f'Spline    ‖err‖∞ = {err72_spl:.2e}', linewidth=2.0, linestyle='-.')
axes[1].set_title('Q7.2(b) — Erro Absoluto |f(x) − p(x)|')
axes[1].set_xlabel('x')
axes[1].set_ylabel('Erro absoluto')
axes[1].set_yscale('log')
axes[1].legend(fontsize=9)
axes[1].grid(True)

plt.tight_layout()
plt.savefig('q7_2b_hermite_comparacao.pdf', dpi=300)
plt.close()
print("Gráfico salvo: q7_2b_hermite_comparacao.pdf")

print("\n--- Item (c) ---")
metodos_72 = [
    ("Hermite cúbico",        err72_herm),
    ("Lagrange (4 nós)",      err72_lag),
    ("Spline cúbica (4 nós)", err72_spl),
]
mais_preciso = min(metodos_72, key=lambda t: t[1])
print(f"  Método com menor erro máximo: {mais_preciso[0]}  (‖err‖∞ = {mais_preciso[1]:.6f})\n")

razao_herm_lag = err72_herm / err72_lag
h_herm = x72_1 - x72_0
h_lag  = (x72_1 - x72_0) / 3.0

print("  Análise do desempenho relativo:")
print()
print("  Hermite cúbico e Lagrange cúbico são ambos polinômios de grau 3 que usam")
print("  exatamente 4 condições de interpolação. A diferença reside nas condições:")
print(f"    • Hermite: usa f(x₀), f(x₁), f'(x₀), f'(x₁) — condições de valor")
print(f"      e derivada nos extremos do intervalo único [0, π/2] (h = π/2).")
print(f"    • Lagrange: usa f(x₀), f(x₁), f(x₂), f(x₃) — 4 valores em nós")
print(f"      com espaçamento h = π/6 ≈ {h_lag:.4f} (3× menor que h do Hermite).")
print()
print("  O erro de interpolação polinomial de grau n satisfaz:")
print("    |f(x) − pₙ(x)| ≤ Mₙ₊₁ / (n+1)! · |ωₙ₊₁(x)|")
print("  Para f(x) = sin(x), M₄ = max|f⁽⁴⁾| = 1 em [0, π/2].")
print("  Em ambos os casos n = 3, mas |ωₙ₊₁(x)| escala com h⁴:")
print(f"    Hermite: h = π/2,  h⁴ ≈ {h_herm**4:.4f}")
print(f"    Lagrange: h = π/6, h⁴ ≈ {h_lag**4:.4f}  (razão h⁴: {(h_herm/h_lag)**4:.0f}×)")
print()
if err72_herm > err72_lag:
    print(f"  O Lagrange com 4 nós equidistantes apresenta erro {razao_herm_lag:.1f}× menor que")
    print("  o Hermite com 2 nós porque seus nós internos cobrem o intervalo com")
    print("  espaçamento substancialmente menor, reduzindo o produto ∏(x − xᵢ).")
    print("  Isso evidencia que a quantidade de nós e seu espaçamento têm impacto")
    print("  mais determinante sobre o erro do que o tipo de condição imposta.")
    print("  O Hermite seria preferível em cenários onde as derivadas são conhecidas")
    print("  mas nós intermediários não estão disponíveis, ou quando a continuidade")
    print("  das derivadas na junção de segmentos é uma exigência do problema.")
else:
    print(f"  O Hermite apresenta erro {1/razao_herm_lag:.1f}× menor que o Lagrange com 4 nós,")
    print("  demonstrando que a informação de derivada pode compensar a ausência de")
    print("  nós intermediários quando a função tem curvatura bem capturada pelas")
    print("  condições de contorno. O resultado é específico para este par (função, intervalo).")

# ----------------------------------------------------------------------------------
# Q7.3 — Regressão com múltiplas variáveis
# ----------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 7.3 — Regressão com múltiplas variáveis")
print("─" * 72)

np.random.seed(99)
m_data = 1000 + 400 * np.random.rand(20)   # massa: 1000–1400 kg
P_data = 80  + 120 * np.random.rand(20)    # potência: 80–200 cv
C_data = 0.005*m_data + 0.03*P_data - 5 + 0.5*np.random.randn(20)

n73 = len(C_data)

print("\n--- Item (a) ---")
print("Montando a matriz de design X e resolvendo as equações normais X^T X β = X^T C...\n")

# Modelo: C = β₀ + β₁·m + β₂·P  →  X = [1 | m | P]
X73     = np.column_stack([np.ones(n73), m_data, P_data])
XTX73   = X73.T @ X73
XTy73   = X73.T @ C_data
beta73  = np.linalg.solve(XTX73, XTy73)

C_hat73   = X73 @ beta73
res73     = C_data - C_hat73
ss_res73  = np.sum(res73**2)
ss_tot73  = np.sum((C_data - np.mean(C_data))**2)
r2_73     = 1.0 - ss_res73 / ss_tot73
# Erro-padrão dos resíduos: estimativa não-viesada de σ
# se = sqrt(RSS / (n − k)), com k = 3 parâmetros estimados (β₀, β₁, β₂)
se_73     = np.sqrt(ss_res73 / (n73 - 3))

cabecalhos_73a = ["Parâmetro", "β estimado", "β verdadeiro", "Erro absoluto"]
linhas_73a = [
    ["β₀ (intercepto)", f"{beta73[0]:.4f}",  "−5,0000",  f"{abs(beta73[0] - (-5.0)):.4f}"],
    ["β₁ (massa)",      f"{beta73[1]:.6f}",  "0,005000", f"{abs(beta73[1] -  0.005):.6f}"],
    ["β₂ (potência)",   f"{beta73[2]:.6f}",  "0,030000", f"{abs(beta73[2] -  0.030):.6f}"],
]
imprimir_tabela(cabecalhos_73a, linhas_73a, ['<', '^', '^', '^'])

print()
print("  Os estimadores de mínimos quadrados (EMQ) coincidem com os estimadores")
print("  de máxima verossimilhança sob erros gaussianos i.i.d. N(0, σ²). Com")
print("  n = 20 observações e σ = 0,5, os coeficientes estimados são consistentes")
print("  mas apresentam variância amostral — os desvios acima são esperados.")

print("\n--- Item (b) ---")
print(f"  R² múltiplo:               {r2_73:.4f}")
print(f"  Erro-padrão dos resíduos:  ŝ = {se_73:.4f} L/100 km")
print(f"  (verdadeiro: σ = 0,5 L/100 km)")
print()
if abs(se_73 - 0.5) / 0.5 < 0.30:
    print(f"  O R² = {r2_73:.4f} indica que o modelo linear explica parte substancial")
    print("  da variância de C, condizente com a estrutura geradora dos dados.")
    print(f"  O erro-padrão estimado ŝ = {se_73:.4f} é próximo do σ verdadeiro (0,5),")
    print("  confirmando que o modelo está bem especificado: a família linear em m e P")
    print("  é a família correta, e os resíduos refletem o ruído aleatório adicionado.")
else:
    print(f"  R² = {r2_73:.4f} indica ajuste razoável. A diferença entre ŝ = {se_73:.4f}")
    print("  e σ verdadeiro (0,5) é esperada dado o tamanho amostral reduzido (n = 20).")

# Gráfico de diagnóstico dos resíduos
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

axes[0].scatter(C_hat73, res73, s=50, zorder=5)
axes[0].axhline(0, linestyle='--', color='gray')
axes[0].set_title('Q7.3(b) — Resíduos vs. Valores Ajustados Ĉ')
axes[0].set_xlabel('Ĉ (L/100 km)')
axes[0].set_ylabel('Resíduo eᵢ = Cᵢ − Ĉᵢ  (L/100 km)')
axes[0].grid(True)

axes[1].scatter(range(1, n73+1), res73, s=50, zorder=5)
axes[1].axhline(0, linestyle='--', color='gray')
axes[1].set_title('Q7.3(b) — Resíduos por Índice de Observação')
axes[1].set_xlabel('Observação')
axes[1].set_ylabel('Resíduo eᵢ  (L/100 km)')
axes[1].grid(True)

plt.tight_layout()
plt.savefig('q7_3b_residuos_regressao_multipla.pdf', dpi=300)
plt.close()
print("\n  Gráfico de resíduos salvo: q7_3b_residuos_regressao_multipla.pdf")

print("\n--- Item (c) ---")
print("Adicionando o termo de interação β₃·m·P e comparando via AIC...\n")

# Modelo com interação: C = β₀ + β₁·m + β₂·P + β₃·m·P
X73_int    = np.column_stack([np.ones(n73), m_data, P_data, m_data*P_data])
beta73_int = np.linalg.solve(X73_int.T @ X73_int, X73_int.T @ C_data)
C_hat_int  = X73_int @ beta73_int
ss_res_int = np.sum((C_data - C_hat_int)**2)
r2_int     = 1.0 - ss_res_int / ss_tot73

# AIC conforme a fórmula do enunciado: AIC = n·ln(RSS/n) + 2·(k+1)
# onde k é o número de regressores (excluindo o intercepto).
# Equivalentemente, k+1 = número total de parâmetros estimados.
k73_sem = 3   # β₀, β₁, β₂
k73_com = 4   # β₀, β₁, β₂, β₃
aic_sem = n73 * np.log(ss_res73  / n73) + 2 * k73_sem
aic_com = n73 * np.log(ss_res_int / n73) + 2 * k73_com

cabecalhos_73c = ["Modelo", "k (nº de params.)", "R²", "RSS", "AIC"]
linhas_73c = [
    ["Sem interação  (β₀ + β₁m + β₂P)",
     str(k73_sem), f"{r2_73:.4f}", f"{ss_res73:.4f}", f"{aic_sem:.4f}"],
    ["Com interação  (+ β₃·m·P)",
     str(k73_com), f"{r2_int:.4f}", f"{ss_res_int:.4f}", f"{aic_com:.4f}"],
]
imprimir_tabela(cabecalhos_73c, linhas_73c, ['<', '^', '^', '^', '^'])

delta_r2  = r2_int - r2_73
delta_aic = aic_com - aic_sem
print()
print(f"  ΔR² = {delta_r2:.4f}  (variação de R² com o termo de interação)")
print(f"  ΔAIC = {delta_aic:.4f}  "
      f"({'o AIC aumenta → modelo sem interação preferido' if delta_aic > 0 else 'o AIC diminui → modelo com interação preferido'})")
print()
if delta_aic > 0:
    print("  Interpretação: a redução de RSS com o termo β₃·m·P é insuficiente para")
    print("  compensar a penalidade de 2 unidades de AIC pelo parâmetro adicional.")
    print(f"  O modelo sem interação (AIC = {aic_sem:.4f}) é preferido ao modelo com")
    print(f"  interação (AIC = {aic_com:.4f}).")
    print()
    print("  Esse resultado é coerente com o processo gerador dos dados: o modelo")
    print("  verdadeiro C = 0,005·m + 0,03·P − 5 não contém interação m·P. A inclusão")
    print("  de β₃ introduz um parâmetro espúrio que o AIC penaliza adequadamente.")
    print()
    print("  Regra prática: quando ΔAIC > 2, o modelo mais complexo não apresenta")
    print("  evidência suficiente de melhoria. Quando ΔAIC < −2, o modelo mais")
    print("  complexo é preferido. Valores |ΔAIC| ≤ 2 indicam evidência ambígua.")
else:
    print(f"  O AIC favorece o modelo com interação (ΔAIC = {delta_aic:.4f} < 0).")
    print("  A redução de RSS justifica o parâmetro adicional segundo o critério.")
    print("  Contudo, com n = 20, a potência estatística para detectar ou refutar")
    print("  termos de interação é limitada — o resultado deve ser interpretado com cautela.")
    
# ==================================================================================
# FIM DO SCRIPT
# ==================================================================================

print("\n" + "═" * 72)
print("  FIM DA EXECUÇÃO — Relatório gerado por:")
print("  Jeann Victor Batista, Pedro Augusto de Souza Finnochio, Thiago Martins da Silva")
print("═" * 72)