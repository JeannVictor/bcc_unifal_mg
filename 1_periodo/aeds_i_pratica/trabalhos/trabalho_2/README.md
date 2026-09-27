# Trabalho 2: Processamento de Imagens PGM

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Programa em C para manipulação de imagens no formato PGM (Portable Gray Map), armazenadas em matriz estática de pixels.

---

## Funcionalidades

O programa carrega uma imagem PGM e oferece um menu com as seguintes operações:

1. Clarear ou escurecer a imagem
2. Gerar o negativo da imagem
3. Binarizar a imagem a partir de um limiar
4. Iconizar a imagem (reduzir para 64x64)
5. Adicionar ruído
6. Suavizar a imagem

Ao sair do menu (opção 0), o resultado é salvo em `edit.pgm`.

---

## Arquivos

| Arquivo | Descrição |
|---|---|
| `main.c` | Menu principal e chamadas às operações |
| `funcao.c` | Implementação das funções de leitura/escrita e processamento da imagem |
| `tp3.h` | Definição da struct `PGMImage` e assinaturas das funções |
| `edit.pgm`, `stanford.pgm` | Imagens de exemplo usadas como entrada/saída |

---

## Como Compilar e Executar

```bash
gcc main.c funcao.c -o trabalho2
./trabalho2
```
