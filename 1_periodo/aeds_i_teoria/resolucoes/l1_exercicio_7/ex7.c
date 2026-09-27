#include <stdio.h>
#include <math.h>

// Exercício 7
// Autor: Jeann Victor Batista

// Função para calcular o fatorial.
int fatorial(int x){
    int resultado = 1;
    while(x >= 1){
        resultado = resultado * x;
        x--;
    }
     return resultado;
}

int main()
{
    // Criação das variáveis
    float numerator = 61, denominator = 1,resultado = 63,termoatual = 0;
    int fatorials = 0,termos = 0;

    // Loop para realização do cálculo
    do{
        fatorials = fatorial(denominator);
        termoatual = numerator / fatorials;
        termos++;
        resultado += termoatual;
        numerator -= 2;
        denominator++;
    }while (termoatual > 0.0000001);

    // Impressão dos Resultados
    printf("Resultado: %.7f\n", resultado);
    printf("Quantidade de termos %d\n",termos);

    return 0;
}