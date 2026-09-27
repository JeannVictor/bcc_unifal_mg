# =============================================================================
# main.py
# =============================================================================
# Plano de Investigação Computacional
# Diferenciação e Integração Numéricas:
# Análise, Comparação e Aplicações em Python
# =============================================================================
# Disciplina   : Cálculo Numérico
# Professora   : Angela Leite Moreno
# Aluno 1      : Jeann Victor Batista              R.A          : 2024.1.08.014
# Aluno 2      : Pedro Augusto de Souza Finnochio  R.A          : 2024.1.08.020
# Aluno 3      : Thiago Martins da Silva           R.A          : 2024.1.08.023
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

from diferencas import (
    df_progressiva, df_regressiva, df_central,
    df_prog3, df_retro3, d2f_central,
    derivada_tabela, d2f_tabela
)
from integracao import (
    ponto_medio, trapezios, simpson13,
    trapezios_tabela, simpson13_tabela,
    cota_trapezio, cota_simpson,
    gauss_legendre, tabela_comparativa
)


# =============================================================================
# CONFIGURAÇÃO DOS GRÁFICOS
# =============================================================================

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


# =============================================================================
# UTILITÁRIO PARA TABELAS
# =============================================================================

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


# =============================================================================
# SEÇÃO 1 — Fórmulas de Diferenças Finitas
# =============================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 1 — Fórmulas de Diferenças Finitas")
print("═" * 72)


# ------------------------------------------------------------------------------
# Q1.1 — Fórmulas de dois pontos: f(x)=sin x em x0=π/3
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 1.1 — Fórmulas de dois pontos")
print("─" * 72)

f      = np.sin
x0     = np.pi / 3
exato  = np.cos(x0)          # 0.500000...

print("\n(a) Tabela com h = 0.1 e h = 0.01")

cabecalho = f"  {'Fórmula':<15} {'h':>6}  {'Aprox':>12}  {'Erro |e|':>12}  {'Ordem'}"
separador = "  " + "─" * 62
print(cabecalho)
print(separador)

for h, ordem in [(0.1, "O(h)"), (0.01, "O(h)"), (0.1, "O(h)"), (0.01, "O(h)"),
                 (0.1, "O(h²)"), (0.01, "O(h²)")]:
    pass  # substituído pelo loop abaixo

dados = [
    ("Progressiva",  df_progressiva, "O(h)"),
    ("Regressiva",   df_regressiva,  "O(h)"),
    ("Central",      df_central,     "O(h²)"),
]

erros = {}
for nome, func, ordem in dados:
    erros[nome] = {}
    for h in (0.1, 0.01):
        aprox = func(f, x0, h)
        erro  = abs(aprox - exato)
        erros[nome][h] = erro
        print(f"  {nome:<15} {h:>6.2f}  {aprox:>12.8f}  {erro:>12.2e}  {ordem}")
    print()

print("\n(b) Fatores de redução de erro (h=0.1 → h=0.01)")
print(f"  {'Fórmula':<15}  {'Erro h=0.1':>12}  {'Erro h=0.01':>12}  {'Fator':>8}  {'Esperado':>10}")
print("  " + "─" * 60)
esperados = {"Progressiva": ("O(h)",  10), "Regressiva": ("O(h)", 10), "Central": ("O(h²)", 100)}
for nome, (ordem, fator_esp) in esperados.items():
    e1 = erros[nome][0.1]
    e2 = erros[nome][0.01]
    fator = e1 / e2
    print(f"  {nome:<15}  {e1:>12.2e}  {e2:>12.2e}  {fator:>8.1f}  {fator_esp:>10}×")

print("""
(c) Por que a central é O(h²) com apenas dois pontos ao redor de x0?

    Expansão de Taylor:
      f(x+h) = f(x) + h·f'(x) + h²/2·f''(x) + h³/6·f'''(x) + ...
      f(x-h) = f(x) - h·f'(x) + h²/2·f''(x) - h³/6·f'''(x) + ...

    Subtraindo:  f(x+h) - f(x-h) = 2h·f'(x) + h³/3·f'''(x) + ...
    Dividindo por 2h:
      f'(x) ≈ [f(x+h) - f(x-h)] / (2h)  +  O(h²)

    O termo em h (primeiro erro) cancela por simetria — os termos
    de potência par somam, os ímpares se cancelam. A progressiva
    subtrai f(x+h) - f(x) e o termo h²/2·f''(x) não cancela,
    deixando erro O(h). A central "paga" apenas 2 pontos mas
    aproveita a simetria para eliminar o termo dominante de erro.
""")

# ------------------------------------------------------------------------------
# Q1.2 — Fórmulas de três pontos
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 1.2 — Fórmulas de três pontos")
print("─" * 72)

f     = np.sin
x0    = np.pi / 3
exato = np.cos(x0)

print("\n(a) Tabela com h = 0.1 e h = 0.01")

dados = [
    ("Prog3",    df_prog3,       "O(h²)"),
    ("Retro3",   df_retro3,      "O(h²)"),
    ("Central",  df_central,     "O(h²)"),
]

print(f"  {'Fórmula':<12} {'h':>6}  {'Aprox':>12}  {'Erro |e|':>12}  {'Ordem'}")
print("  " + "─" * 58)

erros = {}
for nome, func, ordem in dados:
    erros[nome] = {}
    for h in (0.1, 0.01):
        aprox = func(f, x0, h)
        erro  = abs(aprox - exato)
        erros[nome][h] = erro
        print(f"  {nome:<12} {h:>6.2f}  {aprox:>12.8f}  {erro:>12.2e}  {ordem}")
    print()

print("\n(b) Fatores de redução de erro (h=0.1 → h=0.01)")
print(f"  {'Fórmula':<12}  {'Erro h=0.1':>12}  {'Erro h=0.01':>12}  {'Fator':>8}  {'Esperado':>10}")
print("  " + "─" * 56)
for nome, _, _ in dados:
    e1    = erros[nome][0.1]
    e2    = erros[nome][0.01]
    fator = e1 / e2
    print(f"  {nome:<12}  {e1:>12.2e}  {e2:>12.2e}  {fator:>8.1f}  {'100':>10}×")

print("""
(c) Por que df_central (2 pts) e df_prog3/df_retro3 (3 pts) têm o mesmo O(h²)?

    df_prog3  usa: -3f(x) + 4f(x+h) - f(x+2h)  dividido por 2h
    df_retro3 usa:  f(x-2h) - 4f(x-h) + 3f(x)  dividido por 2h
    df_central usa: f(x+h) - f(x-h)             dividido por 2h

    A fórmula central de 2 pontos já é O(h²) por cancelamento
    dos termos ímpares na expansão de Taylor (vide Q1.1c).
    As fórmulas de 3 pontos são construídas para atingir O(h²)
    usando apenas pontos de um lado (bordas de tabela), onde a
    central não pode ser aplicada.

    Identidade algébrica (caso df_central = média de prog1 e retro1):

      df_prog  = [f(x+h) - f(x)]   / h  →  f'(x) + h/2·f''(x) + ...
      df_retro = [f(x) - f(x-h)]   / h  →  f'(x) - h/2·f''(x) + ...
      média    = [f(x+h) - f(x-h)] / 2h →  f'(x) + O(h²)   ← é exatamente df_central

    Logo df_central já é a combinação linear ótima de 2 pontos que
    elimina o erro de 1ª ordem. df_prog3/df_retro3 fazem o mesmo
    truque combinando 3 pontos unilaterais para forçar o mesmo
    cancelamento — por isso os três convergem com o mesmo fator ≈100.
""")

# ------------------------------------------------------------------------------
# Q1.3 — Passo ótimo (truncamento vs arredondamento)
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 1.3 — Passo ótimo")
print("─" * 72)

import matplotlib.pyplot as plt

f     = np.exp
x0    = 1.0
exato = np.e          # f'(x) = e^x → f'(1) = e

hs = np.logspace(0, -16, 200)

erros_central = np.array([abs(df_central(f, x0, h)     - exato) for h in hs])
erros_prog    = np.array([abs(df_progressiva(f, x0, h) - exato) for h in hs])

# (a) Gráfico log-log
fig, ax = plt.subplots(figsize=(8, 5))
ax.loglog(hs, erros_central, label="df_central  O(h²)", color="steelblue")
ax.loglog(hs, erros_prog,    label="df_progressiva  O(h)", color="tomato")
ax.axvline(1e-5,  color="steelblue", linestyle="--", linewidth=0.8, label="h_opt central  ≈ 1e-5")
ax.axvline(1e-8,  color="tomato",    linestyle="--", linewidth=0.8, label="h_opt prog     ≈ 1e-8")
ax.set_xlabel("h")
ax.set_ylabel("Erro absoluto")
ax.set_title("Q1.3 — Erro vs passo h  (f = eˣ, x₀ = 1)")
ax.legend()
ax.grid(True, which="both", linestyle=":", linewidth=0.5)
ax.invert_xaxis()   # h decrescendo da esquerda para direita
plt.tight_layout()
plt.savefig("q13_passo_otimo.png", dpi=300)
plt.close()
print("\n  Gráfico salvo: q13_passo_otimo.png")

# (b) h_opt central
idx_c   = np.argmin(erros_central)
hopt_c  = hs[idx_c]
emin_c  = erros_central[idx_c]
print(f"\n(b) df_central")
print(f"    h_opt experimental : {hopt_c:.2e}")
print(f"    h_opt teórico      : 1.00e-05  (εm^(1/3) ≈ (2.2e-16)^(1/3))")
print(f"    Erro mínimo        : {emin_c:.2e}")

# (c) h_opt progressiva
idx_p   = np.argmin(erros_prog)
hopt_p  = hs[idx_p]
emin_p  = erros_prog[idx_p]
print(f"\n(c) df_progressiva")
print(f"    h_opt experimental : {hopt_p:.2e}")
print(f"    h_opt teórico      : 1.00e-08  (εm^(1/2) ≈ (2.2e-16)^(1/2))")
print(f"    Erro mínimo        : {emin_p:.2e}")

# (d) Comparação
razao = emin_p / emin_c
print(f"\n(d) Comparação de erro mínimo")
print(f"    Erro mín central      : {emin_c:.2e}")
print(f"    Erro mín progressiva  : {emin_p:.2e}")
print(f"    Razão (prog / central): {razao:.1f}×  → central é mais precisa")

print("""
  Interpretação:

  À medida que h decresce, dois efeitos competem:
    - Erro de truncamento: cai com h  (O(h²) ou O(h))
    - Erro de arredondamento: sobe com 1/h pois subtrai valores quase iguais

  O mínimo ocorre onde os dois erros se equilibram.  A fórmula teórica
  para esse ponto é:

    df_central    → h_opt ≈ εm^(1/3) ≈ (2.2e-16)^(1/3) ≈ 6e-6  ~ 1e-5
    df_progressiva → h_opt ≈ εm^(1/2) ≈ (2.2e-16)^(1/2) ≈ 1.5e-8 ~ 1e-8

  No mínimo, o erro residual também difere:
    df_central    → erro_min ≈ εm^(2/3) ≈ 1e-10
    df_progressiva → erro_min ≈ εm^(1/2) ≈ 1e-8

  Isso é consistente com as ordens: a central é mais precisa porque
  seu erro de truncamento cai mais rápido (h²), então consegue usar
  h maior antes do arredondamento dominar, e ainda assim termina
  com erro residual menor (~100× melhor que a progressiva).
""")


# ------------------------------------------------------------------------------
# Q1.4 — Diferenciação de tabela experimental (posição × tempo)
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 1.4 — Diferenciação de tabela experimental")
print("─" * 72)

