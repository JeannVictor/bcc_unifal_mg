#include <stdio.h>
#include <stdlib.h>
#define TAM 5

// Nó do vetor, possui campos para valor e frequência
typedef struct nov_ {
    int valor;
    int freq;
} nov;

// Nó da árvore, possui campos para valor, partilha e os dois ponteiros
typedef struct noa_ {
    int valor;
    int partilha;
    struct noa_ *esq, *dir;
} noa;

// Constrói a árvore a partir de um vetor ordenado com campos de valor e frequência
noa* construcao(nov v[], int inf, int sup) {
    noa* raiz = malloc(sizeof(noa)); // Espaço reservado para a raiz da árvore/subárvore 

    if (inf != sup) { // Se houver mais de um nó no intervalo
        int max = inf; // Índice do valor de maior frequência 

        for (int i = inf; i <= sup; i++) // Busca frequência máxima no intervalo
            if (v[i].freq > v[max].freq)
                max = i;

        raiz->valor = v[max].valor; // Valor da raiz é o de maior frequência

        // "Apaga" o nó usado movendo os valores subsequentes
        for (int i = max; i < sup; i++)
            v[i] = v[i + 1];
        sup--;

        int mid = (inf + sup) / 2; // Determina o ponto médio
        raiz->partilha = v[mid].valor; // Define a partilha como o valor do meio

        // Construção recursiva das subárvores esquerda e direita
        raiz->esq = construcao(v, inf, mid);
        raiz->dir = construcao(v, mid + 1, sup);
    } else { // Caso base: apenas um nó no intervalo
        raiz->valor = v[inf].valor;
        raiz->partilha = -1; // Partilha inválida
        raiz->esq = NULL;
        raiz->dir = NULL;
    }

    return raiz;
}

// Printa a árvore em formato de árvore
void printa(noa *raiz, int altura) {
    if (!raiz)
        return;

    printa(raiz->dir, altura + 1);

    for (int i = 0; i < altura; i++)
        printf("   ");

    printf("%d|%d\n", raiz->valor, raiz->partilha);

    printa(raiz->esq, altura + 1);
}

// Libera a memória alocada para a árvore
void liberaArvore(noa *raiz) {
    if (!raiz)
        return;
    liberaArvore(raiz->esq);
    liberaArvore(raiz->dir);
    free(raiz);
}

int main() {
    nov vet[TAM];
    noa *raiz = NULL;
    int opcao, n = 0;

    do {
        printf("\n=== MENU DE OPERAÇÕES ===\n");
        printf("1. Inserir valores no vetor\n");
        printf("2. Construir a árvore\n");
        printf("3. Imprimir a árvore\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                if (n > 0) {
                    printf("O vetor já foi preenchido. Reinicie o programa para redefinir os valores.\n");
                } else {
                    printf("Digite o número de elementos (máx %d): ", TAM);
                    scanf("%d", &n);
                    if (n > TAM || n <= 0) {
                        printf("Número inválido de elementos!\n");
                        n = 0;
                        break;
                    }
                    for (int i = 0; i < n; i++) {
                        printf("Digite o valor e a frequência do elemento %d: ", i + 1);
                        scanf("%d %d", &vet[i].valor, &vet[i].freq);
                    }
                    printf("Vetor preenchido com sucesso!\n");
                }
                break;

            case 2:
                if (n == 0) {
                    printf("Erro: O vetor ainda não foi preenchido.\n");
                } else if (raiz) {
                    printf("A árvore já foi construída.\n");
                } else {
                    raiz = construcao(vet, 0, n - 1);
                    printf("Árvore construída com sucesso!\n");
                }
                break;

            case 3:
                if (!raiz) {
                    printf("Erro: A árvore ainda não foi construída.\n");
                } else {
                    printf("\n=== IMPRIMINDO A ÁRVORE ===\n");
                    printa(raiz, 0);
                }
                break;

            case 0:
                printf("Encerrando o programa...\n");
                break;

            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while (opcao != 0);

    // Libera a memória alocada antes de encerrar o programa
    if (raiz) {
        liberaArvore(raiz);
    }

    return 0;
}
