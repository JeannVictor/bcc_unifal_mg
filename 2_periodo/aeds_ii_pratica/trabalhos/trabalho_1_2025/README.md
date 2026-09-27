# Trabalho Prático 1 (2025) - Palíndromos

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Implementação em C que verifica, para cada linha de um arquivo de entrada, se o conteúdo é um palíndromo. A regra do trabalho exige o uso exclusivo de pilha e fila (sem percorrer a string em ordem direta/inversa): cada caractere lido é inserido simultaneamente em uma pilha e em uma fila, e a comparação elemento a elemento entre as duas estruturas determina se a expressão é um palíndromo.

---

## Estrutura do Projeto

| Arquivo | Descrição |
|---|---|
| [trabalho.c](./trabalho.c) | Código-fonte com as estruturas de pilha e fila encadeadas e a lógica de verificação |
| [descricao.pdf](./descricao.pdf) | Enunciado oficial do trabalho (DCE792 - AEDS 2) |
| [palindromos.txt](./palindromos.txt) | Arquivo de entrada usado pelo programa, uma expressão por linha |

---

## Como Compilar e Executar

Não há makefile; compile diretamente com gcc:

```bash
gcc trabalho.c -o trabalho
./trabalho
```

O programa lê `palindromos.txt` (deve estar na mesma pasta) e imprime, para cada linha, `1` se for palíndromo ou `0` caso contrário.