t_pos = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
x_pos = np.array([0.0, 1.2, 4.8, 10.6, 18.5, 27.1, 35.8, 43.6])

# (a) Velocidade
v = derivada_tabela(t_pos, x_pos)

print("\n(a) Velocidade estimada v(t) = x'(t)")
print(f"  {'t (s)':>6}  {'x (m)':>8}  {'v (m/s)':>10}  {'Fórmula'}")
print("  " + "─" * 46)
formulas = ["Prog3 (borda)"] + ["Central"] * 6 + ["Retro3 (borda)"]
for i in range(len(t_pos)):
    print(f"  {t_pos[i]:>6.1f}  {x_pos[i]:>8.1f}  {v[i]:>10.4f}  {formulas[i]}")

# (b) Aceleração
a = d2f_tabela(t_pos, x_pos)

print("\n(b) Aceleração estimada a(t) = x''(t)  (pontos interiores)")
print(f"  {'t (s)':>6}  {'a (m/s²)':>10}")
print("  " + "─" * 20)
for i in range(1, len(t_pos) - 1):
    print(f"  {t_pos[i]:>6.1f}  {a[i]:>10.4f}")

# (c) Mudança de sinal da aceleração
print("\n(c) Análise do sinal da aceleração")
print(f"  {'t (s)':>6}  {'a (m/s²)':>10}  {'Situação'}")
print("  " + "─" * 36)
for i in range(1, len(t_pos) - 1):
    if a[i] > 0:
        sit = "acelerando"
    elif a[i] < 0:
        sit = "FREANDO ◄"
    else:
        sit = "constante"
    print(f"  {t_pos[i]:>6.1f}  {a[i]:>10.4f}  {sit}")

# detectar cruzamento de sinal
for i in range(2, len(t_pos) - 1):
    if a[i-1] * a[i] < 0:
        print(f"\n  → Aceleração muda de sinal entre t={t_pos[i-1]:.1f}s e t={t_pos[i]:.1f}s")

# (d) Incerteza na velocidade
h       = 0.5          # espaçamento da tabela
delta_x = 0.1         # resolução GPS (m)
delta_v = 2 * delta_x / (2 * h)   # fórmula central: (x_{i+1}-x_{i-1})/(2h)

print(f"\n(d) Incerteza na velocidade")
print(f"  Resolução GPS   : ±{delta_x} m")
print(f"  Passo h         :  {h} s")
print(f"  δv = 2·δx/(2h) = 2·{delta_x}/(2·{h}) = {delta_v:.4f} m/s")
print(f"\n  Velocidades com incerteza:")
print(f"  {'t (s)':>6}  {'v (m/s)':>10}  {'Intervalo'}")
print("  " + "─" * 36)
for i in range(len(t_pos)):
    print(f"  {t_pos[i]:>6.1f}  {v[i]:>10.4f}  [{v[i]-delta_v:.4f}, {v[i]+delta_v:.4f}]")

# (e) Discussão
print("""
(e) Com dados experimentais ruidosos, não faz sentido usar h muito pequeno.

  Para dados tabelados com ruído δx, o erro na derivada central é:

      erro ≈  h²/6 · f'''(x)     ← truncamento (cai com h)
            + 2·δx / (2h)        ← propagação do ruído (SOBE com 1/h)

  Ao contrário de f analítica (onde εm ≈ 1e-16 é minúsculo), aqui
  δx = 0.1 m é enorme. Reduzir h aumenta drasticamente o ruído:

      h = 0.5 s  →  δv ≈ 0.20 m/s   (≈ 2% de v_max)
      h = 0.1 s  →  δv ≈ 1.00 m/s   (≈ 10% de v_max)
      h = 0.01 s →  δv ≈ 10.0 m/s   (inutilizável)

  Com dados experimentais, o passo mínimo útil é limitado pela
  resolução do instrumento, não pela precisão de máquina. O h_opt
  real balanceia truncamento e ruído de medição — e com GPS de 0.1 m,
  h = 0.5 s já está próximo desse ponto ótimo.
""")


# ------------------------------------------------------------------------------
# Q1.5 — Segunda derivada de ln x em x0=2
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 1.5 — Segunda derivada de ln x")
print("─" * 72)

f     = np.log
x0    = 2.0
exato = -1/4      # f''(x) = -1/x²  →  f''(2) = -0.25

# (a) Estimativa com h=0.1
h01    = 0.1
aprox1 = d2f_central(f, x0, h01)
erro1  = abs(aprox1 - exato)

print("\n(a) Estimativa com h = 0.1")
print(f"  f(1.9) = ln(1.9) = {np.log(1.9):.8f}")
print(f"  f(2.0) = ln(2.0) = {np.log(2.0):.8f}")
print(f"  f(2.1) = ln(2.1) = {np.log(2.1):.8f}")
print(f"  f''(2) ≈ [f(1.9) - 2f(2.0) + f(2.1)] / h²")
print(f"         = {aprox1:.8f}")
print(f"  Exato  = {exato:.8f}")
print(f"  Erro   = {erro1:.2e}")

# (b) Cota teórica: |E| ≤ h²/12 · max|f⁽⁴⁾(ξ)|  com ξ ∈ [1.9, 2.1]
# f⁽⁴⁾(x) = 6/x⁴  →  máximo em x=1.9 (extremo esquerdo)
f4max = 6 / 1.9**4
cota1 = h01**2 / 12 * f4max

print(f"\n(b) Cota teórica do erro (h = 0.1)")
print(f"  f⁽⁴⁾(x) = 6/x⁴  →  máx em ξ = 1.9:  f⁽⁴⁾(1.9) = {f4max:.6f}")
print(f"  Cota = h²/12 · f⁽⁴⁾(ξ) = {h01}²/12 · {f4max:.6f} = {cota1:.2e}")
print(f"  Erro real                                           = {erro1:.2e}")
print(f"  Cota ≥ erro real? {'Sim ✓' if cota1 >= erro1 else 'Não ✗'}")

# (c) Repetição para h=0.05 e h=0.01 — verificar fator 4
hs     = [0.1, 0.05, 0.01]
aproxs = [d2f_central(f, x0, h) for h in hs]
erros  = [abs(a - exato) for a in aproxs]

print("\n(c) Convergência — fator 4 a cada h → h/2")
print(f"  {'h':>6}  {'Aprox':>12}  {'Erro':>10}  {'Fator e_ant/e_atual':>20}")
print("  " + "─" * 54)
for i, (h, ap, er) in enumerate(zip(hs, aproxs, erros)):
    if i == 0:
        fator_str = "—"
    else:
        fator_str = f"{erros[i-1]/er:.2f}×"
    print(f"  {h:>6.2f}  {ap:>12.8f}  {er:>10.2e}  {fator_str:>20}")

print("""
  Interpretação:

  d2f_central tem erro O(h²): ao reduzir h por fator r, o erro
  cai por r². Aqui:
    h=0.10 → h=0.05: r=2  →  fator esperado 4×
    h=0.05 → h=0.01: r=5  →  fator esperado 25×

  Os fatores numéricos confirmam essa relação quadrática.
  A cota teórica (h²/12)·max|f⁽⁴⁾| é válida pois é sempre
  maior ou igual ao erro real observado.
""")


# =============================================================================
# SEÇÃO 2 — Newton-Cotes: Trapézios e Simpson
# =============================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 2 — Newton-Cotes: Trapézios e Simpson")
print("═" * 72)


# ------------------------------------------------------------------------------
# Q2.1 — Verificação: ∫₀¹ x² dx e ∫₀¹ x³ dx
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 2.1 — Verificação das fórmulas")
print("─" * 72)

a, b, n = 0.0, 1.0, 4

# ── integrais e exatos ────────────────────────────────────────────────────────
casos = [
    ("∫₀¹ x² dx", lambda x: x**2, 1/3,  "grau 2"),
    ("∫₀¹ x³ dx", lambda x: x**3, 1/4,  "grau 3"),
]

print("""
(a) Expectativa antes de calcular

  Ponto Médio  →  exato para polinômios de grau ≤ 1  (regra de ordem 2,
                  mas integra x¹ exatamente; x² já tem erro de truncamento)
  Trapézios    →  exato para grau ≤ 1
  Simpson 1/3  →  exato para grau ≤ 3  (usa polinômio interpolador de grau 2,
                  mas o erro envolve f⁽⁴⁾ — zero para grau ≤ 3)

  Portanto:
    ∫ x² dx  →  Simpson exato (grau 2 ≤ 3); Ponto Médio e Trapézios com erro
    ∫ x³ dx  →  Simpson ainda exato (grau 3 ≤ 3); demais com erro
""")

print("(b/c) Resultados numéricos")
print()

for titulo, f, exato, grau in casos:
    PM = ponto_medio(f, a, b, n)
    TR = trapezios(f, a, b, n)
    SI = simpson13(f, a, b, n)

    print(f"  {titulo}  (exato = {exato:.6f}, {grau})")
    print(f"  {'Método':<15} {'Resultado':>14} {'Erro':>12}  {'Exato?'}")
    print("  " + "─" * 50)
    for nome, val in [("Ponto Médio", PM), ("Trapézios", TR), ("Simpson 1/3", SI)]:
        erro   = abs(val - exato)
        exato_str = "SIM ✓" if erro < 1e-12 else f"não  ({erro:.2e})"
        print(f"  {nome:<15} {val:>14.10f} {erro:>12.2e}  {exato_str}")
    print()

print("""
  Interpretação:

  Simpson 1/3 integra exatamente polinômios de grau ≤ 3 porque
  ajusta uma parábola (grau 2) em cada par de subintervalos, e a
  regra resulta em um esquema cuja fórmula de erro contém f⁽⁴⁾(ξ).
  Para f(x) = x² ou x³, f⁽⁴⁾ ≡ 0  →  erro exatamente zero,
  independente de n.

  Ponto Médio e Trapézios têm erro proporcional a f''(ξ):
    f(x) = x²  →  f'' = 2  (constante, erro ≠ 0)
    f(x) = x³  →  f'' = 6x (não nula, erro ≠ 0)

  Ponto Médio subestima e Trapézios superestima para funções
  convexas (f'' > 0) — os erros têm sinais opostos, o que é
  visível nos resultados: PM < exato < TR.
""")

# ------------------------------------------------------------------------------
# Q2.2 — ∫₁² 1/x dx com n=4,8,16
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 2.2 — ∫₁² 1/x dx")
print("─" * 72)

f     = lambda x: 1/x
a, b  = 1.0, 2.0
exato = np.log(2)
ns    = [4, 8, 16]

# (a) Tabela comparativa
print(f"\n(a) Tabela comparativa  (exato = ln 2 = {exato:.8f})")
print(f"  {'n':>4}  {'Trapézios':>12}  {'Erro TR':>10}  {'Simpson 1/3':>12}  {'Erro SI':>10}")
print("  " + "─" * 56)

erros_tr = {}
erros_si = {}
for n in ns:
    TR = trapezios(f, a, b, n)
    SI = simpson13(f, a, b, n)
    erros_tr[n] = abs(TR - exato)
    erros_si[n] = abs(SI - exato)
    print(f"  {n:>4}  {TR:>12.8f}  {erros_tr[n]:>10.2e}  {SI:>12.8f}  {erros_si[n]:>10.2e}")

# (b) Fatores de redução ao dobrar n
print(f"\n(b) Fatores de redução ao dobrar n")
print(f"  {'n→2n':>8}  {'Fator TR':>10}  {'Esperado':>10}  {'Fator SI':>10}  {'Esperado':>10}")
print("  " + "─" * 52)
pares = [(4, 8), (8, 16)]
for n1, n2 in pares:
    ftr = erros_tr[n1] / erros_tr[n2]
    fsi = erros_si[n1] / erros_si[n2]
    print(f"  {n1}→{n2:>2}      {ftr:>10.2f}  {'4':>10}       {fsi:>10.2f}  {'16':>10}")

