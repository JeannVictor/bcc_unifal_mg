# Trabalho 2 — Caixeiro Viajante (força bruta)

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Implementação em C do Problema do Caixeiro Viajante (TSP) usando busca por força bruta (permutação de todas as rotas possíveis, calculando a distância euclidiana entre cidades e mantendo o tour de menor custo).

---

## Estrutura

| Caminho | Descrição |
|---|---|
| `descricao.pdf` | Enunciado do trabalho |
| `source/main.c` | Código-fonte |
| `instancias/` | Instâncias de teste no formato `.tsp` (conjuntos de cidades usados como entrada), como `berlin52.tsp`, `a280.tsp`, etc. |
| `makefile` | Script de build |

---

## Compilar e rodar

```bash
make
./tp2
```

O binário gerado se chama `tp2`. Para limpar os artefatos de build:

```bash
make clean
```

---

Por ser força bruta (O(n!)), o programa só é viável para instâncias pequenas.
