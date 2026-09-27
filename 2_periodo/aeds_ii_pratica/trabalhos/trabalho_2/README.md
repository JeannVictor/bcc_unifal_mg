# Trabalho Prático 2 - Comparação entre Árvores Balanceadas e Não-Balanceadas

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Este projeto implementa e compara o desempenho entre uma Árvore Binária de Busca (BST) não balanceada e uma Árvore AVL (balanceada), medindo o tempo de execução para operações de inserção e remoção em diferentes instâncias de teste.

---

## Estrutura do Projeto

| Arquivo | Descrição |
|---|---|
| [arvores.c](./arvores.c) | Código-fonte principal contendo as funções de medição de tempo e execução das operações |
| [arvores.h](./arvores.h) | Arquivo header com as declarações das estruturas e protótipos das funções |
| [funcoes.c](./funcoes.c) | Implementação das funções para BST e AVL |
| [descricao.pdf](./descricao.pdf) | Documento com a descrição detalhada do trabalho e requisitos |
| [instancias/](./instancias/) | Diretório contendo os arquivos de teste (1, 2, 3) com operações de inserção e remoção |
| [makefile](./makefile) | Arquivo para automatizar a compilação |

---

## Como Compilar e Executar

1. Certifique-se de que todos os arquivos estão no diretório correto.
2. No terminal, navegue até o diretório do projeto.
3. Execute os comandos:

```bash
make clean
make
./arvores N
```

Onde `N` é o número da instância (1 a 10) que você deseja testar.

---

## Formato das Entradas

Cada arquivo de instância contém operações no formato:

- `I X` - Inserir o valor X na árvore
- `R X` - Remover o valor X da árvore

---

## Formato da Saída

O programa imprime dois números em ponto flutuante:

1. Tempo de execução para a árvore binária não-balanceada
2. Tempo de execução para a árvore AVL

### Exemplo de Saída

```
0.437499
0.006574
```

Onde o primeiro número representa o tempo da BST e o segundo o tempo da AVL.