# (c) Razão de precisão com n=4
razao = erros_tr[4] / erros_si[4]
pts_tr = 4 + 1   # trapézios com n=4 usa 5 pontos
pts_si = 4 + 1   # simpson com n=4 usa 5 pontos

print(f"\n(c) Comparação com n = 4  (ambos usam {pts_tr} pontos de avaliação)")
print(f"  Erro Trapézios  : {erros_tr[4]:.2e}")
print(f"  Erro Simpson    : {erros_si[4]:.2e}")
print(f"  Razão           : {razao:.1f}×  →  Simpson é {razao:.0f}× mais preciso")

print(f"""
  Interpretação:

  Trapézios interpola f por segmentos lineares (grau 1) em cada
  subintervalo. O erro por subintervalo é proporcional a h³·f''(ξ),
  acumulando O(h²) = O(n⁻²) globalmente. Ao dobrar n:
    fator esperado = 2² = 4  →  observado ≈ {erros_tr[4]/erros_tr[8]:.1f}×  ✓

  Simpson interpola por parábolas (grau 2) em cada par de
  subintervalos. O erro por par é proporcional a h⁵·f⁽⁴⁾(ξ),
  acumulando O(h⁴) = O(n⁻⁴) globalmente. Ao dobrar n:
    fator esperado = 2⁴ = 16  →  observado ≈ {erros_si[4]/erros_si[8]:.1f}×  ✓

  Com n=4, os dois métodos avaliam f nos mesmos 5 pontos
  x = 1.00, 1.25, 1.50, 1.75, 2.00, mas com pesos diferentes:

    Trapézios:  h/2  · [1, 2, 2, 2, 1]
    Simpson:    h/3  · [1, 4, 2, 4, 1]

  Simpson atribui peso maior aos pontos intermediários (4 vs 2),
  o que equivale a ajustar uma parábola em vez de uma reta em cada
  par — capturando melhor a curvatura de 1/x sem custo extra de
  avaliações de função.
""")


# ------------------------------------------------------------------------------
# Q2.3 — Cotas de erro e determinação de n
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 2.3 — Cotas de erro")
print("─" * 72)

tol = 1e-5

# ══════════════════════════════════════════════════════════════════════════════
# (a) ∫₀^π sin x dx  — Trapézios
# ══════════════════════════════════════════════════════════════════════════════
fa, fb  = 0.0, np.pi
exato_a = 2.0
f2max_a = 1.0          # max |f''| = max |sin x| em [0,π] = 1

# cota: (b-a)³/(12n²) · f2max ≤ tol  →  n ≥ sqrt((b-a)³·f2max / (12·tol))
n_teo_a = np.sqrt((fb - fa)**3 * f2max_a / (12 * tol))
n_teo_a = int(np.ceil(n_teo_a))

# verificação experimental: menor n que realmente atinge tol
n_exp_a = 1
while abs(trapezios(np.sin, fa, fb, n_exp_a) - exato_a) > tol:
    n_exp_a += 1

cota_teo_a = cota_trapezio(f2max_a, fa, fb, n_teo_a)
erro_teo_a = abs(trapezios(np.sin, fa, fb, n_teo_a) - exato_a)
erro_exp_a = abs(trapezios(np.sin, fa, fb, n_exp_a) - exato_a)

print(f"""
(a) ∫₀^π sin x dx = 2  — Trapézios  (tolerância = {tol:.0e})

  Cota:  |E| ≤ (b-a)³·max|f''| / (12n²) ≤ tol
         n  ≥ sqrt(π³·1 / (12·{tol:.0e}))
         n  ≥ sqrt({(fb-fa)**3 * f2max_a / (12*tol):.2f})
         n  ≥ {np.sqrt((fb-fa)**3*f2max_a/(12*tol)):.4f}  →  n_teórico = {n_teo_a}

  {'Grandeza':<28} {'Valor':>12}
  {'─'*42}
  {'n teórico (cota)':<28} {n_teo_a:>12d}
  {'Cota garantida p/ n_teo':<28} {cota_teo_a:>12.2e}
  {'Erro real com n_teo':<28} {erro_teo_a:>12.2e}
  {'n experimental (mínimo)':<28} {n_exp_a:>12d}
  {'Erro real com n_exp':<28} {erro_exp_a:>12.2e}
""")

# ══════════════════════════════════════════════════════════════════════════════
# (b) ∫₀¹ e^x dx  — Simpson 1/3
# ══════════════════════════════════════════════════════════════════════════════
ga, gb  = 0.0, 1.0
exato_b = np.e - 1
f4max_b = np.e             # max |f⁽⁴⁾| = max eˣ em [0,1] = e

# cota: (b-a)⁵·f4max / (180·n⁴) ≤ tol  →  n ≥ ((b-a)⁵·f4max/(180·tol))^(1/4)
n_teo_b = ((gb - ga)**5 * f4max_b / (180 * tol)) ** 0.25
n_teo_b = int(np.ceil(n_teo_b))
if n_teo_b % 2 != 0:      # Simpson exige n par
    n_teo_b += 1

# verificação experimental
n_exp_b = 2
while abs(simpson13(np.exp, ga, gb, n_exp_b) - exato_b) > tol:
    n_exp_b += 2           # mantém par

cota_teo_b = cota_simpson(f4max_b, ga, gb, n_teo_b)
erro_teo_b = abs(simpson13(np.exp, ga, gb, n_teo_b) - exato_b)
erro_exp_b = abs(simpson13(np.exp, ga, gb, n_exp_b) - exato_b)

print(f"""(b) ∫₀¹ eˣ dx = e−1  — Simpson 1/3  (tolerância = {tol:.0e})

  Cota:  |E| ≤ (b-a)⁵·max|f⁽⁴⁾| / (180·n⁴) ≤ tol
         n  ≥ ((b-a)⁵·e / (180·{tol:.0e}))^(1/4)
         n  ≥ ({(gb-ga)**5 * f4max_b / (180*tol):.4f})^(1/4)
         n  ≥ {((gb-ga)**5*f4max_b/(180*tol))**0.25:.4f}  →  n_teórico = {n_teo_b} (arred. par)

  {'Grandeza':<28} {'Valor':>12}
  {'─'*42}
  {'n teórico (cota)':<28} {n_teo_b:>12d}
  {'Cota garantida p/ n_teo':<28} {cota_teo_b:>12.2e}
  {'Erro real com n_teo':<28} {erro_teo_b:>12.2e}
  {'n experimental (mínimo)':<28} {n_exp_b:>12d}
  {'Erro real com n_exp':<28} {erro_exp_b:>12.2e}
""")

# ══════════════════════════════════════════════════════════════════════════════
# (c) Discussão
# ══════════════════════════════════════════════════════════════════════════════
print(f"""(c) As cotas são conservadoras?

  Trapézios:  n_teórico = {n_teo_a},  n_experimental = {n_exp_a}
              cota superestimou n por fator {n_teo_a/n_exp_a:.1f}×

  Simpson:    n_teórico = {n_teo_b},  n_experimental = {n_exp_b}
              cota superestimou n por fator {n_teo_b/n_exp_b:.1f}×

  Sim — as cotas são conservadoras por dois motivos:

  1. Usam o MÁXIMO global de |f''| ou |f⁽⁴⁾| no intervalo inteiro,
     mas na prática a derivada pode ser bem menor na maior parte do
     domínio (ex.: |sin x| é 1 apenas em x=π/2 e cai a zero nas bordas).

  2. A cota majorante é uma desigualdade: garante que o erro NUNCA
     supera o valor calculado, mas o erro real costuma ser menor.

  Na prática isso é útil: n_teórico é um limite seguro (nunca falha),
  mas o menor n experimental pode ser significativamente menor.
  Para aplicações críticas usa-se n_teórico; para eficiência
  computacional, refina-se adaptivamente até atingir a tolerância.
""")


# ------------------------------------------------------------------------------
# Q2.4 — Convergência: ∫₀^π x² sin x dx
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 2.4 — Convergência")
print("─" * 72)

f     = lambda x: x**2 * np.sin(x)
a, b  = 0.0, np.pi
exato = np.pi**2 - 4          # ≈ 5.8696

ns    = [4, 8, 16, 32]

erros_tr = np.array([abs(trapezios(f, a, b, n) - exato) for n in ns])
erros_si = np.array([abs(simpson13(f, a, b, n) - exato) for n in ns])

# (a) Gráfico log-log
fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(ns, erros_tr, "o-",  color="tomato",    label="Trapézios  O(n⁻²)")
ax.loglog(ns, erros_si, "s-",  color="steelblue", label="Simpson    O(n⁻⁴)")

# retas de referência
ns_ref = np.array([2, 64], dtype=float)
ax.loglog(ns_ref, 0.5  * ns_ref**-2, "r--", linewidth=0.8, label="incl. −2 (ref.)")
ax.loglog(ns_ref, 0.05 * ns_ref**-4, "b--", linewidth=0.8, label="incl. −4 (ref.)")

ax.set_xlabel("n  (subintervalos)")
ax.set_ylabel("Erro absoluto  |E|")
ax.set_title("Q2.4 — Convergência: ∫₀^π x² sin x dx")
ax.legend()
ax.grid(True, which="both", linestyle=":", linewidth=0.5)
plt.tight_layout()
plt.savefig("q24_convergencia.png", dpi=300)
plt.close()
print("\n  Gráfico salvo: q24_convergencia.png")

# (b) Fatores ao dobrar n
print(f"\n(b) Fatores de redução ao dobrar n")
print(f"  {'n→2n':<8}  {'Erro TR':>10}  {'Fator TR':>9}  {'Esp.':>5}"
      f"  {'Erro SI':>10}  {'Fator SI':>9}  {'Esp.':>5}")
print("  " + "─" * 64)
pares = [(0,1),(1,2),(2,3)]
for i, j in pares:
    ftr = erros_tr[i] / erros_tr[j]
    fsi = erros_si[i] / erros_si[j]
    label = f"{ns[i]}→{ns[j]}"
    print(f"  {label:<8}  {erros_tr[i]:>10.2e}  {ftr:>9.2f}  {'4':>5}"
          f"  {erros_si[i]:>10.2e}  {fsi:>9.2f}  {'16':>5}")

# inclinações numéricas via regressão log-log
incl_tr = np.polyfit(np.log(ns), np.log(erros_tr), 1)[0]
incl_si = np.polyfit(np.log(ns), np.log(erros_si), 1)[0]
print(f"\n  Inclinação log-log  Trapézios : {incl_tr:.3f}  (esperado −2)")
print(f"  Inclinação log-log  Simpson   : {incl_si:.3f}  (esperado −4)")

# (c) menor n (par) de Simpson que supera Trapézios com n=100
erro_tr100 = abs(trapezios(f, a, b, 100) - exato)
n_si = 2
while abs(simpson13(f, a, b, n_si) - exato) > erro_tr100:
    n_si += 2

erro_si_n = abs(simpson13(f, a, b, n_si) - exato)

print(f"\n(c) Trapézios com n=100")
print(f"  Erro TR(100)        : {erro_tr100:.2e}   (avaliações: {101})")
print(f"\n  Menor n de Simpson que supera esse erro:")
print(f"  n_Simpson           : {n_si}   (avaliações: {n_si+1})")
print(f"  Erro SI({n_si})         : {erro_si_n:.2e}")
print(f"  Avaliações TR(100)  : 101   |   Avaliações SI({n_si}): {n_si+1}")
print(f"  Simpson precisa de apenas {n_si+1} avaliações vs 101 do Trapézios"
      f" para superar a mesma precisão.")

