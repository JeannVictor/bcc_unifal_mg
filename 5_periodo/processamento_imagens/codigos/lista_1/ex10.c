#include <stdio.h>

float value(float i){
    float f0 = 0;
    float f2 = 5;
    float f4 = 6;
    float f7 = 7;
    
    if(i >= 0 && i <= 2){
        float m = (f2 - f0)/(2 - 0);
        return f0 + m*(i - 0);
    }else if(i > 2 && i <= 4){
        float m = (f4 - f2)/(4 - 2);
        return f2 + m*(i - 2);
    }else if(i > 4 && i <= 7){
        float m = (f7 - f4)/(7 - 4);
        return f4 + m*(i - 4);
    }
    return i; 
}

void printBoard(float board[8][8]){
    printf("Matriz 8x8:\n");
    for(int i = 0; i < 8; i++){
        for(int j = 0; j < 8; j++){
            printf("%2.2f ", board[i][j]);
        }
        printf("\n");
    }
}

int main(){
    float board[8][8] = {
        {7,1,4,7,6,3,4,6},
        {7,1,7,1,0,1,6,3},
        {4,5,2,4,1,1,7,5},
        {6,0,2,3,7,0,0,7},
        {1,0,5,1,3,1,2,1},
        {7,4,1,1,2,1,4,5},
        {2,6,4,5,1,2,7,2},
        {5,7,3,5,0,4,2,3}
    };

    float transformacao[8];

    printf("Matriz original:\n");
    printBoard(board);
    
    for(int i = 0; i < 8; i++){
        for(int j = 0; j < 8; j++){
            board[i][j] = value(board[i][j]);
        }
    }
    
    printf("\nMatriz após transformação:\n");
    printBoard(board);

    printf("\nVetor de transformação:\n");
    printf("[");
    for(int i = 0; i < 8; i++){
        transformacao[i] = value(i);
        printf("%2.2f,", transformacao[i]);
    }
    printf("]\n");
}