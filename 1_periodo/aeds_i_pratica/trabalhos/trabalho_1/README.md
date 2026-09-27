# Trabalho 1: Estatística em Base de Dados de Veículos

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Este projeto tem como objetivo desenvolver um aplicativo em C para manipulação de registros de veículos armazenados em um arquivo texto.

---

## Objetivo

O sistema permite incluir, buscar, excluir e realizar análises estatísticas sobre os dados, consolidando o aprendizado em manipulação de registros, vetores e variáveis simples.

---

## Funcionalidades

### Operações Disponíveis

1. **Incluir um Novo Veículo**
   Adiciona um novo registro de veículo ao vetor de registros, desde que não exceda o limite de 100 registros.

2. **Buscar Veículo pela Placa com Opção de Exclusão**
   Localiza um veículo pela placa e, opcionalmente, o exclui da base de dados, marcando-o como inválido.

3. **Buscar Veículos pelo Tipo**
   Filtra e exibe todos os veículos de um tipo específico.

4. **Buscar Veículos pelo Câmbio**
   Filtra e exibe todos os veículos com um tipo de câmbio específico.

5. **Buscar Veículos por Faixa de Valores**
   Filtra e exibe todos os veículos cujo valor esteja dentro de uma faixa informada pelo usuário.

6. **Relatório do Banco de Dados**
   Apresenta um resumo estatístico da base de dados, incluindo:
   - Porcentagens de veículos por categoria de tipo.
   - Porcentagens de veículos por tipo de combustível.
   - Veículo mais barato com motor 1.0, seu financiamento em 60 meses e taxa de juros atual.
   - Veículo mais caro com direção hidráulica e câmbio automático, e o valor estimado do seguro.
   - Quantidade e média de quilometragem dos veículos com 5 anos ou mais (2019).

---

## Como Compilar e Executar

```bash
gcc main.c functions.c -o trabalho1
./trabalho1
```

O programa espera o arquivo `bd_veiculosed.txt` no diretório de execução.
