#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Algoritmo de Busca1 para aplicação sequencial

// Struct utilizada
typedef struct no_
{
    int valor;
    int chave;
} no;

// Váriavel Global do Tamanho Vetor
const int N = 10;

int busca1(no L[N],int x){
    int i = 0, busca = -1;
    while(i <= N){
        if(L[i].chave == x){
            busca = i;
            i = N + 1;
        }else
            i++;
    }
    return busca;
}

// Função para gerar vetor
void gerarvetor(no L[N]){
    // Váriaveis
    int i = 0,igual;

    // Valores aleatorios a cada item
    for(int i = 0; i < N ;i++)
        L[i].valor = rand() %100;

    // Criação de chave única    
    do{
        L[i].chave = rand() %100 ; 
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
void imprimirvetor(no L[N]){
    for(int i = 0; i < N ;i++)
        printf("Chave:%d  Valor:%d \n",L[i].chave,L[i].valor);
}

int main()
{
    srand(time(NULL));
    
    // Criação de váriaveis
    no L[N];
    int r,busca;

    // Geração do vetor
    gerarvetor(L);
    // Impressão do vetor apenas para teste
    imprimirvetor( L);

    printf("\nQual chave você deseja procurar?\n");
    scanf("%d",&r);

    // Função busca em ação
    busca = busca1(L,r);
    if(busca == -1){
        printf("A chave procurada não existe no vetor\n");
    }else
        printf("A chave: %d existe!E seu valor é: %d\n",r,L[busca].valor);

    return 0;
}
