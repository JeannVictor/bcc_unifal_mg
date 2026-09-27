#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Exercício 10: 
// Autor: Jeann Victor Batista

// Função para soma valores do array.
int somaV(int arr[],int N){
    int soma = 0;
    for(int i = 0;i < N;i++)
        soma += arr[i];

    return soma;    
}

int main(){

    srand(time(NULL));
    int n;
    printf("Você deseja criar um vetor de quantos números?\n");
    scanf("%d",&n);

    // Criação vetor de TAM = n , e com n valores aleatorios
    int arr[n];
    for(int i = 0; i < n;i++){
        arr[i] = rand() %100;
    }

    // Váriavel para receber o retorno da função "somaV"
    int total = somaV(arr,n);

    // Impressão dos resultados
    printf("A soma de todos os valores do vetor é: %d\n",total);

    return 0;
}