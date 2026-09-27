#include <stdio.h>
#include <stdlib.h>
#include "tp1.h"

int main() {
    Carro carros[MAX_CARROS] = {0};
    int totalcarros = 0, opcao;
    const char* arquivoDados = "BD_veiculosed.txt";

    // Carregar os dados do arquivo no início
    totalcarros = lerArquivo(carros, arquivoDados);

    do {
        printf("\nMenu de Opções:\n");
        printf("1. Adicionar Veículo\n");
        printf("2. Buscar Veículo por Placa\n");
        printf("3. Buscar Veículo por Tipo\n");
        printf("4. Buscar Veículo por Câmbio\n");
        printf("5. Buscar Veículo por Intervalo de Valor\n");
        printf("6. Gerar Relatório\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);
        getchar(); // Limpa buffer

        switch (opcao) {
            case 1:
                adicionarVeiculo(carros, &totalcarros);
                break;
            case 2:
                buscarVeiculoPorPlaca(carros, &totalcarros);
                break;
            case 3:
                buscarVeiculoPorTipo(carros, totalcarros);
                break;
            case 4:
                buscarVeiculoPorCambio(carros, totalcarros);
                break;
            case 5:
                buscarVeiculoPorIntervaloValor(carros, totalcarros);
                break;
            case 6:
                gerarRelatorio(carros, totalcarros);
                break;
            case 0:
                printf("Saindo...\n");
                salvarArquivo(carros, totalcarros, arquivoDados);
                break;
            default:
                printf("Opção inválida. Tente novamente.\n");
        }
    } while (opcao != 0);

    return 0;
}
