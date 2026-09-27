#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct listaenc {
    int chave;
    int valor;
    struct listaenc *prox;
} no;

void busca_enc(int x, no **ant, no **pont, no *ptlista) {
    *ant = ptlista;
    *pont = NULL;
    no *ptr = ptlista->prox;
    while (ptr != NULL) {
        if (ptr->chave < x) {
            *ant = ptr;
            ptr = ptr->prox;
        } else {
            if (ptr->chave == x) {
                *pont = ptr;
            }
            ptr = NULL;
        }
    }
}

int insere_enc(no *y, no *ptlista) {
    no *ant;
    no *pont;
    busca_enc(y->chave, &ant, &pont, ptlista);
    if (pont == NULL) {
        y->prox = ant->prox;
        ant->prox = y;
        return 0;
    }
    return -1;
}

no *remove_enc(int y, no *ptlista) {
    no *ant;
    no *pont;
    busca_enc(y, &ant, &pont, ptlista);
    if (pont != NULL) {
        ant->prox = pont->prox;
        return pont;
    }
    return NULL;
}

void imprimir_lista(no *ptlista) {
    no *ptr = ptlista->prox;
    if (ptr == NULL) {
        printf("A lista está vazia.\n");
    } else {
        printf("\n=== ELEMENTOS DA LISTA ===\n");
        while (ptr != NULL) {
            printf("Chave: %d, Valor: %d\n", ptr->chave, ptr->valor);
            ptr = ptr->prox;
        }
        printf("\n");
    }
}

void gerar_lista_inicial(no *ptlista) {
    int i;
    for(i = 0; i < 5; i++) {
        no *novo = malloc(sizeof(no));
        do {
            novo->chave = rand() % 100 + 1;
            no *ant, *pont;
            busca_enc(novo->chave, &ant, &pont, ptlista);
            if(pont == NULL) { 
                novo->valor = rand() % 100;
                insere_enc(novo, ptlista);
                break;
            }
        } while(1);
    }
    printf("Lista inicial gerada com sucesso!\n");
}

int main() {
    no *ptlista = malloc(sizeof(no));
    ptlista->prox = NULL;
    int opcao;
    
    // Inicializa gerador de números aleatórios
    srand(time(NULL));
    
    // Gera lista inicial
    gerar_lista_inicial(ptlista);
    
    do {
        printf("\n=== MENU DE OPERACOES ===\n");
        printf("1. Inserir elemento\n");
        printf("2. Remover elemento\n");
        printf("3. Imprimir lista\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);
        
        switch(opcao) {
            case 1: {
                no *novo = malloc(sizeof(no));
                printf("Digite o valor do novo elemento: ");
                scanf("%d", &novo->valor);
                
                do {
                    printf("Digite a chave do novo elemento: ");
                    scanf("%d", &novo->chave);
                    
                    no *ant, *pont;
                    busca_enc(novo->chave, &ant, &pont, ptlista);
                    
                    if(pont != NULL) {
                        printf("Chave já existe! Digite uma chave única.\n");
                    } else {
                        break;
                    }
                } while(1);
                
                if(insere_enc(novo, ptlista) == 0) {
                    printf("Elemento inserido com sucesso!\n");
                } else {
                    printf("Erro ao inserir elemento!\n");
                    free(novo);
                }
                break;
            }
            
            case 2: {
                int chave;
                printf("Digite a chave do elemento a ser removido: ");
                scanf("%d", &chave);
                
                no *removido = remove_enc(chave, ptlista);
                if(removido == NULL) {
                    printf("Elemento não encontrado!\n");
                } else {
                    printf("Elemento removido - Chave: %d, Valor: %d\n", 
                           removido->chave, removido->valor);
                    free(removido);
                }
                break;
            }
            
            case 3:
                imprimir_lista(ptlista);
                break;
                
            case 0:
                printf("Encerrando o programa...\n");
                break;
                
            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while(opcao != 0);
    
    // Libera memória da lista antes de encerrar
    no *atual = ptlista->prox;
    while(atual != NULL) {
        no *temp = atual;
        atual = atual->prox;
        free(temp);
    }
    free(ptlista);
    
    return 0;
}