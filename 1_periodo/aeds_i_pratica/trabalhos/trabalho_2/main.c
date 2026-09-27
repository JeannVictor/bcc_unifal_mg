#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "tp3.h"

int main() {
    int opcao, fator;
    PGMImage image;

    srand(time(NULL));

    // Carregar a imagem de entrada
    if (!lerPGM("edit.pgm", &image)) {
        printf("Erro ao carregar a imagem edit.pgm.\n");
        return 1;
    }
    printf("Imagem edit.pgm carregada com sucesso!\n");

    // Menu de opções
    do {
        printf("\nMenu de Opções:\n");
        printf("1. Escurecer ou clarear a imagem\n");
        printf("2. Encontrar a imagem negativa\n");
        printf("3. Binarizar a imagem\n");
        printf("4. Iconizar a imagem\n");
        printf("5. Criar ruídos na imagem\n");
        printf("6. Suavização da imagem\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                printf("Qual é o fator que você deseja aplicar na imagem? (1 para clarear, 0 para escurecer): ");
                scanf("%d", &fator);
                claridade(&image, fator);
                printf("O fator foi aplicado com sucesso!\n");
                break;

            case 2:
                negativo(&image);
                printf("A imagem negativa foi gerada com sucesso!\n");
                break;

            case 3:
                printf("Qual é o fator de limiar para a binarização da imagem? ");
                scanf("%d", &fator);
                binarizar(&image, fator);
                printf("A binarização foi realizada com sucesso!\n");
                break;

            case 4:
                iconizar(&image);
                printf("A imagem foi reduzida para 64x64 com sucesso!\n");
                break;

            case 5:
                printf("Quantos ruídos você deseja adicionar à imagem? ");
                scanf("%d", &fator);
                ruido(&image, fator);
                printf("Ruídos foram adicionados com sucesso!\n");
                break;

            case 6:
                suavizar(&image);
                printf("A imagem foi suavizada com sucesso!\n");
                break;

            case 0:
                escreverPGM("edit.pgm", &image);
                printf("Imagem salva com sucesso no arquivo edit.pgm.\n");
                printf("Saindo...\n");
                break;
                
            default:
                printf("Opção inválida. Tente novamente.\n");
        }
    } while (opcao != 0);



    return 0;
}