print(f"""
  Interpretação:

  (a/b) As inclinações log-log confirmam as ordens teóricas:
    Trapézios → incl. ≈ {incl_tr:.1f}  (O(n⁻²))
    Simpson   → incl. ≈ {incl_si:.1f}  (O(n⁻⁴))
  Ao dobrar n, Trapézios divide o erro por ≈4 e Simpson por ≈16,
  exatamente 2² e 2⁴.

  (c) A convergência O(n⁻⁴) de Simpson é tão superior que ele
  consegue superar Trapézios com n=100 usando apenas n={n_si}
  subintervalos — {n_si+1} avaliações contra 101.
  Para atingir um dado erro ε, a relação entre os n necessários é:

    n_SI / n_TR  ≈  (C_TR / C_SI)^(1/4)  ≪  1

  mostrando que Simpson é exponencialmente mais eficiente por
  avaliação de função conforme a precisão exigida aumenta.
""")


# ------------------------------------------------------------------------------
# Q2.5 — Integração de dados experimentais (potência elétrica)
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 2.5 — Integração de dados experimentais")
print("─" * 72)

t_pot = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5])
P_pot = np.array([0.0, 12.4, 22.8, 30.1, 34.2, 35.0, 32.8, 27.5, 20.3, 12.1])
h     = 0.5    # espaçamento uniforme

# (a) Trapézios tabela
E_trap = trapezios_tabela(t_pot, P_pot)

print(f"\n(a) Trapézios tabelados")
print(f"  E = ∫₀⁴·⁵ P(t) dt ≈ {E_trap:.4f} J")

# (b) Simpson com n=9 (ímpar) → Simpson nos 8 primeiros + Trapézio no último
# primeiros 8 subintervalos: t[0..8], P[0..8]  (n=8, par ✓)
E_si8  = simpson13_tabela(t_pot[:9], P_pot[:9])
# último subintervalo: t[8..9]  (Trapézio simples)
E_last = trapezios_tabela(t_pot[8:], P_pot[8:])
E_misto = E_si8 + E_last

print(f"\n(b) Simpson 1/3 + Trapézio (contorno n=9 ímpar)")
print(f"  n=9 subintervalos é ímpar → Simpson exige n par.")
print(f"  Estratégia: Simpson nos primeiros 8 subintervalos (t=0..4),")
print(f"              Trapézio no último subintervalo (t=4.0→4.5).")
print(f"  E_Simpson(t=0→4) = {E_si8:.4f} J")
print(f"  E_Trapézio(t=4→4.5) = {E_last:.4f} J")
print(f"  E_total            = {E_misto:.4f} J")

# (c) Comparação e confiabilidade
diff = abs(E_misto - E_trap)
print(f"\n(c) Comparação entre métodos")
print(f"  {'Método':<25}  {'Energia (J)':>12}")
print(f"  {'─'*40}")
print(f"  {'Trapézios':<25}  {E_trap:>12.4f}")
print(f"  {'Simpson+Trapézio':<25}  {E_misto:>12.4f}")
print(f"  {'Diferença |ΔE|':<25}  {diff:>12.4f} J")

print(f"""
  O resultado misto (Simpson + Trapézio) é mais confiável.
  Simpson tem erro O(h⁴) nos 8 subintervalos onde é aplicado,
  contra O(h²) do Trapézio. A diferença {diff:.4f} J entre os dois
  métodos serve como estimativa prática do erro do Trapézio puro —
  quando dois métodos de ordens diferentes concordam bem, o resultado
  de maior ordem é o mais confiável.
""")

# (d) Incerteza dos dados vs erro numérico
delta_P  = 0.5          # W  — resolução do instrumento
n_trap   = len(t_pot) - 1

# incerteza propagada na regra dos Trapézios:
# E = h/2·[P0 + 2P1 + ... + 2P8 + P9]
# pesos: bordas=1, interior=2  →  soma dos |coef| = 1+2*(n-1)+1 = 2n
pesos_soma = 2 * n_trap               # soma de todos os coeficientes absolutos
delta_E_dados = h / 2 * pesos_soma * delta_P

# erro numérico do Trapézio: estimado pela diferença com Simpson
erro_numerico = diff

print(f"(d) Incerteza dos dados vs erro numérico")
print(f"  Erro de medição  δP = ±{delta_P} W")
print(f"  Propagação na regra dos Trapézios:")
print(f"    δE = h/2 · Σ|coef| · δP = {h}/2 · {pesos_soma} · {delta_P} = ±{delta_E_dados:.2f} J")
print(f"  Erro numérico (|TR − SI|) ≈ {erro_numerico:.4f} J")
print(f"""
  Comparação:
    Incerteza dos dados  : ±{delta_E_dados:.2f} J
    Erro numérico        :  {erro_numerico:.4f} J
    Precisão exigida     : ±0.10 J

  O erro numérico ({erro_numerico:.4f} J) é muito menor que a incerteza
  dos dados (±{delta_E_dados:.2f} J). A precisão é limitada pelo erro de
  medição do instrumento, não pelo método numérico.

  Com dados de ±{delta_P} W, qualquer método (Trapézios ou Simpson)
  entrega resultado preciso o suficiente numericamente — mas a
  incerteza final de ±{delta_E_dados:.1f} J está bem acima da tolerância
  de ±0.1 J. Para atingir ±0.1 J seria necessário um instrumento
  com resolução δP ≤ {0.1 / (h/2 * pesos_soma):.3f} W, não um método melhor.
""")

# =============================================================================
# SEÇÃO 3 — Quadratura Gaussiana e Comparação de Métodos
# =============================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 3 — Quadratura Gaussiana e Comparação de Métodos")
print("═" * 72)


# ------------------------------------------------------------------------------
# Q3.1 — Eficiência da Gauss-Legendre
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 3.1 — Eficiência da Gauss-Legendre")
print("─" * 72)

f     = lambda x: 1 / x
a, b  = 1.0, 2.0
exato = np.log(2)          # ≈ 0.693147

ns_nc    = [2, 4, 8, 16, 32]
ns_gauss = [2, 3, 4, 5, 6]

print(f"\n∫₁² 1/x dx = ln 2 ≈ {exato:.6f}")
print("\nComparação Newton-Cotes vs. Gauss-Legendre:\n")
tabela_comparativa(f, a, b, exato, ns_nc, ns_gauss)

# (a) GL n=2 (2 avaliações) vs Simpson n=4 (5 avaliações)
GL_2     = gauss_legendre(f, a, b, 2)
SI_4     = simpson13(f, a, b, 4)
erro_GL2 = abs(GL_2 - exato)
erro_SI4 = abs(SI_4 - exato)

print(f"\n(a) Gauss-Legendre n=2 (2 aval.) vs Simpson n=4 (5 aval.)")
print(f"  {'Método':<25} {'Avaliações':>10}  {'Resultado':>14}  {'Erro':>12}")
print("  " + "─" * 66)
print(f"  {'Gauss-Legendre n=2':<25} {2:>10d}  {GL_2:>14.8f}  {erro_GL2:>12.2e}")
print(f"  {'Simpson n=4':<25} {5:>10d}  {SI_4:>14.8f}  {erro_SI4:>12.2e}")
print(f"""
  Gauss-Legendre com apenas 2 avaliações de f é {'mais' if erro_GL2 < erro_SI4 else 'menos'} preciso
  que Simpson com 5 avaliações (erro {erro_GL2:.2e} vs {erro_SI4:.2e}).
  GL com n=2 é exato até grau 2n−1 = 3, o mesmo grau de exatidão do
  Simpson simples de 3 pontos — mas o Simpson usado aqui é composto
  (n=4, ou seja, 2 painéis com h=0,25 cada), não um único painel.
  Cada painel do Simpson composto já é exato até grau 3 *localmente*,
  então refinar h reduz o erro adicionalmente, enquanto GL n=2 aplica
  um único ajuste de grau 3 sobre todo o intervalo [1,2] — sem esse
  refinamento local. Por isso, mesmo com menos avaliações "no papel",
  GL n=2 perde para o Simpson composto com h menor.
""")

# (b) menor n de GL que supera Simpson n=32 (33 avaliações)
erro_SI32 = abs(simpson13(f, a, b, 32) - exato)
n_gl = 2
while abs(gauss_legendre(f, a, b, n_gl) - exato) > erro_SI32:
    n_gl += 1
erro_GLn = abs(gauss_legendre(f, a, b, n_gl) - exato)

print(f"(b) Menor n de Gauss-Legendre que supera Simpson n=32 (33 aval.)")
print(f"  Erro Simpson(n=32)         : {erro_SI32:.2e}   (33 avaliações)")
print(f"  Menor n_GL que supera      : {n_gl}   (erro = {erro_GLn:.2e}, {n_gl} avaliações)")
print(f"  Gauss-Legendre precisa de apenas {n_gl} avaliações contra 33 do Simpson"
      f" para atingir precisão igual ou melhor.")

print(f"""
(c) Por que Gauss-Legendre converge mais rápido?

  Newton-Cotes com n subintervalos usa n+1 nós fixos e igualmente
  espaçados; Simpson (grau 2 por par de subintervalos) é exato até
  grau polinomial 3 independentemente de n, e Trapézios até grau 1.

  Gauss-Legendre com n pontos tem 2n graus de liberdade (n posições
  de nós + n pesos), otimizados para maximizar o grau de exatidão:
  é exato para todo polinômio de grau ≤ 2n−1. Ou seja, GL "compra"
  exatidão polinomial adicional ao permitir que os nós não sejam
  igualmente espaçados — eles se concentram como as raízes dos
  polinômios de Legendre, dando mais peso às regiões relevantes
  para a integração. Por isso, para funções suaves, GL converge
  muito mais rápido por avaliação de função do que qualquer regra
  de Newton-Cotes de ordem fixa.
""")


# ------------------------------------------------------------------------------
# Q3.2 — ∫₀¹ e^(-x²) dx (sem primitiva elementar)
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 3.2 — ∫₀¹ e^(-x²) dx")
print("─" * 72)

f2     = lambda x: np.exp(-x**2)
a2, b2 = 0.0, 1.0
exato2 = erf(1.0) * np.sqrt(np.pi) / 2        # ≈ 0.746824

ns2 = [2, 4, 8, 16, 32]

print(f"\n∫₀¹ e^(-x²) dx ≈ {exato2:.6f}  (referência: erf(1)·√π/2)")

# (a) Trapézios, Simpson e GL para cada n
resultados_tr = [trapezios(f2, a2, b2, n) for n in ns2]
resultados_si = [simpson13(f2, a2, b2, n) for n in ns2]
resultados_gl = [gauss_legendre(f2, a2, b2, n) for n in ns2]

erros_tr2 = np.array([abs(r - exato2) for r in resultados_tr])
erros_si2 = np.array([abs(r - exato2) for r in resultados_si])
erros_gl2 = np.array([abs(r - exato2) for r in resultados_gl])

aval_tr2 = np.array([n + 1 for n in ns2])
aval_si2 = np.array([n + 1 for n in ns2])
aval_gl2 = np.array(ns2)

print(f"\n(a) Trapézios, Simpson e Gauss-Legendre para n = {ns2}")
print(f"  {'n':>4}  {'Trapézios':>14}  {'Erro TR':>12}  {'Simpson':>14}  {'Erro SI':>12}  {'Gauss-Leg.':>14}  {'Erro GL':>12}")
print("  " + "─" * 96)
for i, n in enumerate(ns2):
    print(f"  {n:>4}  {resultados_tr[i]:>14.8f}  {erros_tr2[i]:>12.2e}  "
          f"{resultados_si[i]:>14.8f}  {erros_si2[i]:>12.2e}  "
          f"{resultados_gl[i]:>14.8f}  {erros_gl2[i]:>12.2e}")

