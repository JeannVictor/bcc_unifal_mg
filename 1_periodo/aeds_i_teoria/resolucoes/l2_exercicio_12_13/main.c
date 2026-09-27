#include <stdio.h>
#include <stdlib.h>
#include "ex12.h"

// Exercício 12 e 13: 
// Autor: Jeann Victor Batista

int main() {
    pessoa pessoas[MAX_PESSOAS];
    int totalPessoas = 0;
    int opcao;
    
    // Ler dados do arquivo
    totalPessoas = lerArquivo(pessoas, "nascimento.txt");
    printf("%d pessoas carregadas do arquivo.\n", totalPessoas);

    do {
        printf("\nMenu:\n");
        printf("1. Adicionar pessoa\n");
        printf("2. Buscar pessoa por nome\n");
        printf("3. Salvar e sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);
        while (getchar() != '\n'); // Limpa o buffer

        switch (opcao) {
            case 1:
                adicionarpessoa(pessoas, &totalPessoas);
                break;
            case 2:
                buscarPessoaporNome(pessoas, &totalPessoas);
                break;
            case 3:
                salvarArquivo(pessoas, totalPessoas, "nascimento.txt");
                printf("Alterações salvas. Saindo...\n");
                break;
            default:
                printf("Opção inválida. Tente novamente.\n");
        }

    } while (opcao != 3);

    return 0;
}

