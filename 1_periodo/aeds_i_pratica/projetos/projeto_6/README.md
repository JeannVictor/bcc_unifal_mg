# Projeto 6: Operações com Matrizes

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Este projeto em C implementa operações matemáticas sobre matrizes de valores inteiros.

---

## Objetivo

O programa utiliza duas matrizes fornecidas pelo usuário para realizar as operações especificadas, armazenando os resultados em uma terceira matriz e exibindo-os na tela. Todas as operações com matrizes são implementadas em funções separadas dentro de uma biblioteca.

---

## Funcionalidades

O programa suporta as seguintes operações:

1. **Encontrar a Transposta de uma Matriz**
   Calcula a matriz transposta de uma das matrizes fornecidas.

2. **Somar Duas Matrizes**
   Realiza a soma elemento a elemento das duas matrizes e armazena o resultado em uma terceira matriz.

3. **Multiplicar Duas Matrizes**
   Realiza a multiplicação de matrizes, de acordo com as regras de álgebra linear.

4. **Calcular o Valor Médio dos Elementos da Primeira Matriz**
   Calcula a média de todos os valores armazenados na primeira matriz.

---

## Estrutura do Projeto

**Código Principal**

O código principal (`main.c`) é responsável por:
- Solicitar ao usuário os valores das dimensões das matrizes.
- Exibir um menu de operações.
- Invocar as funções da biblioteca para realizar as operações.

**Biblioteca de Operações com Matrizes**

A biblioteca (`p6.h` e `funcao.c`) contém funções específicas para cada operação:

| Função | Descrição |
|---|---|
| `transposta()` | Calcula a transposta de uma matriz |
| `soma()` | Soma duas matrizes |
| `multiplica()` | Multiplica duas matrizes |
| `media()` | Calcula a média dos elementos de uma matriz |

---

## Como Compilar e Executar

```bash
gcc main.c funcao.c -o p6
./p6
```
