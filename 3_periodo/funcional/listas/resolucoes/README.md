# Resoluções — Programação Funcional (Haskell)

![Haskell](https://img.shields.io/badge/Haskell-5D4F85?logo=haskell&logoColor=white)

Resoluções de exercícios em Haskell, sem estrutura de projeto/build (arquivos `.hs` avulsos).

---

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `list_01/`, `list_02/` | Resolução de cada questão da lista em um arquivo numerado (`1.hs`, `2.hs`, ...), junto com o PDF do enunciado da lista (`lista_1.pdf`, `lista_2.pdf`) |
| `scripts/` | Scripts avulsos usados em aula/estudo (`script00.hs` a `script9.hs`) |
| `provas/` | Resoluções das provas da disciplina (`prova1.hs`, `prova2.hs`) |

---

## Como rodar

Cada arquivo é independente. Para executar diretamente:

```bash
runghc arquivo.hs
```

Ou, para testar interativamente as funções definidas:

```bash
ghci arquivo.hs
```

Requer GHC/Haskell Platform instalado.
