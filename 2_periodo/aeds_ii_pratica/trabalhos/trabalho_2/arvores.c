#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "arvores.h" // Inclui as funções de árvores (BST e AVL)

// Função para medir o tempo de execução das operações na árvore BST
double arvore_binaria(int instancia_num) {
    operacao array[20000];
    double tempo = 0.0;
    clock_t begin = clock();

    // Gera o nome do arquivo com base no número da instância
    char nomeArquivo[50];
    snprintf(nomeArquivo, sizeof(nomeArquivo), "instancias/%d", instancia_num);

    // Executa as operações na BST
    int totalop = lerArquivoBIN(array, nomeArquivo);

    clock_t end = clock();
    tempo += (double)(end - begin) / CLOCKS_PER_SEC;
    return tempo;
}

// Função para medir o tempo de execução das operações na árvore AVL
double arvore_balanceada(int instancia_num) {
    operacao array[20000];
    double tempo = 0.0;
    clock_t begin = clock();

    // Gera o nome do arquivo com base no número da instância
    char nomeArquivo[50];
    snprintf(nomeArquivo, sizeof(nomeArquivo), "instancias/%d", instancia_num);

    // Executa as operações na AVL
    int totalop = lerArquivoAVL(array, nomeArquivo);

    clock_t end = clock();
    tempo += (double)(end - begin) / CLOCKS_PER_SEC;
    return tempo;
}

int main(int argc, char* argv[]) {
    ///////////////////////////////////////////////////////////
    /////////////////// Leitor de instâncias //////////////////
    ///////////////// Não deve ser modificado /////////////////
    ///////////////////////////////////////////////////////////
    int instancia_num = -1;
    instancia_num = atoi(argv[1]);
    if (instancia_num <= 0 || instancia_num > 10) {
        printf("Para executar o código, digite ./arvores x\nonde x é um número entre 1 e 10 que simboliza a instância utilizada\n");
        exit(0);
    }

    // Mede o tempo para a árvore binária não-balanceada
    double tempo_n_balanceada = arvore_binaria(instancia_num);

    // Mede o tempo para a árvore balanceada
    double tempo_balanceada = arvore_balanceada(instancia_num);

    // Imprime os tempos de execução em duas linhas
    printf("%f\n", tempo_n_balanceada); // Tempo BST
    printf("%f\n", tempo_balanceada);   // Tempo AVL

    return 0;
}