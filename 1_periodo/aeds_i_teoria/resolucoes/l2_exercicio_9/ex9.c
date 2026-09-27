#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Exercício 9: 
// Autor: Jeann Victor Batista

// Função para transformar dados em segundos
int maior(int a,int b,int c){
    int maior = a;

    if(b > maior)
        maior = b;
    if(c > maior)
        maior = c;
    
    return maior;
}

int main(){

    // Criação de váriaveis
    int a = 0,b = 0,c = 0;

    // Obtendo valor das váriaveis
    printf("Qual o valor de a?\n");
    scanf("%d",&a);
    printf("Qual o valor de b?\n");
    scanf("%d",&b);
    printf("Qual o valor de c?\n");
    scanf("%d",&c);

    // Váriavel para receber o retorno da função "maior"
    int resultado = maior(a,b,c);

    // Impressão dos resultados
    printf("O maior valor é: %d\n",resultado);

    return 0;
}