#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Exercício 3: 
// Autor: Jeann Victor Batista

int main()
{ 
    srand(time(NULL));
    int arr[100][100],n = 0;

    printf("Qual o valor de N para a matriz quadratica NxN?\n");
    scanf("%d",&n);
    printf("\n");
    
    // Criação da matriz original
    for(int i = 0;i < n;i++){
        for(int j = 0;j < n;j++){
            arr[i][j] = rand() %100 + 1;
        }
    }

    // Impressão matriz original
    for(int i = 0;i < n;i++){
        for(int j = 0;j < n;j++)
            printf("%d ",arr[i][j]);
        printf("\n");
    }

    printf("\n");

    // Transposição da matriz
    for(int i = 0;i < n;i++){
        for(int j = 0;j < n;j++){
            int temp = arr[i][j];
            arr[i][j] = arr[j][i];
            arr[j][i] = temp;
        }
    }

    // Impressão Matriz transposta
    for(int i = 0;i < n;i++){
        for(int j = 0;j < n;j++)
            printf("%d ",arr[j][i]);
        printf("\n");
    }

    return 0;
           
    }