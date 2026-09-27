#include <stdlib.h>
#include <stdio.h>
#include <time.h>

typedef struct no_
{
    int valor;
    int chave;  
    struct no_ *prox;
} no;

// Função para verificar se uma chave já existe na fila
int chave_existe(no *inicio, int chave){
    no *atual = inicio;
    while (atual != NULL) {
        if (atual->chave == chave) 
            return 1;
        atual = atual->prox;
    }
    return 0;
}

void insere_fila(no *x, no **fim, no **inicio){
    if (*fim != NULL)
        (*(*fim)).prox = x;
    else
        *inicio = x;
    *fim = x;
    (*x).prox = NULL;
}

no *remove_fila(no **inicio, no **fim){
    no *exclude = NULL;
    if (*inicio != NULL){
        exclude = *inicio;
        *inicio = (*(*inicio)).prox;
        if (*inicio == NULL){
            *fim = NULL;
        }
    }
    return exclude;
}

void print_fila(no *inicio){
    if (inicio == NULL)
        printf("Fila vazia!\n");
    else{
        no *atual = inicio;
        printf("Fila: \n");
        printf("Chave\tValor\n");
        while (atual != NULL){
            printf("%d\t%d\n", atual->chave, atual->valor);
            atual = atual->prox;
        }
        printf("\n");
    }
}

// Função para gerar lista inicial com valores aleatórios
void gerar_lista_inicial(no **inicio, no **fim){
    for (int i = 0; i < 5; i++){
        no *x = malloc(sizeof(no));
        x->valor = rand() % 100;  // Valor aleatório entre 0 e 99
        x->chave = i + 1;        // Chaves iniciais: 1, 2, 3, 4, 5
        insere_fila(x, fim, inicio);
    }
    printf("Lista inicial gerada com 5 elementos aleatórios.\n");
}

int main(){
    no *inicio = NULL;
    no *fim = NULL;
    int opcao = 0;

    // Inicializa gerador de números aleatórios
    srand(time(NULL));
    
    // Gera lista inicial
    gerar_lista_inicial(&inicio, &fim);

    do{
        printf("\n=== MENU DE OPERACOES ===\n");
        printf("1. Inserir elemento\n");
        printf("2. Remover elemento\n");
        printf("3. Imprimir fila\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);

        switch (opcao){
        case 1:
            no *x = malloc(sizeof(no));
            printf("Digite o valor que deseja adicionar: ");
            scanf("%d", &(x->valor));
            
            // Loop para garantir chave única
            do {
                printf("Digite a chave do elemento: ");
                scanf("%d", &(x->chave));
                if (chave_existe(inicio, x->chave)) 
                    printf("Chave já existe! Digite uma chave única.\n");
                else 
                    break;
            } while(1);

            insere_fila(x, &fim, &inicio);
            printf("O elemento foi adicionado com sucesso!\n");
            break;
        
        case 2:
            no *removido = remove_fila(&inicio, &fim);
            if (removido == NULL){
                printf("Elemento Inexistente ou fila vazia!\n\n");
            }
            else{
                printf("O elemento com chave %d e valor %d foi removido com sucesso!\n\n", 
                       removido->chave, removido->valor);
                free(removido);
            }
            break;
        
        case 3:
            print_fila(inicio);
            break;
        
        case 0:
            printf("Encerrando o programa...\n");
            break;

        default:
            printf("Opção inválida! Tente novamente.\n");    
        }
    }while(opcao != 0);

    // Libera a memória antes de encerrar
    while (inicio != NULL) {
        no *temp = inicio;
        inicio = inicio->prox;
        free(temp);
    }
    
    return 0;
}