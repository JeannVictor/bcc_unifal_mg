#include <stdlib.h>
#include <stdio.h>
#include <time.h>

typedef struct no_ {
    int chave;  // Chave única
    int valor;  // Pode repetir
    struct no_ *prox;
} no;

// Função para verificar se uma chave já existe na pilha
int chave_existe(no *topo, int chave) {
    no *atual = topo;
    while (atual != NULL) {
        if (atual->chave == chave)
            return 1;
        atual = atual->prox;
    }
    return 0;
}

void inserep_enc(no *x, no **topo) {
    x->prox = *topo;
    *topo = x;
}

no *remove_pilha(no **topo) {
    no *exclude = NULL;
    if (*topo != NULL) {
        exclude = *topo;
        *topo = (*topo)->prox;
    }
    return exclude;
}

void printa_pilha(no *topo) {
    if (topo == NULL) {
        printf("Pilha vazia!\n");
        return;
    }
    
    no *atual = topo;
    printf("\n=== ELEMENTOS DA PILHA ===\n");
    printf("Topo -> ");
    while (atual != NULL) {
        printf("[Chave: %d, Valor: %d] ", atual->chave, atual->valor);
        if (atual->prox != NULL) 
            printf("-> ");
        atual = atual->prox;
    }
    printf("\n");
}

void gerar_pilha_inicial(no **topo) {
    for(int i = 0; i < 5; i++) {
        no *novo = malloc(sizeof(no));
        // Gera chave única
        do {
            novo->chave = rand() % 100 + 1;  // Chaves de 1 a 100
        } while (chave_existe(*topo, novo->chave));
        
        novo->valor = rand() % 100;  // Valores podem repetir
        inserep_enc(novo, topo);
    }
    printf("Pilha inicial gerada com sucesso!\n");
}

int main() {
    no *topo = NULL;
    int opcao;
    
    srand(time(NULL));
    gerar_pilha_inicial(&topo);
    
    do {
        printf("\n=== MENU DE OPERACOES ===\n");
        printf("1. Inserir elemento\n");
        printf("2. Remover elemento\n");
        printf("3. Imprimir pilha\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);
        
        switch(opcao) {
            case 1: {
                no *novo = malloc(sizeof(no));
                
                // Lê e verifica chave única
                do {
                    printf("Digite a chave (número inteiro positivo): ");
                    scanf("%d", &novo->chave);
                    
                    if (chave_existe(topo, novo->chave)) {
                        printf("Erro: Chave já existe! Tente outra chave.\n");
                    } else if (novo->chave <= 0) {
                        printf("Erro: A chave deve ser positiva!\n");
                    } else {
                        break;
                    }
                } while (1);
                
                printf("Digite o valor: ");
                scanf("%d", &novo->valor);
                
                inserep_enc(novo, &topo);
                printf("Elemento inserido com sucesso!\n");
                break;
            }
            
            case 2: {
                no *removido = remove_pilha(&topo);
                if(removido == NULL) {
                    printf("Erro: Pilha vazia!\n");
                } else {
                    printf("Elemento removido - Chave: %d, Valor: %d\n", 
                           removido->chave, removido->valor);
                    free(removido);
                }
                break;
            }
            
            case 3:
                printa_pilha(topo);
                break;
                
            case 0:
                printf("Encerrando o programa...\n");
                break;
                
            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while(opcao != 0);
    
    // Libera memória
    while(topo != NULL) {
        no *temp = topo;
        topo = topo->prox;
        free(temp);
    }
    
    return 0;
}