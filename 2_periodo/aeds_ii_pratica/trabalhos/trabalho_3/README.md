# Trabalho Prático 3 - Ordenação de Structs

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Este projeto implementa e compara o desempenho entre três diferentes algoritmos de ordenação: um método simples (Bubble Sort), um método ótimo (Merge Sort) e um método em tempo linear (Bucket Sort). O objetivo é ordenar estruturas de dados (structs) de jogadores com base em seus nomes.

---

## Estrutura do Projeto

| Arquivo | Descrição |
|---|---|
| [main.c](./main.c) | Código-fonte principal contendo a função main e o controle de execução dos algoritmos |
| [funcoes.c](./funcoes.c) | Implementação dos algoritmos de ordenação e funções auxiliares |
| [tp3.h](./tp3.h) | Arquivo header com as declarações das estruturas e protótipos das funções |
| [descricao.pdf](./descricao.pdf) | Documento com a descrição detalhada do trabalho e requisitos |
| [relatorio.pdf](./relatorio.pdf) | Relatório completo do trabalho (com o código feito pelo colega Filipe Bessa Carvalho), incluindo análise dos algoritmos e resultados comparativos |
| [jogadores.csv](./jogadores.csv) | Arquivo de entrada contendo os dados dos jogadores a serem ordenados |
| [makefile](./makefile) | Arquivo para automatizar a compilação |

---

## Como Compilar e Executar

1. Certifique-se de que todos os arquivos estão no diretório correto.
2. No terminal, navegue até o diretório do projeto.
3. Execute os comandos:

```bash
make clean
make all
./tp3 N
```

Onde `N` é o número do algoritmo que você deseja executar:

- `1`: Bubble Sort (método simples)
- `2`: Merge Sort (método ótimo)
- `3`: Bucket Sort (método em tempo linear)

---

## Formato da Entrada

O arquivo `jogadores.csv` contém os dados dos jogadores no formato:

```
Nome,Posição,Naturalidade,Clube,Idade
```

---

## Formato da Saída

O programa imprime:

1. Lista ordenada de jogadores (todos os campos)
2. Quatro métricas de desempenho em linhas separadas:
   - Tempo de execução (em milissegundos)
   - Número de operações de comparação
   - Número de operações de troca
   - Memória total gasta pelo algoritmo

---

## Exemplo de Execução

```bash
./tp3 1
```

Exemplo de saída:

```
[Lista ordenada de jogadores]
...
Estatísticas do algoritmo:
Número de comparações: 657180
Número de trocas: 317179
Memória total alocada: 404 bytes
Tempo de execução: 23.429000 ms
```

