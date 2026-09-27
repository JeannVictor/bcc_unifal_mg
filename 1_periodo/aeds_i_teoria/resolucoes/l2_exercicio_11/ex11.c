#include <stdio.h>

// Exercício 11: 
// Autor: Jeann Victor Batista

int main() {

    // Criação da váriavel N
    int N = 0;
    // Atribuição de valor a váriavel N
    printf("Digite a quantidade de linhas!:\n");
    scanf("%d", &N);

    // Loop para realizar a parte de cima
    for (int i = 1; i <= 2*N - 1; i += 2) { // Quantidade de linhas a ser impressa
        int spaces = (2*N - i) / 2; // Váriavel para dividir os 

        for(int j = 0;j < spaces ;j++)
            printf(".");
        for(int j = 0; j < i;j ++)
            printf("*");
        for(int j = 0;j < spaces;j++)
            printf(".");
    
        printf("\n");    
    }    

    // Loop para realizar a parte de baixo    
    for (int i = 2*N - 3; i >= 1; i = i - 2) { 
        int spaces = (2*N - i) / 2; 

        for(int j = 0;j < spaces ;j++)
            printf(".");
        for(int j = 0; j < i;j ++)
            printf("*");
        for(int j = 0;j < spaces;j++)
            printf(".");
        
        printf("\n"); 
    }   
        
    return 0;
}