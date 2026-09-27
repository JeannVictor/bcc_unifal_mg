# Resoluções — Programação Lógica (Prolog)

![Prolog](https://img.shields.io/badge/Prolog-blue)

Resoluções de exercícios em Prolog, sem estrutura de projeto/build (arquivos `.pl` avulsos).

---

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `list01/`, `list02/` | Resolução de cada questão da lista em um arquivo numerado (`1.pl`, `2.pl`, ...), junto com o PDF do enunciado da lista (`lista1.pdf`, `lista2.pdf`) |
| `provas/` | Resoluções das provas da disciplina (`prova1_2025.pl`, `prova2_2025.pl`) |
| `resolution_slides/exercicio_sala/` | Atividade feita em sala (`atividade.pdf` + `sala.pl`) |
| `resolution_slides/linguagem_prolog_slide/` | Exercícios baseados no slide `linguagem_prolog.pdf`, resolvidos em arquivos numerados |

---

## Como rodar

Cada arquivo é independente. Com o SWI-Prolog instalado, carregue e consulte no interativo:

```bash
swipl arquivo.pl
```

Dentro do interpretador, use `?- predicado(argumentos).` para testar os predicados definidos no arquivo.
