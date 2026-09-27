#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

// Atividade 3: Cena Gráfica
// Autor: Jeann Victor Batista
int main() {
    
    // Variáveis
    float lado1, lado2, lado3, VT = 0, AT = 0;
    char objeto[50];
    FILE *arquivo;

    // Abrindo o arquivo para leitura
    arquivo = fopen("cenagrafica.txt", "r");
    if (arquivo == NULL) {
        printf("Erro: Arquivo não encontrado.\n");
        return 1;
    }

    // Processamento do arquivo
    while (fscanf(arquivo, "%s", objeto) == 1) {
        if (strcmp(objeto, "fim") == 0) {
            break;
        }

        if (strcmp(objeto, "quadrado") == 0) {
            if (fscanf(arquivo, "%f", &lado1) == 1) {
                AT += lado1 * lado1;
            }
        } else if (strcmp(objeto, "retangulo") == 0) {
            if (fscanf(arquivo, "%f %f", &lado1, &lado2) == 2) {
                AT += lado1 * lado2;
            }
        } else if (strcmp(objeto, "triangulo") == 0) {
            if (fscanf(arquivo, "%f %f", &lado1, &lado2) == 2) {
                AT += (lado1 * lado2) / 2;
            }
        } else if (strcmp(objeto, "cubo") == 0) {
            if (fscanf(arquivo, "%f", &lado1) == 1) {
                AT += 6 * lado1 * lado1;
                VT += lado1 * lado1 * lado1;
            }
        } else if (strcmp(objeto, "paralelepipedo") == 0) {
            if (fscanf(arquivo, "%f %f %f", &lado1, &lado2, &lado3) == 3) {
                AT += 2 * ((lado1 * lado2) + (lado1 * lado3) + (lado2 * lado3));
                VT += lado1 * lado2 * lado3;
            }
        } else if (strcmp(objeto, "cilindro") == 0) {
            if (fscanf(arquivo, "%f %f", &lado1, &lado2) == 2) {
                AT += 2 * M_PI * lado1 * (lado1 + lado2);
                VT += M_PI * lado1 * lado1 * lado2;
            }
        } else if (strcmp(objeto, "cone") == 0) {
            if (fscanf(arquivo, "%f %f", &lado1, &lado2) == 2) {
                AT += M_PI * lado1 * (lado1 + lado2);
                VT += (1.0 / 3.0) * M_PI * lado1 * lado1 * lado2;
            }
        } else if (strcmp(objeto, "esfera") == 0) {
            if (fscanf(arquivo, "%f", &lado1) == 1) {
                AT += 4 * M_PI * lado1 * lado1;
                VT += (4.0 / 3.0) * M_PI * lado1 * lado1 * lado1;
            }
        }
    }

    // Exibindo os resultados finais
    printf("A soma das áreas é: %.2f\n", AT);
    printf("A soma dos volumes é: %.2f\n", VT);

    // Fechando o arquivo
    fclose(arquivo);
    return 0;
}
