# Trabalho Prático 1 - Saída do Labirinto

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Este projeto é uma implementação em C para encontrar a saída de um labirinto de tamanho 10x10, utilizando algoritmos e estruturas de dados estudados na disciplina de AEDS 2 (Algoritmos e Estruturas de Dados II).

O objetivo é determinar o caminho entre o ponto de entrada (`E`) e o ponto de saída (`S`) do labirinto, imprimindo os passos na ordem correta, no formato `linha,coluna`.

---

## Estrutura do Projeto

| Arquivo | Descrição |
|---|---|
| [main.c](./main.c) | Código-fonte principal da solução, contendo a lógica para resolver o problema do labirinto |
| [descricao.pdf](./descricao.pdf) | Documento oficial com a descrição detalhada do trabalho, incluindo os requisitos, formato de saída e critérios de avaliação |
| [relatorio.pdf](./relatorio.pdf) | Relatório do trabalho em sua primeira versão (ainda será feito um relatório correto para explicação do código) |
| [makefile](./makefile) | Arquivo de automação para compilar e executar o código |

---

## Como Compilar e Executar

Siga as etapas abaixo para compilar e executar o projeto:

1. Certifique-se de que o `makefile` está na mesma pasta do arquivo `main.c`.
2. No terminal, navegue até o diretório do projeto.
3. Execute os seguintes comandos para compilar e rodar o programa:

```bash
make
make run
```

4. Quando solicitado, informe o nome do arquivo do labirinto (ex.: `labirinto1.txt`).