# (b) Gráfico erro vs avaliações (log-log)
fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(aval_tr2, erros_tr2, "o-", color="tomato",    label="Trapézios")
ax.loglog(aval_si2, erros_si2, "s-", color="steelblue", label="Simpson 1/3")
ax.loglog(aval_gl2, erros_gl2, "^-", color="seagreen",  label="Gauss-Legendre")
ax.set_xlabel("Avaliações de f")
ax.set_ylabel("Erro absoluto  |E|")
ax.set_title("Q3.2 — Precisão por custo: ∫₀¹ e^(-x²) dx")
ax.legend()
ax.grid(True, which="both", linestyle=":", linewidth=0.5)
plt.tight_layout()
plt.savefig("q32_precisao_custo.png", dpi=300)
plt.close()
print("\n(b) Gráfico salvo: q32_precisao_custo.png")
print("  Gauss-Legendre apresenta a melhor curva precisão-por-custo:")
print("  para o mesmo número de avaliações de f, seu erro é ordens de")
print("  grandeza menor que o de Trapézios e Simpson.")

# (c) menor número de avaliações para erro < 1e-8
tol2 = 1e-8

n_tr = 2
while abs(trapezios(f2, a2, b2, n_tr) - exato2) > tol2:
    n_tr += 1
n_si = 2
while abs(simpson13(f2, a2, b2, n_si) - exato2) > tol2:
    n_si += 2
n_gl2 = 1
while abs(gauss_legendre(f2, a2, b2, n_gl2) - exato2) > tol2:
    n_gl2 += 1

print(f"\n(c) Menor número de avaliações para erro < {tol2:.0e}")
print(f"  {'Método':<20} {'n':>6}  {'Avaliações':>10}  {'Erro':>12}")
print("  " + "─" * 54)
print(f"  {'Trapézios':<20} {n_tr:>6d}  {n_tr+1:>10d}  {abs(trapezios(f2,a2,b2,n_tr)-exato2):>12.2e}")
print(f"  {'Simpson 1/3':<20} {n_si:>6d}  {n_si+1:>10d}  {abs(simpson13(f2,a2,b2,n_si)-exato2):>12.2e}")
print(f"  {'Gauss-Legendre':<20} {n_gl2:>6d}  {n_gl2:>10d}  {abs(gauss_legendre(f2,a2,b2,n_gl2)-exato2):>12.2e}")
print(f"\n  Gauss-Legendre atinge erro < {tol2:.0e} com apenas {n_gl2} avaliações,"
      f" muito menos que Trapézios ({n_tr+1}) e Simpson ({n_si+1}).")

print(f"""
(d) Por que o gráfico de Gauss-Legendre não é uma reta em log-log?

  Trapézios e Simpson têm erro que decai como potência de n
  (O(n⁻²) e O(n⁻⁴) respectivamente), o que produz uma reta em
  escala log-log: log|E| = log(C) − p·log(n), com inclinação
  constante −p.

  Gauss-Legendre, para funções analíticas (como e^(−x²), que é
  inteira), converge geometricamente/exponencialmente: o erro
  decai como O(ρ⁻ⁿ) para algum ρ > 1. Nesse caso log|E| é linear
  em n (não em log n), e portanto a curva em escala log-log é
  côncava — cai muito mais rápido que qualquer lei de potência,
  até que o erro atinja o nível de arredondamento de máquina.
""")


# ------------------------------------------------------------------------------
# Q3.3 — Função não-suave: f(x)=|x-0,5|
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 3.3 — Função não-suave")
print("─" * 72)

f3     = lambda x: np.abs(x - 0.5)
a3, b3 = 0.0, 1.0
exato3 = 0.25

ns3 = [2, 4, 8, 16]

erros_tr3 = np.array([abs(trapezios(f3, a3, b3, n) - exato3) for n in ns3])
erros_si3 = np.array([abs(simpson13(f3, a3, b3, n) - exato3) for n in ns3])
erros_gl3 = np.array([abs(gauss_legendre(f3, a3, b3, n) - exato3) for n in ns3])

print(f"\n(a) ∫₀¹ |x − 0,5| dx = 0,25  — erro de cada método")
print(f"  {'n':>4}  {'Erro Trapézios':>16}  {'Erro Simpson':>14}  {'Erro Gauss-Leg.':>16}")
print("  " + "─" * 58)
for i, n in enumerate(ns3):
    print(f"  {n:>4}  {erros_tr3[i]:>16.2e}  {erros_si3[i]:>14.2e}  {erros_gl3[i]:>16.2e}")

# (b) identificar o método mais rápido comparando o erro no maior n
erro_final = {"Trapézios": erros_tr3[-1], "Simpson 1/3": erros_si3[-1], "Gauss-Legendre": erros_gl3[-1]}
melhor = min(erro_final, key=erro_final.get)

print(f"\n(b) Com n = {ns3[-1]}, o menor erro é de {melhor} ({erro_final[melhor]:.2e}).")
print(f"  {'Método':<18} {'Erro (n=' + str(ns3[-1]) + ')':>14}")
print("  " + "─" * 34)
for nome, e in erro_final.items():
    print(f"  {nome:<18} {e:>14.2e}")
print(f"""
  Isso contradiz a tendência observada em Q3.1 e Q3.2, onde
  Gauss-Legendre era claramente superior. Aqui, para uma função
  com derivada descontínua em x=0,5, a vantagem de GL desaparece
  (ou se inverte) porque sua convergência espectral depende de
  suavidade (analiticidade) da função — o que não se verifica em
  |x − 0,5|, que é contínua, mas não diferenciável no ponto x=0,5.
""")

print(f"""(c) Por que a taxa de convergência de Gauss-Legendre cai?

  A convergência exponencial de Gauss-Legendre depende de f(x) ser
  analítica (ou suave o suficiente) em uma região do plano complexo
  ao redor do intervalo de integração. A função |x − 0,5| tem uma
  quina (derivada descontínua) em x=0,5: é contínua, mas não é
  diferenciável ali, e portanto não é analítica.

  Os nós de Gauss-Legendre não coincidem, em geral, com o ponto de
  quina — diferente de Trapézios, que é exato para qualquer n par
  neste problema simétrico (cada nó de Trapézios cai sobre x=0,5,
  ponto onde a própria função, linear por partes, não tem erro de
  interpolação linear). Simpson só zera o erro quando n é múltiplo
  de 4: com n=2, x=0,5 é o nó central de um único painel, mas o
  ajuste quadrático desse painel ainda "sente" a quina e erra
  (8,33e-02); com n=4,8,16, x=0,5 cai exatamente sobre uma fronteira
  entre painéis, isolando a quina fora de qualquer ajuste quadrático.
  Já Gauss-Legendre "vê" a função não-suave em qualquer n (seus nós
  nunca coincidem com x=0,5), e sua convergência degrada para uma
  taxa algébrica (tipicamente O(n⁻²) a O(n⁻³)), perdendo a vantagem
  espectral que tinha para e^(−x²).
""")

print(f"""(d) O que este experimento ensina sobre a escolha do método?

  A superioridade de Gauss-Legendre não é universal — ela depende
  da regularidade (suavidade/analiticidade) do integrando. Para
  funções suaves e analíticas (Q3.1, Q3.2), GL é imbatível em
  eficiência (erro por avaliação de f). Para funções com quinas,
  descontinuidades ou singularidades, seu desempenho se aproxima
  — ou pode até ficar atrás — do de Newton-Cotes.

  Na prática: antes de escolher Gauss-Legendre por sua alta ordem
  teórica, é preciso verificar a suavidade do integrando. Se houver
  pontos não-suaves conhecidos, uma estratégia melhor é dividir o
  intervalo nesses pontos e aplicar GL (ou Simpson) separadamente
  em cada subintervalo suave — restaurando a convergência rápida.
""")

# =============================================================================
# SEÇÃO 4 — Análise Comparativa Global
# =============================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 4 — Análise Comparativa Global")
print("═" * 72)


# ------------------------------------------------------------------------------
# Q4.1 — Tabela de síntese
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 4.1 — Tabela de síntese")
print("─" * 72)

sintese = [
    ("Erro global",
     f"O(h²) ≈ O(n⁻²)  [incl.={incl_tr:.1f}]",
     f"O(h⁴) ≈ O(n⁻⁴)  [incl.={incl_si:.1f}]",
     "O(ρ⁻ⁿ)  (exponencial p/ f analítica)",
     "O(h²)"),
    ("Avals. de f (geral)",
     "n + 1",
     "n + 1",
     "n  (nós ótimos)",
     "2 por ponto (borda: 3)"),
    ("Exato para grau",
     "1  (retas)",
     "3  (cúbicas)",
     "2n − 1",
     "—  (aprox. de derivada, não de integral)"),
    ("Requer n especial?",
     "Não",
     "Sim — n par",
     "Não  (qualquer n ≥ 1)",
     "Não"),
    ("Funciona com tabela?",
     "Sim — trapezios_tabela",
     "Sim — simpson13_tabela",
     "Não  (exige f(x) em nós\nnão-equiespaçados)",
     "Sim — derivada_tabela"),
    ("Melhor cenário",
     "Dados tabelados/ruidosos,\nintegrando qualquer forma",
     "Funções suaves, dados\ntabelados com n par",
     "Funções analíticas suaves,\npoucas avaliações de f",
     "Funções suaves, derivada\nde dados experimentais"),
    ("Pior cenário",
     "Funções muito suaves\n(convergência lenta)",
     "Integrando não-suave\n(perde O(h⁴), Q2.4/Q3.3)",
     "Integrando com quinas/\ndescontinuidades (Q3.3)",
     "Dados muito ruidosos com\nh pequeno (Q1.4e)"),
]

col_labels = ["Aspecto", "Trapézios", "Simpson 1/3", "Gauss-Legendre", "Dif. Central"]
larguras   = [22, 30, 30, 36, 30]

print()
cab = "  " + "".join(f"{c:<{w}}" for c, w in zip(col_labels, larguras))
print(cab)
print("  " + "─" * (sum(larguras)))
for linha in sintese:
    sub_linhas = [str(v).split("\n") for v in linha]
    n_sub = max(len(s) for s in sub_linhas)
    for i in range(n_sub):
        partes = []
        for s, w in zip(sub_linhas, larguras):
            texto = s[i] if i < len(s) else ""
            partes.append(f"{texto:<{w}}")
        print("  " + "".join(partes))
    print()

print("""
  Leitura da síntese:

  Não existe um método "melhor" em absoluto — cada um domina em um
  regime diferente. Trapézios é o mais robusto (funciona com
  qualquer n, qualquer dado tabelado, e degrada suavemente com
  ruído), mas é o mais lento a convergir (O(n⁻²)). Simpson troca
  simplicidade por uma ordem a mais (O(n⁻⁴)) ao custo de exigir n
  par e de assumir suavidade local (ajuste parabólico). Gauss-
  Legendre é imbatível em avaliações de f para integrandos
  analíticos suaves (Q3.1, Q3.2), mas não pode ser aplicado
  diretamente a dados tabelados e perde sua vantagem em funções
  não-suaves (Q3.3). Diferenças finitas centrais seguem a mesma
  lógica de Trapézios/Simpson (O(h²) por cancelamento de Taylor),
  mas têm um problema adicional exclusivo da diferenciação: o
  conflito truncamento × arredondamento (Q1.3), que não existe na
  integração porque a soma de vários f(xi) não amplifica o erro de
  arredondamento da mesma forma que a subtração de valores próximos.
""")


