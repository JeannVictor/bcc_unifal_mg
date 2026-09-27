# Trabalho 3 — Análise de rede de personagens

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)

Trabalho de grafos: construção de uma rede de relacionamento entre personagens do livro "A Storm of Swords" (Game of Thrones) a partir do texto bruto, e cálculo de métricas de centralidade sobre essa rede.

---

## Estrutura

| Caminho | Descrição |
|---|---|
| `descricao.pdf` | Enunciado do trabalho |
| `relatorio_tp3_aedsiii.pdf` | Relatório de apresentação |
| `slide_tp3_aedsiii.pdf` | Slide de apresentação |
| `projeto_game_of_trones/` | Código-fonte em C do projeto (ver detalhes abaixo) |
| `grafico/` | Script Python (`script_grafo.py`) que lê o grafo gerado (`grafo.csv`) e produz uma visualização interativa (`grafo_exato.html`) da rede com plotly/networkx |

---

## projeto_game_of_trones/

Lê o texto de `a_storm_of_swords.txt`, localiza as menções a 10 personagens principais e monta uma matriz de relação entre eles baseada na proximidade das menções no texto (personagens citados a até 100 palavras de distância são considerados relacionados). Sobre essa matriz (tratada como grafo), calcula:

- Número de componentes conexos (`compo_conexos.c`)
- Centralidade de intermediação (betweenness) pelo algoritmo de Brandes, usando Dijkstra com fila de prioridade (`brandes_betwenness.c`)

### Arquivos

| Arquivo | Descrição |
|---|---|
| `main.c` | Leitura do texto e orquestração |
| `func_aux.c` | Funções auxiliares (vetor dinâmico, comparação de strings, heap) |
| `compo_conexos.c` | Cálculo de componentes conexos |
| `brandes_betwenness.c` | Centralidade de intermediação (algoritmo de Brandes) |
| `proj_gameof_trones.h` | Cabeçalho com structs e protótipos |
| `anotacoes.txt` | Anotações de estudo (pseudocódigo do algoritmo de Brandes e trechos de código auxiliares) |
| `grafo.csv` | Matriz de adjacência/relações gerada, usada depois pelo script de visualização em `../grafico` |

---

### Compilar e rodar

```bash
make
./ProjetoGameOfTrones.bin
```

Requer que `a_storm_of_swords.txt` esteja no mesmo diretório de execução (já incluído).

Para limpar os artefatos de build:

```bash
make clean
```
