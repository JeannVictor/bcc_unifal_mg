#ifndef TP3_H
#define TP3_H

#define MAX_CAMPO 100
#define MAX_JOGADOR 1150
#define NUM_BALDES 26

// Struct Utilizada
typedef struct {
    char nome[MAX_CAMPO];
    char posicao[MAX_CAMPO];
    char pais[MAX_CAMPO];
    char clube[MAX_CAMPO];
    int idade;
} jogador;

// Função para ler o arquivo 'jogadores.csv'
int lerArquivo(jogador array[], const char* nomeArquivo);

// Funções para Algoritmo Bubble-Sort
void swap(jogador *a, jogador *b);
void bubbleSort(jogador arr[], int n,int *comparacao,int *troca,size_t *memoria_total);

// Funções para Algoritmo Merge-Sort
void merge(jogador arr[], int n, int *comparacao, int *troca, int begin, int mid, int end,size_t *memoria_total);
void mergeSort(jogador arr[], int n, int *comparacao, int *troca, int begin, int end,size_t *memoria_total);

// Função para Algoritmo Bucket-Sort
void bucketSort(jogador arr[], int N, int *comparacao, int *troca, size_t *memoria_total);

#endif