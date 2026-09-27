#include <stdlib.h>
#include <stdio.h>
#include <limits.h>

int HTAM = 1000;

// Funções auxiliares
int pai(int i) {
    return (i - 1) / 2;
}

int fesq(int i) {
    return (2 * i) + 1;
}

int fdir(int i) {
    return (2 * i) + 2;
}

void swap(int *filho, int *pai) {
    int tmp = *filho;
    *filho = *pai;
    *pai = tmp;
}

void insereheap(int *n, int h[HTAM], int k) {
    if (*n == HTAM) {
        printf("Erro: Heap cheia. Não é possível inserir.\n");
        return;
    }
    (*n)++;
    int i = (*n) - 1;
    h[i] = k;

    while (i != 0 && h[pai(i)] > h[i]) {
        swap(&h[i], &h[pai(i)]);
        i = pai(i);
    }
}

void minimizar(int i, int n, int h[HTAM]) {
    int e = fesq(i);
    int d = fdir(i);
    int min = i;

    if (e < n && h[e] < h[i])
        min = e;
    if (d < n && h[d] < h[min])
        min = d;
    if (min != i) {
        swap(&h[i], &h[min]);
        minimizar(min, n, h);
    }
}

int removemin(int *n, int h[HTAM]) {
    if (*n <= 0)
        return INT_MAX;

    if (*n == 1) {
        (*n)--;
        return h[0];
    }

    int raiz = h[0];
    h[0] = h[(*n) - 1];
    (*n)--;
    minimizar(0, *n, h);
    return raiz;
}

void imprimeheap(int n, int h[HTAM]) {
    printf("Heap atual: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", h[i]);
    }
    printf("\n");
}

int main() {
    int h[HTAM];
    int n = 0;
    int opcao, valor;

    do {
        printf("\n=== MENU DE OPERAÇÕES ===\n");
        printf("1. Inserir elemento\n");
        printf("2. Remover elemento mínimo\n");
        printf("3. Imprimir heap\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                printf("Digite o valor a ser inserido: ");
                scanf("%d", &valor);
                insereheap(&n, h, valor);
                break;

            case 2:
                valor = removemin(&n, h);
                if (valor == INT_MAX) {
                    printf("Erro: Heap está vazia.\n");
                } else {
                    printf("Elemento removido: %d\n", valor);
                }
                break;

            case 3:
                printf("\n=== IMPRIMINDO A HEAP ===\n");
                imprimeheap(n, h);
                break;

            case 0:
                printf("Encerrando o programa...\n");
                break;

            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while (opcao != 0);

    return 0;
}
