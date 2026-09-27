#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "tp3.h"

// Função auxiliar para trocar dois jogadores no array
void swap(jogador *a, jogador *b) {
    jogador temp = *a;
    *a = *b;
    *b = temp;
}

// Implementação do algoritmo Bubble Sort para ordenar jogadores por nome
void bubbleSort(jogador arr[], int n, int *comparacao, int *troca, size_t *memoria_total) {
    bool swapped; // Variável para rastrear se houve troca na iteração
    *memoria_total += sizeof(jogador); // Memória utilizada para o array de jogadores

    for (int i = 0; i < n - 1; i++) {
        swapped = false; // Reseta o status de troca no início de cada iteração externa
        for (int j = 0; j < n - i - 1; j++) {
            (*comparacao)++; // Incrementa o contador de comparações
            if (strcmp(arr[j].nome, arr[j + 1].nome) > 0) { // Compara nomes dos jogadores
                swap(&arr[j], &arr[j + 1]); // Troca se estiverem na ordem errada
                (*troca)++; // Incrementa o contador de trocas
                swapped = true; // Marca que houve troca nesta iteração
            }
        }
        if (!swapped) // Interrompe se o array já estiver ordenado
            break;
    }
}

// Função auxiliar para mesclar dois subarrays no Merge Sort
void merge(jogador arr[], int n, int *comparacao, int *troca, int begin, int mid, int end, size_t *memoria_total) {
    int dimL = mid - begin + 1; // Tamanho do subarray esquerdo
    int dimR = end - mid;       // Tamanho do subarray direito

    // Alocação dinâmica para subarrays temporários
    jogador *esquerda = malloc(dimL * sizeof(jogador));
    if (esquerda) *memoria_total += dimL * sizeof(jogador);

    jogador *direita = malloc(dimR * sizeof(jogador));
    if (direita) *memoria_total += dimR * sizeof(jogador);

    // Copia os elementos para os subarrays temporários
    for (int i = 0; i < dimL; i++) esquerda[i] = arr[begin + i];
    for (int j = 0; j < dimR; j++) direita[j] = arr[mid + 1 + j];

    // Mescla os subarrays ordenados de volta no array principal
    int i = 0, j = 0, k = begin;
    while (i < dimL && j < dimR) {
        (*comparacao)++; // Incrementa o contador de comparações
        if (strcmp(esquerda[i].nome, direita[j].nome) <= 0) {
            arr[k++] = esquerda[i++];
        } else {
            arr[k++] = direita[j++];
        }
        (*troca)++; // Incrementa o contador de trocas
    }

    // Copia os elementos restantes do subarray esquerdo, se houver
    while (i < dimL) {
        arr[k++] = esquerda[i++];
        (*troca)++;
    }

    // Copia os elementos restantes do subarray direito, se houver
    while (j < dimR) {
        arr[k++] = direita[j++];
        (*troca)++;
    }

    // Libera a memória alocada para os subarrays temporários
    free(esquerda);
    free(direita);
}

// Implementação do algoritmo Merge Sort
void mergeSort(jogador arr[], int n, int *comparacao, int *troca, int begin, int end, size_t *memoria_total) {
    if (begin < end) {
        int mid = begin + (end - begin) / 2; // Calcula o índice do meio

        // Recursivamente divide e ordena os subarrays
        mergeSort(arr, n, comparacao, troca, begin, mid, memoria_total);
        mergeSort(arr, n, comparacao, troca, mid + 1, end, memoria_total);

        // Mescla os subarrays ordenados
        merge(arr, n, comparacao, troca, begin, mid, end, memoria_total);
    }
}

// Implementação do algoritmo Bucket Sort
void bucketSort(jogador arr[], int n, int *comparacao, int *troca, size_t *memoria_total) {
    jogador **baldes = malloc(NUM_BALDES * sizeof(jogador *)); // Array de ponteiros para baldes
    int *sizes = malloc(NUM_BALDES * sizeof(int)); // Array para armazenar o tamanho de cada balde

    // Inicializa os baldes e seus tamanhos
    for (int i = 0; i < NUM_BALDES; i++) {
        baldes[i] = NULL;
        sizes[i] = 0;
    }
    *memoria_total += NUM_BALDES * (sizeof(jogador *) + sizeof(int));

    // Distribui os jogadores nos baldes correspondentes com base na inicial do nome
    for (int i = 0; i < n; i++) {
        char inicial = arr[i].nome[0];
        int index = inicial - 'A'; // Calcula o índice do balde

        if (index >= 0 && index < NUM_BALDES) {
            sizes[index]++;
            baldes[index] = realloc(baldes[index], sizes[index] * sizeof(jogador));
            *memoria_total += sizes[index] * sizeof(jogador);
            baldes[index][sizes[index] - 1] = arr[i];
        }
    }

    // Ordena individualmente cada balde usando Merge Sort
    for (int i = 0; i < NUM_BALDES; i++) {
        if (sizes[i] > 1) {
            mergeSort(baldes[i], sizes[i], comparacao, troca, 0, sizes[i] - 1, memoria_total);
        }
    }

    // Combina os baldes ordenados de volta no array principal
    int k = 0;
    for (int i = 0; i < NUM_BALDES; i++) {
        for (int j = 0; j < sizes[i]; j++) {
            arr[k++] = baldes[i][j];
            (*troca)++;
        }
    }

    // Libera a memória alocada para os baldes
    for (int i = 0; i < NUM_BALDES; i++) {
        if (baldes[i]) free(baldes[i]);
    }
    free(baldes);
    free(sizes);
}

// Função para ler jogadores de um arquivo CSV e armazenar no array
int lerArquivo(jogador array[], const char *nomeArquivo) {
    FILE *arquivo;
    char linha[300]; // Buffer para armazenar cada linha do arquivo
    int totaljogador = 0; // Contador de jogadores

    arquivo = fopen(nomeArquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nomeArquivo);
        return 0;
    }

    fgets(linha, sizeof(linha), arquivo); // Pula a primeira linha (cabeçalho)

    while (fgets(linha, sizeof(linha), arquivo) && totaljogador < MAX_JOGADOR) {
        linha[strcspn(linha, "\n")] = 0; // Remove o caractere de nova linha
        char nome[MAX_CAMPO], posicao[MAX_CAMPO], pais[MAX_CAMPO], clube[MAX_CAMPO];
        int idade;

        // Lê os campos separados por vírgulas
        int lidos = sscanf(linha, "%[^,],%[^,],%[^,],%[^,],%d",
                           nome, posicao, pais, clube, &idade);

        if (lidos == 5) { // Verifica se todos os campos foram lidos corretamente
            strncpy(array[totaljogador].nome, nome, MAX_CAMPO - 1);
            strncpy(array[totaljogador].posicao, posicao, MAX_CAMPO - 1);
            strncpy(array[totaljogador].pais, pais, MAX_CAMPO - 1);
            strncpy(array[totaljogador].clube, clube, MAX_CAMPO - 1);
            array[totaljogador].idade = idade;
            totaljogador++;
        } else {
            printf("Erro ao processar a linha: %s\n", linha);
        }
    }

    fclose(arquivo);
    return totaljogador;
}





