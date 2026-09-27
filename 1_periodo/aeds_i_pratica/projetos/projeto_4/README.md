# Projeto 4: Operações em Vetores

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Este projeto tem como objetivo realizar diversas operações em um vetor de 1000 posições armazenando valores inteiros. O programa apresenta um menu interativo para o usuário realizar as operações desejadas quantas vezes forem necessárias.

---

## Funcionalidades

O programa permite as seguintes operações no vetor:

1. **Buscar pela Primeira Ocorrência de um Valor**
   O programa retorna a posição da primeira ocorrência de um valor informado pelo usuário.

2. **Contar a Quantidade de Ocorrências de um Valor**
   O programa conta quantas vezes um valor aparece no vetor.

3. **Contar a Quantidade de Ocorrências de Valores em um Intervalo**
   O programa verifica quantos valores dentro de um intervalo (mínimo e máximo) aparecem no vetor.

4. **Inverter os Valores do Vetor**
   O programa reverte a ordem dos elementos no vetor.

5. **Excluir um Valor Informado pelo Usuário**
   O programa remove o valor informado e desloca os elementos à esquerda para evitar "buracos".

6. **Retirar Todos os Valores Repetidos**
   O programa elimina valores duplicados no vetor, mantendo apenas a primeira ocorrência de cada valor.

---

## Estrutura do Programa

1. **Entrada de Dados**
   O usuário insere valores inteiros no vetor (até 1000 posições). Para simular valores iniciais, o vetor pode ser preenchido automaticamente.

2. **Menu Interativo**
   Um menu permite ao usuário escolher uma das operações listadas. O programa executa a operação e exibe o resultado.

3. **Operações e Processamento**
   As funções responsáveis pelas operações utilizam lógica eficiente para manipular o vetor sem comprometer o desempenho.

4. **Execução Contínua**
   Após realizar uma operação, o programa retorna ao menu para permitir novas interações até que o usuário opte por sair.

---

## Como Compilar e Executar

```bash
gcc p4.c -o p4
./p4
```