# ------------------------------------------------------------------------------
# Q4.2 — Tomada de decisão com 201 pontos
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 4.2 — Tomada de decisão")
print("─" * 72)

n_pontos = 201
n_sub    = n_pontos - 1          # 200 subintervalos
t_ini, t_fim = 0.0, 100.0
h_sinal  = (t_fim - t_ini) / n_sub

print(f"\nCenário: sinal elétrico com {n_pontos} pontos amostrados a cada 0,5 s,")
print(f"         em [{t_ini:.0f}, {t_fim:.0f}] s  →  n = {n_sub} subintervalos, h = {h_sinal} s")

print(f"""
(a) Viabilidade de cada proposta

  Estudante A — Trapézios com os 201 pontos:
    VIÁVEL. trapezios_tabela (ou trapezios com n={n_sub}) usa
    exatamente os pontos disponíveis, sem exigir avaliações de f
    fora da amostragem. Nenhuma restrição sobre n.

  Estudante B — Simpson 1/3 com os 200 subintervalos:
    VIÁVEL. n={n_sub} é par, condição exigida por simpson13 /
    simpson13_tabela. Usa também todos os pontos disponíveis, sem
    nenhuma avaliação extra de f.

  Estudante C — Gauss-Legendre com n=5 no intervalo todo:
    TEM PROBLEMA CONCEITUAL. gauss_legendre(f, a, b, n) precisa
    avaliar f(x) nos nós de Gauss-Legendre, que são raízes de um
    polinômio de Legendre transformadas para [a,b] — pontos que,
    em geral, NÃO coincidem com os instantes t = 0, 0.5, 1.0, ...
    amostrados. Como o sinal é conhecido apenas nesses 201 pontos
    tabelados (não existe uma expressão fechada f(t) para avaliar
    em qualquer t), o Estudante C não tem como calcular f nos nós
    de Gauss sem antes interpolar os dados — o que introduziria uma
    fonte de erro adicional não contemplada na proposta.
""")

# (b) Recomendação quantitativa
# Ilustração de escala do erro: cotas de erro com f2max=f4max=1 (unidade
# de referência) apenas para comparar como a ordem de cada regra escala
# com o mesmo h — não são cotas reais do sinal, que é desconhecido.
cota_tr_ref = cota_trapezio(1.0, t_ini, t_fim, n_sub)
cota_si_ref = cota_simpson(1.0, t_ini, t_fim, n_sub)

print(f"(b) Recomendação para dados experimentais")
print(f"  Com h = {h_sinal} s fixo pela taxa de amostragem (não pode ser refinado):")
print(f"    h²  = {h_sinal**2:.4f}")
print(f"    h⁴  = {h_sinal**4:.4f}")
print(f"  Cota Trapézios (ref., f''max=1)   : {cota_tr_ref:.4e}")
print(f"  Cota Simpson   (ref., f⁽⁴⁾max=1)  : {cota_si_ref:.4e}")
print(f"  Razão cota_TR / cota_SI            : {cota_tr_ref/cota_si_ref:.1f}×")
print(f"""
  Recomendo Simpson 1/3 (Estudante B):

  - Usa TODOS os 201 pontos disponíveis, exatamente como Trapézios
    (nenhum dado é descartado e nenhuma avaliação extra é feita).
  - Para o mesmo h = {h_sinal} s, sua cota de erro escala com h⁴ em vez
    de h², de modo que — mesmo sem conhecer f''/f⁽⁴⁾ do sinal real —
    a razão estrutural entre as cotas já favorece Simpson por um
    fator de ordem {cota_tr_ref/cota_si_ref:.0f}× (Q2.2, Q2.4 confirmam esse
    comportamento empiricamente para outras funções suaves).
  - Gauss-Legendre, apesar de mais eficiente por avaliação de f para
    integrandos analíticos (Q3.1), não é aplicável aqui sem
    interpolação — o que o tira de consideração para dados
    puramente tabelados como este.
""")

# (c) Sinal com descontinuidades
print(f"""(c) Se o sinal tivesse descontinuidades (chaveamento elétrico)?

  Sim, a recomendação mudaria. Simpson 1/3 ajusta uma parábola a
  cada par de subintervalos (Q2.4, Q3.3); perto de uma
  descontinuidade esse ajuste é inválido — a parábola tenta suavizar
  um salto, gerando oscilações locais (fenômeno análogo ao de Gibbs)
  que podem até superar o erro de Trapézios, cancelando a vantagem
  teórica de O(h⁴).

  Nessa situação a estratégia mais robusta é:
    1. Localizar os instantes de chaveamento (onde f(t) salta);
    2. Dividir o intervalo de integração exatamente nesses pontos,
       tratando cada trecho suave separadamente;
    3. Aplicar Simpson (ou Trapézios) dentro de cada trecho suave, e
       Trapézios especificamente nos subintervalos que contêm a
       descontinuidade (mesma lógica usada em Q2.5b para n ímpar).

  Esse comportamento é consistente com o observado em Q3.3 para
  Gauss-Legendre: métodos de alta ordem (Simpson, GL) dependem de
  suavidade local para entregar sua taxa de convergência teórica;
  na presença de quinas ou saltos, a robustez de Trapézios (ou de
  uma versão segmentada dos métodos de ordem maior) volta a ser a
  escolha mais segura.
""")


# =============================================================================
# SEÇÃO 5 — Projeto Integrador: Cálculo Variacional e Física
# =============================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 5 — Projeto Integrador")
print("═" * 72)


# ------------------------------------------------------------------------------
# Q5.1 — Comprimento de curva: f(x)=x² em [0,2]
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 5.1 — Comprimento de curva")
print("─" * 72)

a_curva, b_curva = 0.0, 2.0
u_b     = 2 * b_curva
L_exato = 0.25 * (u_b * np.sqrt(1 + u_b**2) + np.log(u_b + np.sqrt(1 + u_b**2)))

print(f"\n  L = ∫₀² √(1+4x²) dx   (f'(x) = 2x)")
print(f"  L_exato = {L_exato:.6f}")

# (a) Derivação analítica: f'(x) = 2x
integrando_analitico = lambda x: np.sqrt(1 + (2*x)**2)
n_curva  = 10
L_an     = simpson13(integrando_analitico, a_curva, b_curva, n_curva)
erro_an  = abs(L_an - L_exato)

print(f"\n(a) Comprimento com Simpson 1/3 (n={n_curva}), usando f'(x)=2x analítico")
print(f"  L_analítico = {L_an:.8f}")
print(f"  Erro        = {erro_an:.2e}")

# (b) Derivação numérica: usar apenas os valores de f na malha
x_curva  = np.linspace(a_curva, b_curva, n_curva + 1)
f_curva  = x_curva**2
fp_num   = derivada_tabela(x_curva, f_curva)      # f'(x_k) via diferenças finitas
integrando_num = np.sqrt(1 + fp_num**2)
L_num    = simpson13_tabela(x_curva, integrando_num)
erro_num = abs(L_num - L_exato)

print(f"\n(b) Comprimento usando f'(x_k) estimado por derivada_tabela")
print(f"  {'x_k':>6}  {'f(x_k)':>10}  {'f_analit':>12}  {'f_numer':>12}")
print("  " + "─" * 46)
for xi, fi, fpi in zip(x_curva, f_curva, fp_num):
    print(f"  {xi:>6.2f}  {fi:>10.4f}  {2*xi:>12.4f}  {fpi:>12.4f}")
print(f"\n  L_numérico  = {L_num:.8f}")
print(f"  Erro        = {erro_num:.2e}")

# (c) Comparação
print(f"\n(c) Comparação entre (a) e (b)")
print(f"  Erro com f' analítica : {erro_an:.2e}")
print(f"  Erro com f' numérica  : {erro_num:.2e}")
print(f"  Diferença |L_num - L_an| = {abs(L_num - L_an):.2e}")
print(f"""
  Como f(x) = x² é um polinômio de grau 2, tanto a diferença central
  quanto as fórmulas de 3 pontos usadas nas bordas por derivada_tabela
  são EXATAS para f' = 2x (o termo de erro dessas fórmulas depende de
  f''' ou derivadas superiores, que são identicamente nulas para uma
  parábola). Por isso a diferenciação numérica não introduz erro
  adicional aqui além do arredondamento de máquina — os dois
  comprimentos coincidem até a ordem de 1e-14, e o erro total
  observado é devido inteiramente à integração por Simpson 1/3,
  não à derivação.
""")

# (d) Convergência com n=10,20,40,80
ns_curva = [10, 20, 40, 80]
erros_an  = []
erros_num = []
for n in ns_curva:
    L_a = simpson13(integrando_analitico, a_curva, b_curva, n)
    xi  = np.linspace(a_curva, b_curva, n + 1)
    fpi = derivada_tabela(xi, xi**2)
    L_n = simpson13_tabela(xi, np.sqrt(1 + fpi**2))
    erros_an.append(abs(L_a - L_exato))
    erros_num.append(abs(L_n - L_exato))

print(f"\n(d) Convergência com n = {ns_curva}")
print(f"  {'n':>4}  {'Erro f_analit':>16}  {'Erro f_numer':>16}")
print("  " + "─" * 40)
for n, ea, en in zip(ns_curva, erros_an, erros_num):
    print(f"  {n:>4}  {ea:>16.2e}  {en:>16.2e}")

# fatores de redução par a par
print(f"\n  Fatores de redução ao dobrar n")
print(f"  {'n→2n':>8}  {'Fator':>8}  {'Esperado O(h⁴)':>16}")
print("  " + "─" * 36)
fatores = []
for i in range(len(ns_curva) - 1):
    fator = erros_an[i] / erros_an[i+1]
    fatores.append(fator)
    print(f"  {ns_curva[i]}→{ns_curva[i+1]:<4}  {fator:>8.2f}  {'16':>16}")

# inclinação log-log: todos os pontos vs. apenas a região assintótica (exclui n=10)
incl_todos     = np.polyfit(np.log(ns_curva), np.log(erros_an), 1)[0]
incl_assintota = np.polyfit(np.log(ns_curva[1:]), np.log(erros_an[1:]), 1)[0]

fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(ns_curva, erros_an,  "o-", color="steelblue", label="f' analítica")
ax.loglog(ns_curva, erros_num, "s--", color="tomato",   label="f' numérica (derivada_tabela)")
ax.set_xlabel("n  (subintervalos)")
ax.set_ylabel("Erro absoluto  |E|")
ax.set_title("Q5.1 — Convergência do comprimento de arco")
ax.legend()
ax.grid(True, which="both", linestyle=":", linewidth=0.5)
plt.tight_layout()
plt.savefig("q51_convergencia.png", dpi=300)
plt.close()
print(f"\n  Gráfico salvo: q51_convergencia.png")
print(f"  Inclinação log-log (todos os pontos)       : {incl_todos:.2f}")
print(f"  Inclinação log-log (região assintótica)     : {incl_assintota:.2f}  (esperado −4)")

print(f"""
  As duas curvas praticamente se sobrepõem: como discutido em (c), a
  diferenciação numérica não acrescenta erro para f(x)=x² — o gargalo
  de precisão é inteiramente a integração por Simpson 1/3.

  O fator de redução n=10→20 ({fatores[0]:.0f}×) é bem maior que os 16×
  esperados para O(h⁴): com h=0.2 (n=10) o erro ainda carrega
  contribuição de termos de ordem superior (h⁶, h⁸, ...) da expansão
  do erro de Simpson, que ainda não desapareceram — a malha não é fina
  o bastante para a assíntota O(h⁴) dominar sozinha. Já os fatores
  n=20→40 ({fatores[1]:.1f}×) e n=40→80 ({fatores[2]:.1f}×) ficam bem
  próximos de 16×, confirmando que a partir de h≈0.1 (n=20) a
  convergência já segue fielmente a ordem teórica.

  Por isso a inclinação de regressão log-log usando todos os 4 pontos
  ({incl_todos:.2f}) fica distorcida pelo ponto pré-assintótico n=10;
  calculada apenas na região assintótica (n=20,40,80), a inclinação
  ({incl_assintota:.2f}) confirma com precisão a ordem O(h⁴) de Simpson.
""")

