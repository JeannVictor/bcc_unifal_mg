#include <stdio.h>
#include <stdlib.h>

// Atividade 1: Criando condições
// Autor: Jeann Victor Batista

int main()
{
    // Criação das variáveis.
    int x, y, z;

    // Valores dos lados determinados pelo usuário.
    printf("Digite o valor do 1° lado:\n");
    scanf("%d", &x);
    while (x <= 0) {
        printf("Digite um valor maior que zero.\n");
        scanf("%d", &x);
    }

    printf("Digite o valor do 2° lado:\n");
    scanf("%d", &y);
    while (y <= 0) {
        printf("Digite um valor maior que zero.\n");
        scanf("%d", &y);
    }

    printf("Digite o valor do 3° lado:\n");
    scanf("%d", &z);
    while (z <= 0) {
        printf("Digite um valor maior que zero.\n");
        scanf("%d", &z);
    }

    // Verificando se o triângulo existe.
    if ((x + y) > z && (x + z) > y && (y + z) > x) {

        // Verificação se é  triângulo retângulo.
        if (((x * x) + (y * y) == (z * z) ||
             ((y * y) + (z * z) == (x * x)) ||
             (x * x) + (z * z) == (y * y))) {
            printf("Este triângulo é retângulo.\n");
        }

        // Verificação do tipo do triângulo.
        if (x == y && y == z) {
            printf("Este triângulo é equilátero.\n");
        } else if (x == y || x == z || y == z) {
            printf("Este triângulo é isósceles.\n");
        } else {
            printf("Este triângulo é escaleno.\n");
        }
    } else {
        printf("Os lados não formam um triângulo.\n");
    }

    return 0;
}


