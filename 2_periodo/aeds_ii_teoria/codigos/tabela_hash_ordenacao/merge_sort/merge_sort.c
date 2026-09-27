#include<stdio.h>
#include <stdbool.h>

void merge(int arr[], int l, int m, int r){
    
    int dimL = m-l+1;
    int dimR = r -m;
    int L[dimL], R[dimR];

    int i, j, k;
    for(i = 0; i < dimL; i++){
        L[i] = arr[l+i];
    }
    for(j = 0; j < dimR; j++){
        R[j] = arr[m+1+j];
    }

    i = 0; j = 0, k = l;
    while(i < dimL && j < dimR){
        if(L[i] <= R[j]){
            arr[k] = L[i];
            i++;
        }else{
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while(i < dimL){
        arr[k] = L[i];
        i++;
        k++;
    }

    while(j < dimR){
        arr[k] = R[j];
        j++;
        k++;
    }
}

void mergeSort(int arr[], int l, int r){
    if (l < r) {
        int m = l + (r - l) / 2;

        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);

        merge(arr, l, m, r);
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
    int arr[] = { 66, 30, 27, 13, 25, 10 };
    int n = sizeof(arr) / sizeof(arr[0]);
    
    printf("Original array (size %d): \n", n);
    printArray(arr, n);

    mergeSort(arr, 0, n - 1);

    printf("Sorted array: \n");
    printArray(arr, n);
    return 0;
}