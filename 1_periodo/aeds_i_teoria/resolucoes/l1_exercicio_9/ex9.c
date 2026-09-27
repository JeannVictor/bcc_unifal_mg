#include <stdio.h>
#include <math.h>

// Exercício 9
// Autor: Jeann Victor Batista

// O exercício em si tinha como propósito calcular os primeiros 20 termos
// Porem não foi possível representar isso

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
    double numerator = 0, resultado = 1,expoente = 2;
    int fatorials = 0,denominator = 2,sinal = -1;

    // Obtenção da váriavel X
    printf("Qual valor de X você quer saber o Cossen?\n");
    scanf("%lf",&numerator);

    // Loop para realização do cálculo
    do{
        fatorials = fatorial(denominator);
        resultado += (sinal * pow(numerator,expoente) / fatorials);
        expoente = expoente + 2;
        denominator += 2;
        sinal = sinal * -1;
    }while (denominator <= 33);

    // Impressão dos Resultados
    printf("o valor de e^x: %f\n", resultado);
    

    return 0;
}