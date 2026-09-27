#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct no_ {
    int valor;
    int chave;
} no;

// Variáveis Globais
int f = -1, r = -1;
const int M = 10;
no L[10];  // apenas uma declaração global

int insere(no x) {
    int prov = (r + 1) % M;
    if(prov != f) {
        r = prov;
        L[r] = x;
        if(f == -1)
            f = 0;  
        return r;
    }
    return -1;
}

no *removeNo() {
    no *exclude = (no *)malloc(sizeof(no));
    if(f != -1) {
        *exclude = L[f];
        if(f == r)
            f = r = -1;
        else
            f = (f + 1) % M;
        return exclude;
    }
    free(exclude);
    return NULL;
}

void gerarvetor() {
    int i = 0;
    no novo;
    
    f = r = -1;  // reinicializa a fila
    
    while(i < 5) {
        novo.valor = rand() % 100;
        novo.chave = rand() % 100 + 1;
        
        int chaveRepetida = 0;
        // Verifica incluindo o último elemento
        if(f != -1) {
            int j = f;
            do {
                if(L[j].chave == novo.chave) {
                    chaveRepetida = 1;
                    break;
                }
                j = (j + 1) % M;
            } while(j != (r + 1) % M);
        }
        
        if(!chaveRepetida) {
            if(insere(novo) != -1) {
                i++;
            }
        }
    }
}

void imprimirvetor() {
    if(f == -1) {
        printf("Fila vazia.\n");
        return;
    }
    
    int i = f;
    do {
        printf("Chave:%d  Valor:%d \n", L[i].chave, L[i].valor);
        i = (i + 1) % M;
    } while(i != (r + 1) % M);
}

int main() {
    no novoNo, *removido;
    int opcao, resultado;
    
    srand(time(NULL));
    gerarvetor();
    
    do {
        printf("\n=== MENU DE OPERACOES ===\n");
        printf("1. Inserir elemento\n");
        printf("2. Remover elemento\n");
        printf("3. Imprimir fila\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);
        
        switch(opcao) {
            case 1:
                printf("Digite o valor do novo elemento: ");
                scanf("%d", &novoNo.valor);
                printf("Digite a chave do novo elemento: ");
                scanf("%d", &novoNo.chave);

                do {
                    int chaveRepetida = 0;
                    if(f != -1) {
                        int i = f;
                        do {
                            if(L[i].chave == novoNo.chave) {
                                chaveRepetida = 1;
                                printf("Digite um valor de chave que não exista: ");
                                scanf("%d", &novoNo.chave);
                                break;
                            }
                            i = (i + 1) % M;
                        } while(i != (r + 1) % M);
                    }
                    if(!chaveRepetida) break;
                } while(1);

                resultado = insere(novoNo);
                if(resultado == -1)
                    printf("Erro: Fila cheia!\n");
                else
                    printf("Elemento inserido com sucesso!\n");
                break;
                
            case 2:
                removido = removeNo();
                if(removido == NULL)
                    printf("Erro: Fila vazia!\n");
                else {
                    printf("Elemento removido - Chave: %d, Valor: %d\n", 
                           removido->chave, removido->valor);
                    free(removido);
                }
                break;
                
            case 3:
                printf("\n=== ESTADO ATUAL DA FILA ===\n");
                imprimirvetor();
                break;
                
            case 0:
                printf("Encerrando o programa...\n");
                break;
                
            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while(opcao != 0);
    
    return 0;
}