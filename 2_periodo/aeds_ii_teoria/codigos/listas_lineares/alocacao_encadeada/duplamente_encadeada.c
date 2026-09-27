#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct no_
{
    int chave;
    int valor;
    struct no_ *ant;
    struct no_ *prox;
} no;

no *buscar(no *ptlista, int x)
{
    no *ultimo = ptlista->ant;
    if (ultimo != ptlista && x <= ultimo->chave)
    {
        no *pont = ptlista->prox;
        while (pont->chave < x)
        {
            pont = pont->prox;
        }
        return pont;
    }
    return ptlista;
}

no *inserir(no *ptlista, no *novo_no)
{
    no *pont = buscar(ptlista, novo_no->chave);
    if (pont == ptlista || pont->chave != novo_no->chave) {
        no *anterior = pont->ant;
        novo_no->ant = anterior;
        novo_no->prox = anterior->prox;
        anterior->prox = novo_no;
        pont->ant = novo_no;
        return NULL;
    }
    return pont;
}

no *remover(no *ptlista, int x)
{
    no *pont = buscar(ptlista, x);
    if (pont != ptlista && pont->chave == x) {
        no *anterior = pont->ant;
        no *proximo = pont->prox;
        anterior->prox = proximo;
        proximo->ant = anterior;
        return pont;
    }
    return NULL;
}

// Função para imprimir a lista
void imprimir_lista(no *ptlista)
{
    if (ptlista->prox == ptlista)
    {
        printf("Lista vazia!\n");
        return;
    }
    
    no *atual = ptlista->prox;
    printf("\nLista atual:\n");
    printf("Chave\tValor\n");
    while (atual != ptlista)
    {
        printf("%d\t%d\n", atual->chave, atual->valor);
        atual = atual->prox;
    }
}

// Função para gerar lista inicial com valores aleatórios
void gerar_lista_inicial(no *ptlista)
{
    for (int i = 0; i < 5; i++)
    {
        no *novo = malloc(sizeof(no));
        novo->valor = rand() % 100;  // Valor aleatório entre 0 e 99
        novo->chave = i + 1;        // Chaves iniciais: 1, 2, 3, 4, 5
        
        if (inserir(ptlista, novo) != NULL) {
            free(novo);
            printf("Erro ao inserir elemento inicial %d\n", i+1);
        }
    }
    printf("Lista inicial gerada com 5 elementos aleatórios.\n");
}

// Função para inicializar a lista circular
no *inicializar_lista()
{
    no *ptlista = malloc(sizeof(no));
    ptlista->prox = ptlista;
    ptlista->ant = ptlista;
    return ptlista;
}

int main()
{
    no *ptlista = inicializar_lista();
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
                printf("Digite a chave do novo elemento: ");
                scanf("%d", &novo->chave);
                
                if(inserir(ptlista, novo) != NULL) {
                    printf("Erro: chave já existe!\n");
                    free(novo);
                } else {
                    printf("Elemento inserido com sucesso!\n");
                }
                break;
            }
            case 2: {
                int chave;
                printf("Digite a chave do elemento a ser removido: ");
                scanf("%d", &chave);
                no *removido = remover(ptlista, chave);
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
    while(atual != ptlista) {
        no *temp = atual;
        atual = atual->prox;
        free(temp);
    }
    free(ptlista);
    
    return 0;
}







