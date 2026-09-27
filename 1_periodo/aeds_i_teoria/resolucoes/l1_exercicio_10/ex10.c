#include <stdio.h>
#include <math.h>

// Exercício 10
// Autor: Jeann Victor Batista

int main()
{
    unsigned long long resultado = 0;  // Usando unsigned long long para evitar overflow

    // Calculando a soma das potências de 2 de 2^0 até 2^63
    for(int i = 0; i < 64; i++){  
        resultado += (1LL << i);  // O uso do pow não funcinou. Por isso do deslocamento.
    }

    // Impressão do resultado
    printf("O total de grãos é: %llu\n", resultado);  

    return 0;
}

