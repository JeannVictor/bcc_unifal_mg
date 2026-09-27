#include<stdio.h>

//dada uma subarvore, torná-la uma max-heap
void heapify(int arr[], int n, int i){
    int maior = i;

    //filho a esquerda
    int esq = 2 * i + 1;
    //filho a direita
    int dir = 2 * i + 2;

    if(esq < n && arr[esq] > arr[maior]){
        maior = esq;
    }

    if(dir < n && arr[dir] > arr[maior]){
        maior = dir;
    }

    //a raiz não é o maior.
    //preciso trocar a ordem dos nós, 
    //de modo ao maior ir para a raiz
    if(maior != i){
        int temp = arr[i];
        arr[i] = arr[maior];
        arr[maior] = temp;

        //como trocamos os elementos de ordem,
        //preciso garantir que o nó que desceu
        //e que está na posição "maior"
        //é maior do que os seus "novos filhos"

        heapify(arr, n, maior);
    }
}

void heapSort(int arr[], int n){
    //tornar o vetor uma max-heap
    for(int i = n/2 - 1; i >= 0; i--){
        heapify(arr, n, i);
    }

    //mover o maior elemento para o final
    for(int i = n-1; i > 0; i--){
        //movendo o maior elemento
        //para o final da heap
        int temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;

        heapify(arr, i, 0);
    }
}

void printArray(int arr[], int n){
    int i;
    for(i = 0; i < n; i++){
        printf("%4d ", arr[i]);
    }
    printf("\n");
}

int main(){
    int arr[] = {9, 4, 3, 8, 10, 2, 5};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    printf("Original array (size %d): \n", n);
    printArray(arr, n);

    heapSort(arr, n);

    printf("Sorted array: \n");
    printArray(arr, n);
    return 0;
}