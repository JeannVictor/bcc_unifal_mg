#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tp3.h"

int lerPGM(const char *arquivo, PGMImage *image) {
    FILE *file = fopen(arquivo, "r");
    if (!file) {
        perror("Erro ao abrir o arquivo");
        return 0;
    }

    char format[3];
    fscanf(file, "%2s", format);
    if (strcmp(format, "P2") != 0) {
        fprintf(stderr, "Formato inválido: %s\n", format);
        fclose(file);
        return 0;
    }

    fscanf(file, "%d %d", &image->largura, &image->altura);
    if (image->largura > MAX_LAR|| image->altura > MAX_ALT) {
        fprintf(stderr, "Erro: Dimensões excedem o limite máximo (%dx%d).\n", MAX_LAR, MAX_ALT);
        fclose(file);
        return 0;
    }

    fscanf(file, "%d", &image->cinza);

    for (int i = 0; i < image->altura; i++) {
        for (int j = 0; j < image->largura; j++) {
            fscanf(file, "%d", &image->pixels[i][j]);
        }
    }

    fclose(file);
    return 1;
}

void escreverPGM(const char *filename, PGMImage *image) {
    FILE *file = fopen(filename, "w");
    if (!file) {
        perror("Erro ao abrir o arquivo para escrita");
        return;
    }

    fprintf(file, "P2\n");
    fprintf(file, "%d %d\n", image->largura, image->altura);
    fprintf(file, "%d\n", image->cinza);

    for (int i = 0; i < image->altura; i++) {
        for (int j = 0; j < image->largura; j++) {
            fprintf(file, "%d ", image->pixels[i][j]);
        }
        fprintf(file, "\n");
    }

    fclose(file);
}

// Função para aplicar efeito de escurecer ou clarear por um fator
void claridade(PGMImage *image,int fator){
    for (int i = 0; i < image->altura; i++) {
        for (int j = 0; j < image->largura; j++){
            if(fator >= 0){
                image->pixels[i][j] = image->pixels[i][j] + fator;
                if(image->pixels[i][j] > 255)
                    image->pixels[i][j] = 255;
            }else{
                image->pixels[i][j] = image->pixels[i][j] + fator;
                if(image->pixels[i][j] < 0)
                    image->pixels[i][j] = 0;    
            }
        }          
    }
}


// FUnção para gerar a imagem negativa
void negativo(PGMImage *image){
    for (int i = 0; i < image->altura; i++) {
        for (int j = 0; j < image->largura; j++)
            image->pixels[i][j] = image->cinza - image->pixels[i][j];    
    }
}

// Função para binarizar a imagem por um fator
void binarizar(PGMImage *image,int fator){
    for (int i = 0; i < image->altura; i++) {
        for (int j = 0; j < image->largura; j++){
            if(image->pixels[i][j] >= fator){
                image->pixels[i][j] = 255;
            }else{
                image->pixels[i][j] = 0;
            }
        }          
    }
}

void iconizar(PGMImage *image) {
    // Verificar se a imagem original tem dimensões suficientes
    if (image->altura < 64 || image->largura < 64) {
        printf("Erro: A imagem é muito pequena para ser reduzida a 64x64.\n");
        return;
    }

    // Criar uma nova imagem para armazenar a versão reduzida
    PGMImage nova_imagem;
    nova_imagem.altura = 64;
    nova_imagem.largura = 64;
    nova_imagem.cinza = image->cinza;

    // Calcular os fatores de redução
    int fator_altura = image->altura / nova_imagem.altura;
    int fator_largura = image->largura / nova_imagem.largura;

    // Reduzir a imagem usando média dos pixels no bloco
    for (int i = 0; i < nova_imagem.altura; i++) {
        for (int j = 0; j < nova_imagem.largura; j++) {
            // Calcular a região do bloco
            int soma = 0;
            int contador = 0;

            for (int di = 0; di < fator_altura; di++) {
                for (int dj = 0; dj < fator_largura; dj++) {
                    int ni = i * fator_altura + di;
                    int nj = j * fator_largura + dj;

                    // Garantir que os índices estão dentro dos limites da imagem original
                    if (ni >= 0 && ni < image->altura && 
                        nj >= 0 && nj < image->largura) {
                        soma += image->pixels[ni][nj];
                        contador++;
                    }
                }
            }

            // Calcular a média do bloco
            nova_imagem.pixels[i][j] = (contador > 0) ? (soma / contador) : 0;
        }
    }

    // Substituir a imagem original pela versão reduzida
    *image = nova_imagem;
}


// Função para criar ruídos na imagem
void ruido(PGMImage *image,int ruido){

    int alturar = 0,colunar = 0;

    for (int i = 0; i < ruido; i++) {
        alturar = rand()%image->altura;
        colunar = rand()%image->largura;

        image->pixels[alturar][colunar] = (rand() % 2) * 255;          
    }
}

// Função para suavizar a imagem
void suavizar(PGMImage *image) {
    int altura = image->altura;
    int largura = image->largura;

    // Criar uma cópia da matriz original para preservar os valores ao calcular a média
    int copia[altura][largura];

    // Copiar a matriz original para a cópia
    for (int i = 0; i < altura; i++) {
        for (int j = 0; j < largura; j++) {
            copia[i][j] = image->pixels[i][j];
        }
    }

    // Aplicar a suavização
    for (int i = 0; i < altura; i++) {
        for (int j = 0; j < largura; j++) {
            int soma = 0;
            int contador = 0;

            // Percorrer os vizinhos na janela 3x3
            for (int di = -1; di < 2; di++) {
                for (int dj = -1; dj < 2; dj++) {
                    int ni = i + di;  // Nova linha
                    int nj = j + dj;  // Nova coluna

                    // Verificar se o vizinho está dentro dos limites da matriz
                    if (ni >= 0 && ni < altura && nj >= 0 && nj < largura) {
                        soma += copia[ni][nj];
                        contador++;
                    }
                }
            }

            // Atualizar o pixel central com a média dos vizinhos
            image->pixels[i][j] = soma / contador;
        }
    }
}






