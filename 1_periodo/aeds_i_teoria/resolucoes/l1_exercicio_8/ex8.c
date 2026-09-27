#include <stdio.h>
#include <math.h>

// Exercício 8
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
    double numerator = 0, denominator = 0,resultado = 0,termoatual = 0,expoente = 0;;
    int fatorials = 0,termos = 0;

    // Obtenção da váriavel X
    printf("Qual valor de X você quer testar na serie?\n");
    scanf("%lf",&numerator);

    // Loop para realização do cálculo
    do{
        fatorials = fatorial(denominator);
        termoatual = pow(numerator,expoente) / fatorials;
        resultado += termoatual;
        termos++;
        expoente++;
        denominator++;
    }while (termoatual > 0.00001);

    // Impressão dos Resultados
    printf("o valor de e^x: %.5f\n", resultado);
    printf("Quantidade de termos %d\n",termos);

    return 0;
}