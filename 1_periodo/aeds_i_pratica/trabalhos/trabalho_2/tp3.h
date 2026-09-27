#ifndef TP3_H
#define TP3_H

#define MAX_LAR 1024   // Largura máxima da imagem
#define MAX_ALT 1024  // Altura máxima da imagem

typedef struct {
    int largura;                  // Largura da imagem
    int altura;                 // Altura da imagem
    int cinza;                // Valor máximo de tons de cinza
    int pixels[MAX_ALT][MAX_LAR];  // Pixels armazenados em array estático
} PGMImage;

int lerPGM(const char *arquivo, PGMImage *image);
void escreverPGM(const char *filename, PGMImage *image);
void claridade(PGMImage *image,int fator);
void negativo(PGMImage *image);
void binarizar(PGMImage *image,int fator);
void iconizar(PGMImage *image);
void ruido(PGMImage *image,int ruido);
void suavizar(PGMImage *image);

#endif