# ------------------------------------------------------------------------------
# Q5.2 — Trabalho de força variável
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 5.2 — Trabalho de força variável")
print("─" * 72)

x_forca = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0])
F_forca = np.array([0, 8, 15, 20, 24, 26, 27, 26, 22, 17, 11, 5, 0], dtype=float)

# (a) Trabalho por Trapézios e Simpson 1/3
W_trap = trapezios_tabela(x_forca, F_forca)
W_simp = simpson13_tabela(x_forca, F_forca)   # n = 12 (par) ✓

print(f"\n(a) W = ∫₀⁶ F(x) dx   (n = {len(F_forca)-1} subintervalos, par)")
print(f"  {'Método':<15}  {'W (J)':>10}")
print("  " + "─" * 28)
print(f"  {'Trapézios':<15}  {W_trap:>10.4f}")
print(f"  {'Simpson 1/3':<15}  {W_simp:>10.4f}")
print(f"  Diferença |ΔW| = {abs(W_simp - W_trap):.4f} J")

# (b) Ponto de força máxima via F'(x) ≈ 0
Fprime = derivada_tabela(x_forca, F_forca)

print(f"\n(b) Derivada F'(x) e localização do máximo")
print(f"  {'x (m)':>6}  {'F (N)':>7}  {'F_linha (N/m)':>14}")
print("  " + "─" * 32)
for xi, Fi, Fpi in zip(x_forca, F_forca, Fprime):
    print(f"  {xi:>6.1f}  {Fi:>7.1f}  {Fpi:>14.3f}")

idx_max = int(np.argmax(F_forca))
print(f"\n  F'(x) passa de positivo para negativo exatamente em x = {x_forca[idx_max]:.1f} m,")
print(f"  onde F'({x_forca[idx_max]:.1f}) = {Fprime[idx_max]:.4f} ≈ 0  → máximo da força "
      f"(F = {F_forca[idx_max]:.1f} N)")

# (c) Onde a força cresce/decresce mais rápido
idx_cresce   = int(np.argmax(Fprime))
idx_decresce = int(np.argmin(Fprime))
print(f"\n(c) Taxas de variação extremas")
print(f"  Crescimento mais rápido  : x = {x_forca[idx_cresce]:.1f} m,  F' = {Fprime[idx_cresce]:>7.3f} N/m")
print(f"  Decrescimento mais rápido: x = {x_forca[idx_decresce]:.1f} m,  F' = {Fprime[idx_decresce]:>7.3f} N/m")
print(f"""
  A força cresce mais rapidamente logo no início do percurso
  (|F'| ≈ {abs(Fprime[idx_cresce]):.1f} N/m em x = {x_forca[idx_cresce]:.1f} m) do que decresce
  perto do final (|F'| ≈ {abs(Fprime[idx_decresce]):.1f} N/m em x = {x_forca[idx_decresce]:.1f} m).
  Isso indica uma variação inicial mais brusca que a desaceleração
  no fim do trilho.
""")

# (d) Velocidade final: W = ΔKE = ½mv²  (parte do repouso)
m_obj  = 2.0
v_trap = np.sqrt(2 * W_trap / m_obj)
v_simp = np.sqrt(2 * W_simp / m_obj)

print(f"(d) Velocidade final (m = {m_obj} kg, parte do repouso)")
print(f"  v = √(2W/m)")
print(f"  Usando W_Trapézios = {W_trap:.4f} J  →  v = {v_trap:.4f} m/s")
print(f"  Usando W_Simpson   = {W_simp:.4f} J  →  v = {v_simp:.4f} m/s")
print(f"  Diferença |Δv| = {abs(v_simp - v_trap):.4f} m/s")


# ------------------------------------------------------------------------------
# Q5.3 — Distribuição Normal
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 5.3 — Distribuição Normal")
print("─" * 72)

phi_integrando = lambda t: np.exp(-t**2 / 2) / np.sqrt(2 * np.pi)
lim_inf = -6.0

x_phi   = [1.96, 2.58, 3.00]
tab_phi = [0.9750, 0.9951, 0.9987]

# (a) Simpson 1/3 com n=100
print(f"\n(a) Φ(x) por Simpson 1/3 (n=100), truncando em [-6, x]")
print(f"  {'x':>6}  {'Φ_Simpson':>12}  {'Φ_tabelado':>12}  {'Erro':>10}")
print("  " + "─" * 46)
Phi_simpson = {}
for x, tab in zip(x_phi, tab_phi):
    S = simpson13(phi_integrando, lim_inf, x, 100)
    Phi_simpson[x] = S
    print(f"  {x:>6.2f}  {S:>12.6f}  {tab:>12.4f}  {abs(S - tab):>10.2e}")

# (b) Gauss-Legendre com n=5,10,20
print(f"\n(b) Φ(x) por Gauss-Legendre  (n = 5, 10, 20)")
print(f"  {'x':>6}  {'n':>4}  {'Φ_GL':>12}  {'Erro':>10}")
print("  " + "─" * 40)
for x, tab in zip(x_phi, tab_phi):
    for n in (5, 10, 20):
        G = gauss_legendre(phi_integrando, lim_inf, x, n)
        print(f"  {x:>6.2f}  {n:>4}  {G:>12.6f}  {abs(G - tab):>10.2e}")

print(f"\n  Comparação com Simpson (n=100, 101 avaliações):")
for x, tab in zip(x_phi, tab_phi):
    erro_simp = abs(Phi_simpson[x] - tab)
    n_gl = 2
    while abs(gauss_legendre(phi_integrando, lim_inf, x, n_gl) - tab) > erro_simp:
        n_gl += 1
        if n_gl > 40:
            break
    print(f"  x={x:.2f}: GL supera Simpson(n=100) a partir de n = {n_gl}  "
          f"({n_gl} avaliações vs 101)")

# (c) Truncamento em -6
cauda = phi_integrando(-6.0)
print(f"\n(c) Cauda da distribuição em t=-6")
print(f"  f(-6) = {cauda:.3e}   (densidade praticamente nula)")
print(f"""
  A cauda para t < -6 contribui com densidade da ordem de {cauda:.1e},
  bem abaixo de qualquer tolerância numérica razoável. Por isso
  truncar em -6 (em vez de -∞) introduz um erro desprezível, muito
  menor que os erros de truncamento de Simpson ou Gauss-Legendre já
  observados acima.
""")

# (d) Interpolação inversa para z_0.025
x_grid   = np.linspace(1.80, 2.10, 7)
phi_grid = np.array([simpson13(phi_integrando, lim_inf, x, 100) for x in x_grid])
z_0025   = np.interp(0.975, phi_grid, x_grid)

print(f"(d) Interpolação inversa para z_0,025  (Φ(z) = 0,975)")
print(f"  {'x':>6}  {'Φ(x)':>10}")
print("  " + "─" * 18)
for xi, phii in zip(x_grid, phi_grid):
    print(f"  {xi:>6.3f}  {phii:>10.6f}")
print(f"\n  z_0,025 estimado (interpolação linear inversa) = {z_0025:.4f}")
print(f"  Valor exato de referência                       = 1.9600")
print(f"  Erro                                             = {abs(z_0025-1.96):.2e}")

# =============================================================================
# SEÇÃO 6 — Desafio (Opcional — Pontuação Extra)
# =============================================================================

print("\n" + "═" * 72)
print("  SEÇÃO 6 — Desafio (Opcional)")
print("═" * 72)


# ------------------------------------------------------------------------------
# Q6.1 — Richardson/Romberg
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 6.1 — Richardson/Romberg")
print("─" * 72)

f_romb = lambda x: 1 / x
a_romb, b_romb = 1.0, 2.0
exato_romb = np.log(2)

# (a) R(h) = [4T(h/2) - T(h)]/3  ≡  Simpson 1/3(2n)
n_r   = 4
T_h   = trapezios(f_romb, a_romb, b_romb, n_r)
T_h2  = trapezios(f_romb, a_romb, b_romb, 2 * n_r)
R_h   = (4 * T_h2 - T_h) / 3
S_2n  = simpson13(f_romb, a_romb, b_romb, 2 * n_r)

print(f"\n(a) Verificação: R(h) = [4·T(h/2) - T(h)] / 3  ≡  Simpson(2n)")
print(f"  T(n={n_r})           = {T_h:.10f}")
print(f"  T(n={2*n_r})          = {T_h2:.10f}")
print(f"  R(h)              = {R_h:.10f}")
print(f"  Simpson(n={2*n_r})    = {S_2n:.10f}")
print(f"  |R(h) - Simpson(2n)| = {abs(R_h - S_2n):.2e}   → equivalência confirmada")

# (b) Tabela de Romberg completa: h = 0.5, 0.25, 0.125 (n = 2, 4, 8)
ns_romb = [2, 4, 8]
T0 = [trapezios(f_romb, a_romb, b_romb, n) for n in ns_romb]

tabela_romb = [T0]
nivel = T0
k = 1
while len(nivel) > 1:
    fator = 4**k
    novo_nivel = [(fator * nivel[i+1] - nivel[i]) / (fator - 1) for i in range(len(nivel) - 1)]
    tabela_romb.append(novo_nivel)
    nivel = novo_nivel
    k += 1

print(f"\n(b) Tabela de Romberg para ∫₁² 1/x dx  (h = 0.5, 0.25, 0.125)")
print(f"  {'Nível':<8}{'Ordem':<10}{'Valores'}")
print("  " + "─" * 66)
for nivel_idx, linha in enumerate(tabela_romb):
    ordem = 2 * (nivel_idx + 1)
    valores_str = "  ".join(f"{v:.8f}" for v in linha)
    print(f"  R{nivel_idx:<7}O(h^{ordem}){'':<3}{valores_str}")

print(f"\n  Erros absolutos:")
for nivel_idx, linha in enumerate(tabela_romb):
    ordem = 2 * (nivel_idx + 1)
    erros_str = "  ".join(f"{abs(v-exato_romb):.2e}" for v in linha)
    print(f"  R{nivel_idx}  O(h^{ordem})  {erros_str}")

# Estender a tabela até encontrar erro < 1e-10, contando avaliações únicas de f
tol_romb = 1e-10
ns_ext   = [2, 4, 8, 16, 32]
T0_ext   = [trapezios(f_romb, a_romb, b_romb, n) for n in ns_ext]

tabela_ext = [T0_ext]
nivel = T0_ext
k = 1
while len(nivel) > 1:
    fator = 4**k
    novo_nivel = [(fator*nivel[i+1]-nivel[i])/(fator-1) for i in range(len(nivel)-1)]
    tabela_ext.append(novo_nivel)
    nivel = novo_nivel
    k += 1

melhor_n_finest = None
melhor_erro = None
for nivel_idx, linha in enumerate(tabela_ext):
    for col_idx, v in enumerate(linha):
        erro_v = abs(v - exato_romb)
        n_finest = ns_ext[col_idx + nivel_idx]
        if erro_v < tol_romb and (melhor_n_finest is None or n_finest < melhor_n_finest):
            melhor_n_finest = n_finest
            melhor_erro = erro_v

avals_necessarias = melhor_n_finest + 1   # malha mais fina; pontos são aninhados por bisseção

