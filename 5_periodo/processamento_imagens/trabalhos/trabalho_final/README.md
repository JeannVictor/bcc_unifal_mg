# Trabalho Final - Processamento de Imagens

![C](https://img.shields.io/badge/C-C11-a8b9cc)
![Make](https://img.shields.io/badge/build-make-blue)

Codificação e decodificação de contornos de imagens binárias usando código de cadeia (chain code), conforme `atividade_codigo_cadeia.pdf`.

---

## Arquivos

| Arquivo | Descrição |
|---|---|
| `main.c` | Ponto de entrada do programa |
| `codificacao.c` | Implementação da codificação do contorno |
| `decodificacao.c` | Implementação da decodificação do contorno |
| `codigo_cadeia.h` | Cabeçalho com as definições comuns |
| `imagem_teste.pbm` | Imagem binária de teste |
| `makefile` | Build do projeto |

---

## Como rodar

```bash
make
make run
```

Ou, para limpar os binários gerados:

```bash
make clean
```
