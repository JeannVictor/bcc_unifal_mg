#ifndef PROJ_GAME_OF_TRONES_H
#define PROJ_GAME_OF_TRONES_H

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
/*
Struct que armazena:
e a posição encontrada no texto.
@param nome: índice do nome do personagem
@param posicao: posição encontrada no texto
@note O índice do nome do personagem é o índice no vetor de nomes
declarado no arquivo main.c.
*/
typedef struct posicoes_{
    int nome;
    int posicao;
}posicoes;


/*
Struct que armazena:
@param tam_alocado: tamanho alocado do vetor
@param tam: tamanho atual do vetor
@param elm: vetor de struct posições
*/
typedef struct vetor_{
    int tam_alocado, tam;
    posicoes *elm;
}vetor;

vetor *iniciaVet(int tam_inicial);
void insereVet(vetor *vet, posicoes valor);
bool compSemPontu(char *str1, const char *str2);
void insereHeap(int heap[], int pos[], int v, int *tamHeap, int dist[]);
int removeMin(int heap[], int pos[], int *tamHeap, int dist[]);

double *brandesBetwenness(int **grafo, int n);
int nCompoConexos(int **grafo, int n);

#endif