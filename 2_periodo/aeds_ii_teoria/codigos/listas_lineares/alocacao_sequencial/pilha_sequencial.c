#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Algoritmo de Inserção/Remoção em pilhas.

// Struct utilizada
typedef struct no_
{
    int valor;
    int chave;
} no;

// Váriavel Global do Tamanho Vetor
int N = 5;
const int M = 10;

// Função para inserir um novo "no" na pilha
int insere (no L[M],no x){
    if(N - 1 != M){
        N++;
        L[N - 1] = x;
        return N;
    }
    return -1;
}

// Função para remover um "no" da pilha
no *removeNo(no L[M]){
   
    if(N!= 0){
        no *exclude = &L[N - 1];  
        N --;
        return exclude;
    }
    return NULL;
}

// Função para gerar pilha aleatória
void gerarvetor(no L[M]){
    int i = 0,igual;

    // Criação do vetor
    for(int i = 0; i < M ;i++){
        L[i].chave = -1;
        L[i].valor = 0;
    }
    // Valores aleatórios a cada item
    for(int i = 0; i < N ;i++)
        L[i].valor = rand() %100;

    // Criação de chave única    
    do{
        L[i].chave = rand() %100 + 1; 
        igual = 0;
        for(int j = 0; j < i ;j ++){
            if(L[j].chave == L[i].chave)
                igual = 1;
        }
        if(igual == 0)
            i++;
    }while(i < N);
}

// Função para imprimir vetor
void imprimirvetor(no L[M]){
    for(int i = 0; i < N; i++)  // Imprimir apenas até o índice N-1
        printf("Chave:%d  Valor:%d \n", L[i].chave, L[i].valor);
    if (N == 0)
        printf("Pilha vazia.\n");

}

int main() {

    no L[M],novoNo,*removido;
    int opcao, resultado;
    
    // Inicializa gerador de números aleatórios
    srand(time(NULL));
    
    // Gera o vetor inicial
    gerarvetor(L);
    
    do {
        printf("\n=== MENU DE OPERACOES ===\n");
        printf("1. Inserir elemento\n");
        printf("2. Remover elemento\n");
        printf("3. Imprimir pilha\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);
        
        switch(opcao) {
            case 1:
                printf("Digite o valor do novo elemento: ");
                scanf("%d", &novoNo.valor);
                printf("Digite a chave do novo elemento: ");
                scanf("%d", &novoNo.chave);

                int chaveRepetida;
                do {
                    chaveRepetida = 0;
                    for(int i = 0; i < N; i++) {
                        if(novoNo.chave == L[i].chave) {
                            chaveRepetida = 1;
                            printf("Digite um valor de chave que não exista: ");
                            scanf("%d", &novoNo.chave);
                            break;  // Sai do for para reiniciar a verificação
                        }
                    }
                } while(chaveRepetida);

                resultado = insere(L, novoNo);
                if(resultado == -1)
                    printf("Erro: Pilha cheia!\n");
                else
                    printf("Elemento inserido com sucesso! Novo topo: %d\n", resultado);
                
                break;
                
            case 2:
                removido = removeNo(L);
                if(removido == NULL)
                    printf("Erro: Pilha vazia!\n");
                else
                    printf("Elemento removido - Chave: %d, Valor: %d\n", 
                           removido->chave, removido->valor);
                           
                break;
                
            case 3:
                printf("\n=== ESTADO ATUAL DA PILHA ===\n");
                imprimirvetor(L);
                break;
                
            case 0:
                printf("Encerrando o programa...\n");
                break;
                
            default:
                printf("Opção invalida! Tente novamente.\n");
        }
    } while(opcao != 0);
    
    return 0;
}