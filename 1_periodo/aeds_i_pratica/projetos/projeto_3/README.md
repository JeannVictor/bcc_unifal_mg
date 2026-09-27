# Projeto 3: Cena Gráfica

![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)

Este projeto em C implementa a leitura de um arquivo-texto (`cenagrafica.txt`) que descreve uma cena composta por objetos geométricos bidimensionais (2D) e tridimensionais (3D).

---

## Descrição

Cada linha do arquivo representa um objeto geométrico, incluindo seu nome e os parâmetros necessários para calcular sua área ou volume. Ao final do processamento, o programa calcula e exibe:

1. **Área Total da Cena**: soma das áreas de todos os objetos 2D/3D.
2. **Volume Total da Cena**: soma dos volumes de todos os objetos 3D.

O arquivo deve seguir o formato especificado e incluir uma linha final com a palavra-chave `fim` para indicar o término da lista de objetos.

---

## Funcionalidades

1. **Leitura do Arquivo**
   O programa lê o arquivo `cenagrafica.txt` e interpreta cada linha para identificar o objeto e seus parâmetros.

2. **Cálculo de Área e Volume**
   - Para objetos 2D, calcula a área com base nos parâmetros fornecidos.
   - Para objetos 3D, calcula a área/volume com base nos parâmetros fornecidos.

3. **Exibição dos Resultados**
   O programa exibe na tela:
   - A **área total** de todos os objetos.
   - O **volume total** de todos os objetos 3D.

---

## Como Compilar e Executar

```bash
gcc p3.c -o p3
./p3
```

O programa espera o arquivo `cenagrafica.txt` no diretório de execução.
