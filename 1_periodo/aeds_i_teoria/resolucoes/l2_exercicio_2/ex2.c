#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Exercício 2: 
// Autor: Jeann Victor Batista

// Função Selection Sort
void selectionSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {

        int min_idx = i;

        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_idx]) 
                min_idx = j;
        }

        int temp = arr[i];
        arr[i] = arr[min_idx];
        arr[min_idx] = temp;
    }
}

// Função para imprimir vetor
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    srand(time(NULL));
    int arr[100];
    int igual = 0,i = 0,k = 0;

    // Gerar vetor aleatorio desordenado
    do{
        arr[i] = rand() %100 ; 
        igual = 0;
        for(int j = 0; j < i ;j ++){
            if(arr[j] == arr[i])
                igual = 1;
        }
        if(igual == 0)
            i++;
    }while(i < 100);

    // Impressão array original
    printArray(arr,100);

    // Descobrir até onde será ordenado
    printf("Até onde você deseja que o vetor seja ordenado? (1 a 100):?\n");
    scanf("%d",&k);

    // Impressão array modificado
    selectionSort(arr,k);
    printArray(arr,100);
  
    return 0;
}
