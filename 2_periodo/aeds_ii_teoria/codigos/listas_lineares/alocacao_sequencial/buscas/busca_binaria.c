#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Algoritmo de Busca em vetores ordenados para aplicação sequencial

// Struct utilizada
typedef struct no_
{
    int valor;
    int chave;
} no;

// Váriavel Global do Tamanho Vetor
const int N = 10;

int buscabin(no L[N],int x){
    // Váriaveis
    int inf = 0,sup = N,meio, busca = -1;

    while(inf <= sup){
        meio = (inf + sup)/2;
        if(L[meio].chave == x){
            busca = meio;
            inf = sup + 1;
        }else if(L[meio].chave < x){
            inf = meio + 1;
        }else
            sup = meio - 1;
    }
    return busca;
}
// Método de ordenação de vetor
void bubblesort(no L[N]){
    int tmp;
    for(int i = 0; i < N-1;i++){
        for (int j = 0; j < N - i - 1; j++){
            if(L[j].chave > L[j+1].chave){
                tmp = L[j + 1].chave;
                L[j + 1].chave = L[j].chave;
                L[j].chave = tmp;
            }    
        }
    }
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
    imprimirvetor(L);

    printf("\n");

    // Ordenação do vetor
    bubblesort(L);
    imprimirvetor(L);

    printf("\nQual chave você deseja procurar?\n");
    scanf("%d",&r);

    // Função busca em ação
    busca = buscabin(L,r);
    if(busca == -1){
        printf("A chave procurada não existe no vetor\n");
    }else
        printf("A chave: %d existe!E seu valor é: %d\n",r,L[busca].valor);

    return 0;
}