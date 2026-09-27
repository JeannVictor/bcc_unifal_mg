#include <stdio.h>

int main(){
    int board[6][6] = {
        {9,5,7,5,3,4},
        {0,2,6,4,2,5},
        {4,1,2,4,6,2},
        {2,3,6,3,0,0},
        {7,8,3,4,5,4},
        {0,5,2,9,8,7},
    };

    // Inicializando histograma com zeros
    int histograma[10];
    for(int i = 0; i < 10; i++){
        histograma[i] = 0;
    }
    
    // Contando a frequência de cada nível de cinza
    for(int i = 0; i < 6; i++){
        for(int j = 0;j < 6;j++){
            histograma[board[i][j]] = histograma[board[i][j]] + 1;
        }
    }

    printf("Histograma com 10 níveis de cinza:\n");
    printf("[");
    // Imprimindo o histograma
    for(int i = 0; i < 10; i++){
        if(i == 9){
            printf("%d", histograma[i]);
        }else{  
            printf("%d,", histograma[i]);
        }  
    }
    printf("]\n");
}