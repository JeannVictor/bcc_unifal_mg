#include <stdio.h>
#include <string.h>

// Exercício 5
// Autor: Jeann Victor Batista

int main()
{
    //Criação váriaveis
    float numerator = 1,denominator = 1,resultado = 0;

    // Loop para realização do cálculo
    while (denominator <= 50)
    {
        resultado = numerator/denominator + resultado;
        numerator = numerator + 2;
        denominator++;
    }

    // Impressão dos Resultados
    printf("Resultado: %f\n",resultado);
    
    
    return 0;
}
