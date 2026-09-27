# Projeto 2: Análise de Alturas Aleatórias

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Este projeto em C/C++ gera aleatoriamente 1000 valores de alturas de pessoas entre **1.5 e 2.3 metros** e realiza análises estatísticas sobre os dados.

---

## Descrição

O programa realiza as seguintes análises:

1. Calcula a **média das alturas**.
2. Determina a **maior altura** registrada.
3. Determina a **menor altura** registrada.
4. Calcula a **porcentagem de pessoas com altura maior que 2.0 metros**.

---

## Como Funciona

O programa utiliza a função `rand()` para gerar alturas aleatórias dentro do intervalo especificado. Com base nos valores gerados, são feitas análises estatísticas básicas, que são exibidas ao usuário no final.

---

## Como Compilar e Executar

```bash
gcc p2.c -o p2
./p2
```