print(f"\n  Estendendo a tabela até n = {ns_ext[-1]} para atingir erro < {tol_romb:.0e}:")
print(f"  Menor malha final necessária : n = {melhor_n_finest}  (h = {(b_romb-a_romb)/melhor_n_finest})")
print(f"  Erro atingido                : {melhor_erro:.2e}")
print(f"  Avaliações de f (pontos únicos, malhas aninhadas): {avals_necessarias}")

# (c) Comparação de eficiência
print(f"\n(c) Comparação de eficiência: Romberg × Gauss-Legendre")
print(f"  {'Método':<26}  {'Avaliações':>10}  {'Erro':>10}")
print("  " + "─" * 52)
print(f"  {'Romberg (Richardson)':<26}  {avals_necessarias:>10}  {melhor_erro:>10.2e}")
for n in range(2, 8):
    G = gauss_legendre(f_romb, a_romb, b_romb, n)
    erro_g = abs(G - exato_romb)
    print(f"  {'Gauss-Legendre n='+str(n):<26}  {n:>10}  {erro_g:>10.2e}")

print(f"""
  Romberg precisa de {avals_necessarias} avaliações de f para atingir
  erro < {tol_romb:.0e}, enquanto Gauss-Legendre atinge erro comparável
  (ou menor) com apenas 6-7 pontos. Isso ocorre porque Gauss-Legendre
  escolhe os nós de forma ótima (maximizando o grau de exatidão por
  ponto), enquanto Romberg parte de malhas uniformes e usa
  extrapolação para cancelar termos de erro sucessivos — eficaz, mas
  ainda limitado pelo número de avaliações da malha mais fina. Para
  funções suaves como 1/x, Gauss-Legendre é ordens de magnitude mais
  eficiente por avaliação de função.
""")


# ------------------------------------------------------------------------------
# Q6.2 — Monte Carlo
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 6.2 — Monte Carlo")
print("─" * 72)

f_mc     = lambda x: np.exp(-x**2)
exato_mc = np.sqrt(np.pi) / 2 * erf(1.0)      # ∫₀¹ e^(-x²) dx

print(f"\n  ∫₀¹ e^(-x²) dx = (√π/2)·erf(1) = {exato_mc:.8f}")

# (a) Monte Carlo com N = 10², 10³, 10⁴, 10⁵ — média de 20 execuções
Ns_mc = [100, 1000, 10000, 100000]
erros_mc = []

print(f"\n(a) Monte Carlo — erro médio de 20 execuções")
print(f"  {'N':>8}  {'Erro médio':>12}")
print("  " + "─" * 24)
for N in Ns_mc:
    erros_rep = []
    for rep in range(20):
        rng = np.random.default_rng(1000 + rep)
        x_amostra = rng.uniform(0, 1, N)
        I_mc = np.mean(f_mc(x_amostra))       # volume do domínio = 1
        erros_rep.append(abs(I_mc - exato_mc))
    erro_medio = np.mean(erros_rep)
    erros_mc.append(erro_medio)
    print(f"  {N:>8}  {erro_medio:>12.2e}")

# (b) Verificação O(N^-1/2) em log-log
incl_mc = np.polyfit(np.log(Ns_mc), np.log(erros_mc), 1)[0]

fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(Ns_mc, erros_mc, "o-", color="darkorange", label="Monte Carlo")
Ns_ref = np.array([100.0, 100000.0])
ax.loglog(Ns_ref, erros_mc[0] * (Ns_ref/Ns_mc[0])**-0.5, "k--", linewidth=0.8, label="incl. −1/2 (ref.)")
ax.set_xlabel("N  (amostras)")
ax.set_ylabel("Erro absoluto médio")
ax.set_title("Q6.2 — Convergência de Monte Carlo")
ax.legend()
ax.grid(True, which="both", linestyle=":", linewidth=0.5)
plt.tight_layout()
plt.savefig("q62_montecarlo.png", dpi=300)
plt.close()

print(f"\n(b) Gráfico salvo: q62_montecarlo.png")
print(f"  Inclinação log-log observada: {incl_mc:.3f}  (esperado −0.5, O(N^-1/2))")

# (c) N necessário para erro < 1e-4, comparado com Gauss-Legendre
C_mc       = erros_mc[-1] * np.sqrt(Ns_mc[-1])     # erro ≈ C/√N
N_para_1e4 = int(np.ceil((C_mc / 1e-4) ** 2))

print(f"\n(c) N necessário para erro < 1e-4")
print(f"  Ajuste erro ≈ C/√N  →  C ≈ {C_mc:.4f}")
print(f"  N necessário        ≈ {N_para_1e4:.2e}")

print(f"\n  Comparação com Gauss-Legendre:")
print(f"  {'n (GL)':>8}  {'Erro':>10}")
print("  " + "─" * 20)
for n in range(2, 6):
    G = gauss_legendre(f_mc, 0, 1, n)
    print(f"  {n:>8}  {abs(G - exato_mc):>10.2e}")

print(f"""
  Monte Carlo precisaria de aproximadamente {N_para_1e4:.0e} amostras
  para atingir erro < 1e-4, enquanto Gauss-Legendre atinge erro muito
  menor com apenas 3-4 pontos. Para uma função suave em 1D, Monte
  Carlo é extremamente ineficiente comparado a quadraturas
  determinísticas — sua vantagem só aparece em dimensões altas.
""")

# (d) Extensão para 2D: ∫₀¹∫₀¹ e^(-(x²+y²)) dx dy
f2_mc    = lambda x, y: np.exp(-(x**2 + y**2))
exato_2d = exato_mc ** 2      # integral se separa em produto de duas 1D

erros_mc_2d = []
for N in Ns_mc:
    erros_rep = []
    for rep in range(20):
        rng = np.random.default_rng(2000 + rep)
        x_amostra = rng.uniform(0, 1, N)
        y_amostra = rng.uniform(0, 1, N)
        I_2d = np.mean(f2_mc(x_amostra, y_amostra))
        erros_rep.append(abs(I_2d - exato_2d))
    erros_mc_2d.append(np.mean(erros_rep))

print(f"\n(d) Extensão 2D: ∫₀¹∫₀¹ e^(-(x²+y²)) dx dy = {exato_2d:.8f}")
print(f"  {'N':>8}  {'Erro médio MC (2D)':>18}")
print("  " + "─" * 30)
for N, e in zip(Ns_mc, erros_mc_2d):
    print(f"  {N:>8}  {e:>18.2e}")

# Gauss-Legendre 2D via produto tensorial
from numpy.polynomial.legendre import leggauss

def gauss_legendre_2d(f, n):
    t, A = leggauss(n)
    x = 0.5 * t + 0.5     # transformação [-1,1] → [0,1]
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += A[i] * A[j] * f(x[i], x[j])
    return 0.25 * total   # jacobiano (0.5)² por eixo

print(f"\n  Gauss-Legendre 2D (produto tensorial n×n)")
print(f"  {'n':>4}  {'Avaliações':>10}  {'Erro':>10}")
print("  " + "─" * 28)
for n in (2, 4, 6):
    G2d = gauss_legendre_2d(f2_mc, n)
    print(f"  {n:>4}  {n*n:>10}  {abs(G2d - exato_2d):>10.2e}")

print(f"""
  Mesmo em 2D, Gauss-Legendre ainda domina: com n=4 (16 avaliações)
  atinge erro muito menor que Monte Carlo com N=10⁵ (100.000 amostras).
  Isso ocorre porque o custo de Gauss-Legendre cresce como n^d
  (exponencial na dimensão d), enquanto o de Monte Carlo permanece
  O(N) independente de d, com erro sempre O(N^-1/2). A vantagem de
  Monte Carlo só se manifesta quando a dimensão é alta o suficiente
  (tipicamente d ≳ 5-8, dependendo da suavidade do integrando) para
  que n^d supere o custo fixo de Monte Carlo — daí seu uso dominante
  em problemas de alta dimensão (finanças, física estatística,
  aprendizado de máquina), onde quadraturas por produto tensorial
  se tornam inviáveis.
""")


# ------------------------------------------------------------------------------
# Q6.3 — Gradient Check
# ------------------------------------------------------------------------------
print("\n" + "─" * 72)
print("QUESTÃO 6.3 — Gradient Check")
print("─" * 72)

rng_gc = np.random.default_rng(42)
K_gc   = 20
X_gc   = rng_gc.standard_normal((K_gc, 3))
theta_verdadeiro = np.array([2.0, -1.0, 0.5])
y_gc   = X_gc @ theta_verdadeiro + 0.1 * rng_gc.standard_normal(K_gc)

theta0 = np.array([0.5, 0.5, 0.5])

def perda(theta):
    """L(theta) = Σ (θᵀxₖ - yₖ)²"""
    r = X_gc @ theta - y_gc
    return np.sum(r**2)

# (a) Gradiente analítico: ∇L = 2 Xᵀ(Xθ - y)
grad_analitico = 2 * X_gc.T @ (X_gc @ theta0 - y_gc)

print(f"\n(a) Gradiente analítico  ∇L(θ) = 2·Xᵀ(Xθ - y)")
print(f"  θ₀ = {theta0}")
print(f"  ∇L_analítico = {grad_analitico}")

# (b) Gradiente numérico por diferenças centrais (ε = 1e-5)
eps_gc = 1e-5

def gradiente_numerico(theta, eps):
    g = np.zeros_like(theta)
    for i in range(len(theta)):
        t_mais = theta.copy(); t_mais[i] += eps
        t_menos = theta.copy(); t_menos[i] -= eps
        g[i] = (perda(t_mais) - perda(t_menos)) / (2 * eps)
    return g

grad_numerico = gradiente_numerico(theta0, eps_gc)

print(f"\n(b) Gradiente numérico  (diferença central, ε = {eps_gc:.0e})")
print(f"  ∇L_numérico  = {grad_numerico}")

# (c) Diferença relativa
diff_rel = np.linalg.norm(grad_analitico - grad_numerico) / np.linalg.norm(grad_analitico)

print(f"\n(c) Diferença relativa")
print(f"  ‖∇L_analítico − ∇L_numérico‖ / ‖∇L_analítico‖ = {diff_rel:.2e}")
print(f"  Critério (< 1e-5): {'PASSOU ✓' if diff_rel < 1e-5 else 'FALHOU ✗'}  → gradiente correto")

# (d) Por que não usar ε muito pequeno?
epsilons = [1e-2, 1e-4, 1e-5, 1e-7, 1e-9, 1e-11]
print(f"\n(d) Sensibilidade da diferença relativa a ε")
print(f"  {'ε':>8}  {'Diferença relativa':>18}")
print("  " + "─" * 30)
for eps in epsilons:
    g = gradiente_numerico(theta0, eps)
    d = np.linalg.norm(grad_analitico - g) / np.linalg.norm(grad_analitico)
    print(f"  {eps:>8.0e}  {d:>18.2e}")

print(f"""
  Assim como na Seção 1.3, o erro da diferença central tem dois
  regimes: para ε "grande" o erro de truncamento já é desprezível
  para esta função quadrática, e a diferença relativa fica dominada
  pelo arredondamento de máquina, que CRESCE quando ε diminui
  (subtração de valores de perda quase iguais perde dígitos
  significativos). Por isso o gradient check não deve usar ε
  extremamente pequeno (ex.: 1e-11): em vez de melhorar a precisão,
  ele amplifica o erro de cancelamento catastrófico — o mesmo
  fenômeno do h_opt identificado para df_central na Seção 1.3.
""")

# =============================================================================
# FIM DO SCRIPT
# =============================================================================

print("\n" + "═" * 72)
print("  FIM DA EXECUÇÃO — Relatório gerado por:")
print("  Jeann Victor Batista, Pedro Augusto de Souza Finnochio, Thiago Martins da Silva")
print("═" * 72)