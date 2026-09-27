#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Algoritmo de Busca/Inserção/Remoção em aplicação sequencial.

// Struct utilizada
typedef struct no_
{
    int valor;
    int chave;
} no;

// Váriavel Global do Tamanho Vetor
int N = 10;
const int M = 15;

// Função para realizar a busca de um elemento.
int busca(no L[M],int x){
// Percorre o vetor de 0 até N-1
    for (int i = 0; i < N; i++) {
        if (L[i].chave == x)
            return i; // Retorna o índice onde a chave foi encontrada
    }
    return -1; // Retorna -1 se a chave não foi encontrada
}

// Função para inserir um novo "no" no vetor
int insere (no L[M],no x){
    if (N < M){
        if (busca(L,x.chave) == -1){
            L[N] = x;
            N++;
            return N; // Retorna posição 
        }else
            return 0; // 0 = Elemento já existente
    }else
        return -1; // -1 = Lista cheia
}

// Função para remover um "no" do vetor
no *removeseq(no L[M],int x){
    int indice;
    no *exclude = NULL;
    if (N != 0){
        indice = busca(L,x);
        if (indice != -1){
            exclude = malloc(sizeof(no));
            *exclude = L[indice];
            for (int i = indice; i < N - 1; i++)
                L[i] = L[i + 1];
            N--;
        }
    }
    return exclude;
}

// Função para gerar vetor
void gerarvetor(no L[M]){
    int i = 0,igual;

    // Criação do vetor
    for(int i = 0; i < M ;i++){
        L[i].chave = -1;
        L[i].valor = 0;
    }
    // Valores aleatorios a cada item
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
    for(int i = 0; i < M ;i++)
        printf("Chave:%d  Valor:%d \n",L[i].chave,L[i].valor);
}

int main()
{
    srand(time(NULL));
    
    // Criação de váriaveis
    no L[M];
    int e,valor;
    no r;

    // Geração do vetor

    gerarvetor(L);
    // Impressão do vetor apenas para teste
    imprimirvetor( L);

    do{
        printf("\nMenu:\n");
        printf("1. Adicionar chave\n");
        printf("2. Remover chave\n");
        printf("0. Para sair do programa\n");
        scanf("%d",&e);

        switch (e){
            case 1:
                printf("\nDigite a chave e o valor do novo elemento:\n");
                scanf("%d %d", &r.chave, &r.valor);
                valor = insere(L, r);
                if(valor == 0){
                    printf("A chave que deseja adicionar já existe!");
                }else if(valor == -1){
                    printf("O vetor está cheio!");
                }else if(valor != 0 && valor != -1 )
                    printf("A chave foi adicionada com sucesso!");
                
                break;
            case 2:
                printf("\nQual chave você deseja remover do vetor?\n");
                int chave_remover;
                scanf("%d", &chave_remover);
                no *removido = removeseq(L, chave_remover);
                if (removido != NULL) {
                    printf("Chave %d removida com sucesso.\n", removido->chave);
                    free(removido);
                } else {
                    printf("Chave não encontrada.\n");
                }

                break;
            case 0:
                printf("Encerrando o programa...\n");
                break;

            default:
                printf("Opção inválida. Tente novamente.\n");
                break;
            }
    }while(e != 0);
    imprimirvetor(L);
   
    return 0;
}