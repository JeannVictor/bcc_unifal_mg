#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "tp3.h"

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Uso: ./tp3 x\nonde x é um número entre 1 e 3:\n");
        printf("1 - Bubble Sort\n");
        printf("2 - Merge Sort\n");
        printf("3 - Bucket Sort\n");
        return 1;
    }

    int escolha = atoi(argv[1]);
    if (escolha <= 0 || escolha > 3) {
        printf("Por favor, escolha um número entre 1 e 3\n");
        return 1;
    }

    jogador array[MAX_JOGADOR];
    int total = lerArquivo(array, "jogadores.csv");
    int troca = 0, comparacao = 0;
    size_t memoria_total = 0;
    clock_t inicio, fim;
    double tempo_total;

    switch(escolha) {
        case 1:
            printf("Executando Bubble Sort...\n");
            inicio = clock();
            bubbleSort(array, total, &comparacao, &troca,&memoria_total);
            fim = clock();
            break;
            
        case 2:
            printf("Executando Merge Sort...\n");
            inicio = clock();
            mergeSort(array, total, &comparacao, &troca, 0, total - 1, &memoria_total);
            fim = clock();
            break;
            
        case 3:
            printf("Executando Bucket Sort...\n");
            inicio = clock();
            bucketSort(array,total,&comparacao,&troca,&memoria_total);
            fim = clock();
            break;
    }

    // Calcula o tempo de execução
    tempo_total = ((double)(fim - inicio)) / CLOCKS_PER_SEC * 1000;

    // Imprime os resultados ordenados
    for(int i = 0; i < total; i++) {
        printf("%s,%s,%s,%s,%d\n",
            array[i].nome,
            array[i].posicao,
            array[i].pais,
            array[i].clube,
            array[i].idade);
    }

    // Exibe as estatísticas do algoritmo
    printf("\nEstatísticas do algoritmo:\n");
    printf("Número de comparações: %d\n", comparacao);
    printf("Número de trocas: %d\n", troca);
    printf("Memória total alocada: %zu bytes\n", memoria_total);
    printf("Tempo de execução: %.6f ms\n", tempo_total);

    return 0;
}