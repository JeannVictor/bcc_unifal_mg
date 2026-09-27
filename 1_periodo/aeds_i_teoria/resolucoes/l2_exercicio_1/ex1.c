#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Exercício 1: 
// Autor: Jeann Victor Batista

int main()
{ 
    srand(time(NULL));
    
    // Criação de váriaveis
    int i = 0,arr[50],igual = 0,maior = -1,menor = 101;
    float media = 0;
    int abaixo = 0,acima = 0;

    // Loop para criação de números aleatorios sem repetição.
    do{
        arr[i] = rand() %100 + 1; 
        igual = 0;
        for(int j = 0; j < i ;j ++){
            if(arr[j] == arr[i])
                igual = 1;
        }
        if(igual == 0)
            i++;
    }while(i < 50);

    // Loop para obter o maior/menor valor do vetor.    
    for(int i = 0;i < 50;i++){
        media += arr[i];
        if(arr[i] >maior)
            maior = arr[i];
        if(arr[i] < menor)
            menor = arr[i];    
    }

    // Cálculo da média
    media = media/50;

    // Loop para obter qtd de valores acima/abaixo da média.
    for(int i = 0;i < 50;i++){
        if(arr[i] >= media){
            acima++;
        }else{
            abaixo++;
        }
    }

    // Impressão dos resultados
    printf("O maior valor encontrado no vetor foi:%d\n",maior);
    printf("O menor valor encontrado no vetor foi:%d\n",menor);
    printf("A média dos valores do vetor foi:%.2f\n",media);
    printf("A quantidade de valores acima da média foi:%d\n",acima);
    printf("A quantidade de valores abaixo da média foi:%d\n",abaixo);

    return 0;
               
    }

    
       