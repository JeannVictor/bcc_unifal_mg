#include <stdlib.h>
#include <stdio.h>
#include <time.h>

// Estrutura de Fila Encadeada com Algoritmos de Inserção/Exclusão
typedef struct fila_
{
    char letra;
    struct fila_ *prox;
} fila;

void insere_fila(fila *x, fila **fim, fila **inicio){
    if (*fim != NULL)
        (*(*fim)).prox = x;
    else
        *inicio = x;
    *fim = x;
    (*x).prox = NULL;
}

fila *remove_fila(fila **inicio, fila **fim){
    fila *exclude = NULL;
    if (*inicio != NULL){
        exclude = *inicio;
        *inicio = (*(*inicio)).prox;
        if (*inicio == NULL){
            *fim = NULL;
        }
    }
    return exclude;
}
//############################################################# 
// Estrutura de Pilha e Inserção/Exclusão
typedef struct pilha_ {
    char letra;
    struct pilha_ *prox;
} pilha;

void insere_pilha(pilha *x, pilha **topo) {
    x->prox = *topo;
    *topo = x;
}

pilha *remove_pilha(pilha **topo) {
    pilha *exclude = NULL;
    if (*topo != NULL) {
        exclude = *topo;
        *topo = (*topo)->prox;
    }
    return exclude;
}
//############################################################# 

int main(int argc, char const *argv[])
{
    FILE *arquivo;

    pilha *topoP = NULL;
    fila *inicioF = NULL;
    fila *fimF    = NULL;
    char c;

    arquivo = fopen("palindromos.txt", "r");
    if (arquivo == NULL) {
        perror("Error opening file");
        return 1;
    }

    while (1) {
        topoP = NULL;
        inicioF = fimF = NULL;

        // lê uma linha até \n ou EOF
        while ((c = fgetc(arquivo)) != '\n' && c != EOF) {
            
            pilha *novaPilha = malloc(sizeof(pilha));
            fila *novaFila   = malloc(sizeof(fila));

            novaPilha->letra = c;
            novaFila->letra  = c;

            insere_pilha(novaPilha, &topoP);
            insere_fila(novaFila, &fimF, &inicioF);
        }

        // se não leu nada, sai
        if (topoP == NULL && inicioF == NULL) {
            break;
        }

        // compara pilha e fila
        int ehPalindromo = 1;
        while (inicioF != NULL && topoP != NULL) {
            fila *chrFila = remove_fila(&inicioF,&fimF);
            pilha *chrPilha = remove_pilha(&topoP);

            if (chrFila->letra != chrPilha->letra) {
                ehPalindromo = 0;   
            }
            free(chrFila);
            free(chrPilha);
        }

        printf("%d\n", ehPalindromo);

        if (c == EOF) break; // acabou o arquivo
    }

    fclose(arquivo);
    return 0;
}
