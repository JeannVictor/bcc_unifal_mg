import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import numpy as np

# --- Leitura do CSV ---
with open("grafo.csv", "r") as f:
    lines = [line.strip() for line in f.readlines()]

# Processa a matriz de adjacência
header = [name.strip() for name in lines[0].split(",")[1:11]]
data_lines = lines[1:11]
adj_data = []
for line in data_lines:
    parts = line.split(",")
    adj_data.append([float(x.strip()) if x.strip() else 0 for x in parts[1:11]])

df = pd.DataFrame(adj_data, columns=header, index=[line.split(",")[0].strip() for line in data_lines])

# Processa os dados de betweenness da última linha
betweenness_line = lines[11].split(",")[1:11]
betweenness_data = {node: float(val) for node, val in zip(header, betweenness_line)}

# --- Construção do Grafo ---
G = nx.from_pandas_adjacency(df)

# Adiciona atributos
nx.set_node_attributes(G, betweenness_data, "betweenness")

# --- Layout ---
pos = {
    'Jaime': [1, 0.8],    # Destaque para o mais central
    'Tyrion': [0.8, 0],    # Segundo mais central
    'Cersei': [1, -0.5],
    'Arya': [-1, 0.5],
    'Bran': [-0.8, -0.3],
    'Brienne': [0.5, 0.5],
    'Catelyn': [-0.5, 0.8],
    'Sam': [-1, -0.5],
    'Sansa': [0, -1],
    'Varys': [0, 0]
}

# --- Arestas ---
edge_traces = []
max_weight = 418  # Do seu CSV: max=418 (Brienne-Jaime)

for u, v, d in G.edges(data=True):
    edge_trace = go.Scatter(
        x=[pos[u][0], pos[v][0], None],
        y=[pos[u][1], pos[v][1], None],
        line=dict(width=0.5 + (d['weight']/max_weight)*10, color='#888'),
        hoverinfo='text',
        hovertext=f"{u} ↔ {v}<br>Peso: {d['weight']}",
        mode='lines',
        showlegend=False
    )
    edge_traces.append(edge_trace)

# --- Nós ---
node_trace = go.Scatter(
    x=[pos[n][0] for n in G.nodes()],
    y=[pos[n][1] for n in G.nodes()],
    mode='markers+text',
    text=list(G.nodes()),
    textposition='top center',
    textfont=dict(size=12, color='black'),
    hoverinfo='text',
    hovertext=[f"<b>{node}</b><br>Betweenness: {betweenness_data[node]:.6f}" for node in G.nodes()],
    marker=dict(
        size=[30 + 150*betweenness_data[n] for n in G.nodes()],
        color=[betweenness_data[n] for n in G.nodes()],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title='Betweenness'),
        line=dict(width=2, color='DarkSlateGrey')
    )
)

# --- Figura Final ---
fig = go.Figure(
    data=edge_traces + [node_trace],
    layout=go.Layout(
        title="<b>Rede de Personagens - Dados Exatos do CSV</b><br>"
              "<sub>Pesos: 2-418 | Betweenness: Jaime (0.222222), Tyrion (0.138889)</sub>",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=20, r=20, t=100),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, visible=False),
        plot_bgcolor='white'
    )
)

fig.write_html("grafo_exato.html")
print("✅ Visualização exata gerada em grafo_exato.html")

# --- Verificação ---
print("\nValores de betweenness confirmados:")
for node, val in betweenness_data.items():
    print(f"{node}: {val:.6f}")