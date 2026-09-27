#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "p6.h"

// Atividade 6: Operações sobre Matrizes
// Autor: Jeann Victor Batista
// Compilação: gcc -o programa jeann.c funcao.c -Wall

#define TAM 128
typedef int TMatriz[TAM][TAM];

int main()
{
    TMatriz m,n; 
    srand(time(NULL)); 
    // Definição do tamanho da matriz
    int tmp,opcao,la,lb,ca,cb;

    // Obtendo a quantidade linhas e colunas das Matrizes
    printf("Qual será o número de linhas da Matriz A?\n");
    scanf("%d",&la);
    printf("Qual será o número de colunas da Matriz A?\n");
    scanf("%d",&ca);
    printf("Qual será o número de linhas da Matriz B?\n");
    scanf("%d",&lb);
    printf("Qual será o número de colunas da Matriz B?\n");
    scanf("%d",&cb);

    // Criação aleatoria das matrizes.
    criamatriz(m,la,ca);
    imprimirmatriz(m,la,ca);
    printf("\n");
    criamatriz(n,lb,cb);
    imprimirmatriz(n,lb,cb);

    do {
        printf("\nMenu de Opções:\n");
        printf("1. Matriz Transposta\n");
        printf("2. Soma de Matrizes\n");
        printf("3. Multiplicar Matrizes\n");
        printf("4. Média de valores da Matriz \n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);
        getchar(); // Limpa buffer

        switch (opcao) {
            case 1:
                printf("Qual matriz você deseja visualizar a transposta?\n");
                printf("1. Matriz A\n");
                printf("2. Matriz B\n");
                scanf("%d", &tmp);
                if(tmp == 1){
                    printf("A Matriz A transposta será:\n");
                    transposta(m,la,ca);
                }    
                if(tmp == 2){
                    printf("A Matriz B transposta será:\n");
                    transposta(n,lb,cb);
                }         
                break;
            case 2:
                if((la == lb) && (ca == cb)){
                    soma(m,n,la,ca);
                }else
                    printf("Não é póssivel realizar a soma dessas matrizes\n");

                break;
            case 3:
                if(ca == lb){
                    printf("A  matriz resultante da multiplicação das matrizes é:\n");
                    multiplica(m,n,la,ca,lb,cb);
                }else
                    printf("Não é póssivel realizar a multiplicação dessas matrizes\n");         
                break;
            case 4:
                printf("Qual matriz você deseja visualizar a média?\n");
                printf("1. Matriz A\n");
                printf("2. Matriz B\n");
                scanf("%d", &tmp);
                if(tmp == 1){
                    printf("A  média da Matriz A é:\n");
                    media(m,la,ca);
                }
                if(tmp == 2){
                    printf("A média da Matriz B é:\n");
                    media(m,lb,cb);         
                }
                break;
            case 0:
                printf("Saindo...\n");
                break;
            default:
                printf("Opção inválida. Tente novamente.\n");
        }
    } while (opcao != 0);
    return 0;
}