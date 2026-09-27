#include <stdio.h>
#include <math.h>

// Exercício 6
// Autor: Jeann Victor Batista

int main()
{
    // Criação das variáveis
    float base = 2, denominator = 50, exponent = 1, numerator = 0, resultado = 0;

    // Loop para realização do cálculo
    while (denominator > 0) // Evita divisão por zero
    {
        numerator = pow(base, exponent);
        resultado += numerator / denominator;
        exponent++;
        denominator--;
    }

    // Impressão dos Resultados
    printf("Resultado: %.2f\n", resultado);

    return 0;
}
