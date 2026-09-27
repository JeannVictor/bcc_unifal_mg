#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "p6.h"

// Impressão da matriz
void imprimirmatriz(TMatriz m,int nl,int nc){
    int i,j;
    for(i = 0; i < nl; i++){
        for(j = 0; j < nc; j++)  
            printf("%d ", m[i][j]);
        printf("\n");
    }
}   

// Criação de matriz com números aleatórios
int criamatriz(TMatriz m,int nl,int nc){
    int i,j;
    for(i = 0; i < nl; i++){
        for(j = 0; j < nc; j++)  
            m[i][j] = rand() % 11;
    }
    return 1;
}
// Função de transposição e impressão dela
void transposta(TMatriz m,int nl,int nc){
    int i,j;
    // Criação matriz resultado
    TMatriz mr;
    for(i = 0; i < nl; i++){
        for(j = 0; j < nc; j++)  
            mr[i][j] = 0;
    }

    // Transpondo
    for(i = 0; i < nl; i++){
        for(j = 0; j < nc; j++)  
            mr[j][i] = m[i][j];
    }
    imprimirmatriz(mr, nl,nc);
}

// Função de soma e impressão da soma
void soma(TMatriz m,TMatriz n,int nl,int nc){
    int i,j;
    // Criação matriz resultado
    TMatriz a;
    for(i = 0; i < nl; i++){
        for(j = 0; j < nc; j++)  
            a[i][j] = 0;
    }

    // Soma das matrizes
    for(i = 0; i < nl; i++){
        for(j = 0; j < nc; j++)  
            a[i][j] =m[i][j] + n[i][j];
    }
    imprimirmatriz(a, nl,nc);
}

// Função de multiplicação e impressão da multiplicação
void multiplica(TMatriz m,TMatriz n,int la,int ca,int lb,int cb){
    int i,j,k;

    // Criação matriz resultado
    TMatriz a;
    for(i = 0; i < la; i++){
        for(j = 0; j < cb; j++)  
            a[i][j] = 0;
    }

    // Multiplicação das matrizes
    for (i = 0; i < la; i++) {
        for (j = 0; j < cb; j++) {
            for (k = 0; k < ca; k++) {  
                a[i][j] += m[i][k] * n[k][j];
            }
        }
    }
    imprimirmatriz(a,la,cb);
}

// Função de obter média(soma de todos os elementos/qtd elementos) e impressão da média
void media(TMatriz m,int nl,int nc){
    int i,j;
    float media = 0;
    for(i = 0;i < nl;i++){
        for(j = 0;j < nc;j++)
            media = m[i][j] + media;
    }
    media = media/(nl * nc);
    printf("A média da matriz é:%.2f",media);
}

