#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Estilo profissional
sns.set_theme(style='whitegrid', font_scale=1.2)
plt.rcParams['figure.figsize'] = (8, 5)

# Lê o CSV
df = pd.read_csv('resultados.csv')

# Converte colunas numéricas
for col in ['enviados', 'retrans', 'descartados', 'taxa_perda_efetiva', 'tempo_s', 'throughput_kbps']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df_valid = df.dropna(subset=['throughput_kbps'])

# ============================================================
# GRÁFICOS
# ============================================================

# 1. Throughput vs N
plt.figure()
for prob in sorted(df_valid['prob'].unique()):
    subset = df_valid[df_valid['prob'] == prob]
    grouped = subset.groupby('janela')['throughput_kbps'].mean().reset_index()
    plt.plot(grouped['janela'], grouped['throughput_kbps'], marker='o', linewidth=2, label=f'{int(prob*100)}%')
plt.xlabel('Tamanho da Janela (N)')
plt.ylabel('Throughput (Kbps)')
plt.title('Throughput vs Tamanho da Janela')
plt.legend(title='Prob. de perda')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('throughput_vs_N.png', dpi=300)
plt.close()

# 2. Retransmissões vs N
plt.figure()
for prob in sorted(df_valid['prob'].unique()):
    subset = df_valid[df_valid['prob'] == prob]
    grouped = subset.groupby('janela')['retrans'].mean().reset_index()
    plt.plot(grouped['janela'], grouped['retrans'], marker='s', linewidth=2, label=f'{int(prob*100)}%')
plt.xlabel('Tamanho da Janela (N)')
plt.ylabel('Número de Retransmissões')
plt.title('Retransmissões vs Tamanho da Janela')
plt.legend(title='Prob. de perda')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('retrans_vs_N.png', dpi=300)
plt.close()

# 3. Perda efetiva vs Probabilidade (N=8)
N_FIXO = 8
subset = df_valid[df_valid['janela'] == N_FIXO]
subset = subset.sort_values('prob')
plt.figure()
plt.plot(subset['prob'], subset['taxa_perda_efetiva'], marker='o', linestyle='--', color='red', linewidth=2, label='Medida')
plt.plot([0, 0.2], [0, 0.2], 'k--', alpha=0.5, label='Ideal (y=x)')
plt.xlabel('Probabilidade configurada')
plt.ylabel('Taxa de perda efetiva (%)')
plt.title(f'Convergência da perda simulada (N={N_FIXO})')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('perda_efetiva.png', dpi=300)
plt.close()

# 4. Tempo total vs N
plt.figure()
for prob in sorted(df_valid['prob'].unique()):
    subset = df_valid[df_valid['prob'] == prob]
    grouped = subset.groupby('janela')['tempo_s'].mean().reset_index()
    plt.plot(grouped['janela'], grouped['tempo_s'], marker='^', linewidth=2, label=f'{int(prob*100)}%')
plt.xlabel('Tamanho da Janela (N)')
plt.ylabel('Tempo total (segundos)')
plt.title('Tempo de Transferência vs Tamanho da Janela')
plt.legend(title='Prob. de perda')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('tempo_vs_N.png', dpi=300)
plt.close()

# 5. Tempo vs Probabilidade (para diferentes N)
plt.figure()
for N in [8, 16, 32]:
    subset = df_valid[df_valid['janela'] == N]
    subset = subset.sort_values('prob')
    plt.plot(subset['prob'], subset['tempo_s'], marker='D', linewidth=2, label=f'N={N}')
plt.xlabel('Probabilidade de perda')
plt.ylabel('Tempo total (segundos)')
plt.title('Tempo de Transferência vs Probabilidade de Perda')
plt.legend(title='Janela')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('tempo_vs_perda.png', dpi=300)
plt.close()

# ============================================================
# TABELAS LATEX
# ============================================================

# Throughput
pivot_tp = df_valid.pivot_table(index='janela', columns='prob', values='throughput_kbps', aggfunc='mean').round(0).astype(int)
pivot_tp.columns = [f'{int(c*100)}%' for c in pivot_tp.columns]
with open('tabela_throughput.tex', 'w') as f:
    f.write(pivot_tp.to_latex(caption='Throughput médio (Kbps) por janela e probabilidade.', label='tab:throughput'))

# Retransmissões
pivot_ret = df_valid.pivot_table(index='janela', columns='prob', values='retrans', aggfunc='mean').round(0).astype(int)
pivot_ret.columns = [f'{int(c*100)}%' for c in pivot_ret.columns]
with open('tabela_retrans.tex', 'w') as f:
    f.write(pivot_ret.to_latex(caption='Número médio de retransmissões por janela e probabilidade.', label='tab:retrans'))

# Tempo
pivot_tempo = df_valid.pivot_table(index='janela', columns='prob', values='tempo_s', aggfunc='mean').round(3)
pivot_tempo.columns = [f'{int(c*100)}%' for c in pivot_tempo.columns]
with open('tabela_tempo.tex', 'w') as f:
    f.write(pivot_tempo.to_latex(caption='Tempo médio de transferência (segundos) por janela e probabilidade.', label='tab:tempo'))

print("✅ Gráficos gerados:")
print("   - throughput_vs_N.png")
print("   - retrans_vs_N.png")
print("   - perda_efetiva.png")
print("   - tempo_vs_N.png")
print("   - tempo_vs_perda.png")
print("✅ Tabelas LaTeX:")
print("   - tabela_throughput.tex")
print("   - tabela_retrans.tex")
print("   - tabela_tempo.tex")