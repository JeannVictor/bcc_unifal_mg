#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "tp1.h"

int lerArquivo(Carro carro[], const char* nomeArquivo) {
    FILE *arquivo;
    char linha[300];
    int totalcarros = 0;

    arquivo = fopen(nomeArquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nomeArquivo);
        return 0;
    }

    while (fgets(linha, sizeof(linha), arquivo) && totalcarros < MAX_CARROS) {
        linha[strcspn(linha, "\n")] = 0;
        if (strstr(linha, "FIM") != NULL) break;

        int lidos = sscanf(
            linha,
            "%s %s %s %d %d %f %s %s %s %s %d %s %f",
            carro[totalcarros].modelo,
            carro[totalcarros].marca,
            carro[totalcarros].tipo,
            &carro[totalcarros].ano,
            &carro[totalcarros].km,
            &carro[totalcarros].potencia,
            carro[totalcarros].combustivel,
            carro[totalcarros].cambio,
            carro[totalcarros].direcao,
            carro[totalcarros].cor,
            &carro[totalcarros].portas,
            carro[totalcarros].placa,
            &carro[totalcarros].valor
        );

        if (lidos == 13) {
            carro[totalcarros].valido = 1;
            totalcarros++;
        } else {
            printf("Erro ao processar a linha: %s\n", linha);
        }
    }

    fclose(arquivo);
    return totalcarros;
}

void salvarArquivo(Carro carro[], int totalcarros, const char* nomeArquivo) {
    FILE *arquivo = fopen(nomeArquivo, "w");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s para escrita\n", nomeArquivo);
        return;
    }

    for (int i = 0; i < totalcarros; i++) {
        if (carro[i].valido) {
            fprintf(
                arquivo,
                "%s %s %s %d %d %.2f %s %s %s %s %d %s %.2f\n",
                carro[i].modelo,
                carro[i].marca,
                carro[i].tipo,
                carro[i].ano,
                carro[i].km,
                carro[i].potencia,
                carro[i].combustivel,
                carro[i].cambio,
                carro[i].direcao,
                carro[i].cor,
                carro[i].portas,
                carro[i].placa,
                carro[i].valor
            );
        }
    }

    fprintf(arquivo, "FIM\n");
    fclose(arquivo);
}

void adicionarVeiculo(Carro *carro, int *totalcarros) {
    // Verifica se o limite de veículos foi atingido.
    if (*totalcarros >= MAX_CARROS) {
        printf("Limite do banco de dados atingido.\n");
        return;
    }

    Carro novoCarro;

    // Dados do novo veículo.
    printf("Forneça os dados do novo veículo!\n");
    
    printf("Modelo: ");
    fgets(novoCarro.modelo, sizeof(novoCarro.modelo), stdin);
    novoCarro.modelo[strcspn(novoCarro.modelo, "\n")] = 0;

    printf("Marca: ");
    fgets(novoCarro.marca, sizeof(novoCarro.marca), stdin);
    novoCarro.marca[strcspn(novoCarro.marca, "\n")] = 0;

    printf("Tipo: ");
    fgets(novoCarro.tipo, sizeof(novoCarro.tipo), stdin);
    novoCarro.tipo[strcspn(novoCarro.tipo, "\n")] = 0;

    printf("Ano: ");
    scanf("%d", &novoCarro.ano);
    while (getchar() != '\n'); // Limpa o buffer

    printf("Quilometragem: ");
    scanf("%d", &novoCarro.km);
    while (getchar() != '\n'); // Limpa o buffer

    printf("Potência: ");
    scanf("%f", &novoCarro.potencia);
    while (getchar() != '\n'); // Limpa o buffer

    printf("Tipo de combustível: ");
    fgets(novoCarro.combustivel, sizeof(novoCarro.combustivel), stdin);
    novoCarro.combustivel[strcspn(novoCarro.combustivel, "\n")] = 0;

    printf("Tipo de câmbio: ");
    fgets(novoCarro.cambio, sizeof(novoCarro.cambio), stdin);
    novoCarro.cambio[strcspn(novoCarro.cambio, "\n")] = 0;

    printf("Tipo de direção: ");
    fgets(novoCarro.direcao, sizeof(novoCarro.direcao), stdin);
    novoCarro.direcao[strcspn(novoCarro.direcao, "\n")] = 0;

    printf("Cor: ");
    fgets(novoCarro.cor, sizeof(novoCarro.cor), stdin);
    novoCarro.cor[strcspn(novoCarro.cor, "\n")] = 0;

    printf("Número de portas: ");
    scanf("%d", &novoCarro.portas);
    while (getchar() != '\n'); // Limpa o buffer

    printf("Placa do veículo: ");
    fgets(novoCarro.placa, sizeof(novoCarro.placa), stdin);
    novoCarro.placa[strcspn(novoCarro.placa, "\n")] = 0;

    printf("Valor: ");
    scanf("%f", &novoCarro.valor);
    while (novoCarro.valor < 0) {
        printf("Digite um valor válido!\n");
        scanf("%f", &novoCarro.valor);
    }
    while (getchar() != '\n'); // Limpa o buffer

    novoCarro.valido = 1;

    carro[*totalcarros] = novoCarro;
    (*totalcarros)++;

    printf("Veículo adicionado com sucesso!\n");
}

void buscarVeiculoPorPlaca(Carro carro[], int *totalcarros) {
    
    char placa[MAX_CAMPO];
    int existe = 0, opcao;

    // Obter a placa a ser buscada
    printf("Digite a placa do veículo para buscá-lo: ");
    fgets(placa, sizeof(placa), stdin);
    placa[strcspn(placa, "\n")] = 0;

    // Loop para busca e uma possível remoção
    for (int i = 0; i < *totalcarros; i++) {
        if (carro[i].valido && strcmp(carro[i].placa, placa) == 0) {
            existe = 1;
            printf("O carro de placa %s foi encontrado no banco de dados!\n", carro[i].placa);

            printf("Você gostaria de excluir o respectivo veículo? (1 = SIM, 0 = NÃO): ");
            scanf("%d", &opcao);
            while (getchar() != '\n'); // Limpa o buffer

            if (opcao == 1) {
                carro[i].valido = 0;
                printf("O veículo de placa %s foi excluído!\n", carro[i].placa);
                return;
            } else {
                printf("O veículo não foi excluído.\n");
                return;
            }
        }
    }

    if (!existe) {
        printf("A placa digitada não foi encontrada no banco de dados.\n");
    }
}

void buscarVeiculoPorTipo(Carro carro[], int totalcarros) {
    char type[MAX_CAMPO]; // Armazena o tipo buscado
    int existe = 0;       // Controle para verificar se o tipo foi encontrado

    // Obter o tipo do veículo a ser buscado
    printf("Digite o tipo do veículo para buscá-lo: ");
    fgets(type, sizeof(type), stdin);
    type[strcspn(type, "\n")] = 0; // Remover o caractere de nova linha

    // Loop para busca do tipo
    printf("\nResultados encontrados:\n");
    for (int i = 0; i < totalcarros; i++) {
        if (carro[i].valido && strcmp(carro[i].tipo, type) == 0) {
            existe = 1;
            printf("Placa: %s | Modelo: %s | Marca: %s | Ano: %d | Valor: %.2f\n",
                   carro[i].placa, carro[i].modelo, carro[i].marca, carro[i].ano, carro[i].valor);
        }
    }

    // Mensagem caso nenhum veículo seja encontrado
    if (!existe) {
        printf("O tipo de veículo buscado não existe no banco de dados.\n");
        printf("Tipos disponíveis: Hatch, SUV, Pick-up, Sedan, Passeio, Van.\n");
    }
}

void buscarVeiculoPorCambio(Carro carro[], int totalcarros) {
    char cambioo[MAX_CAMPO]; // Armazena o tipo de câmbio buscado
    int existe = 0;          // Controle para verificar se o câmbio foi encontrado

    // Obter o tipo de câmbio do veículo a ser buscado
    printf("Digite o tipo de câmbio do veículo para buscá-lo: ");
    fgets(cambioo, sizeof(cambioo), stdin);
    cambioo[strcspn(cambioo, "\n")] = 0; // Remover o caractere de nova linha

    // Loop para busca do tipo de câmbio
    printf("\nResultados encontrados:\n");
    for (int i = 0; i < totalcarros; i++) {
        if (carro[i].valido && strcmp(carro[i].cambio, cambioo) == 0) {
            existe = 1;
            printf("Placa: %s | Modelo: %s | Marca: %s | Ano: %d | Valor: %.2f\n",
                   carro[i].placa, carro[i].modelo, carro[i].marca, carro[i].ano, carro[i].valor);
        }
    }

    // Mensagem caso nenhum veículo seja encontrado
    if (!existe) {
        printf("O tipo de câmbio buscado não existe no banco de dados.\n");
        printf("Tipos disponíveis: Manual, Automático.\n");
    }
}

void buscarVeiculoPorIntervaloValor(Carro carro[], int totalcarros) {
    // Váriaveis
    float first, second;
    int existe = 0;

    printf("Todos os veículos dentro do intervalo digitado serão mostrados.\n");
    printf("O 1° valor do intervalo precisa ser menor que o 2° (ambos não podem ser <= 0).\n");

    // Obter o primeiro valor do intervalo
    do {
        printf("Digite o 1° valor (deve ser > 0): ");
        scanf("%f", &first);
    } while (first <= 0);

    // Obter o segundo valor do intervalo
    do {
        printf("Digite o 2° valor (deve ser > 0): ");
        scanf("%f", &second);
    } while (second <= 0);

    // Garantir que first < second
    while (first >= second) {
        printf("O 1° valor precisa ser menor que o 2°.\n");
        printf("Digite o 2° valor válido: ");
        scanf("%f", &second);
    }
    while (getchar() != '\n'); // Limpa o buffer

    // Loop para busca
    printf("\nVeículos no intervalo de valor %.2f a %.2f:\n", first, second);
    for (int i = 0; i < totalcarros; i++) {
        if (carro[i].valido && carro[i].valor >= first && carro[i].valor <= second) {
            existe = 1;
            printf("Placa: %s | Modelo: %s | Marca: %s | Ano: %d | Valor: %.2f\n",
                   carro[i].placa, carro[i].modelo, carro[i].marca, carro[i].ano, carro[i].valor);
        }
    }

    if (!existe) {
        printf("Não existem veículos dentro desse intervalo de valor.\n");
    }
}

void gerarRelatorio(Carro carro[], int totalcarros) {
    // Inicializar variáveis locais
    int SUV = 0, Hatch = 0, Pick = 0, Sedan = 0, Passeio = 0, Van = 0;
    int flex = 0, gasosa = 0, diesel = 0;
    int qtd = 0;
    double quilometragem = 0.0;
    double barato = 500000.0, caro = -1.0;
    int existe = 0, indiceBarato = -1, indiceCaro = -1;

    // Contar tipos de veículos
    for (int i = 0; i < totalcarros; i++) {
        if (!carro[i].valido) continue;
        
        if (strcmp(carro[i].tipo, "SUV") == 0) SUV++;
        else if (strcmp(carro[i].tipo, "Hatch") == 0) Hatch++;
        else if (strcmp(carro[i].tipo, "Pick-up") == 0) Pick++;
        else if (strcmp(carro[i].tipo, "Sedan") == 0) Sedan++;
        else if (strcmp(carro[i].tipo, "Passeio") == 0) Passeio++;
        else if (strcmp(carro[i].tipo, "Van") == 0) Van++;

        if (strcmp(carro[i].combustivel, "Flex") == 0) flex++;
        else if (strcmp(carro[i].combustivel, "Gasolina") == 0) gasosa++;
        else if (strcmp(carro[i].combustivel, "Diesel") == 0) diesel++;
    }

    // Calcular porcentagens de tipos de veículos
    printf("Porcentagens por tipo de veículo:\n");
    printf("SUV: %.2f%%\n", (SUV / (double)totalcarros) * 100);
    printf("Hatch: %.2f%%\n", (Hatch / (double)totalcarros) * 100);
    printf("Pick-up: %.2f%%\n", (Pick / (double)totalcarros) * 100);
    printf("Sedan: %.2f%%\n", (Sedan / (double)totalcarros) * 100);
    printf("Passeio: %.2f%%\n", (Passeio / (double)totalcarros) * 100);
    printf("Van: %.2f%%\n", (Van / (double)totalcarros) * 100);
    printf("------------------------------------------------------------------------------------------------\n");

    // Calcular porcentagens de combustíveis
    printf("Porcentagens por tipo de combustível:\n");
    printf("Flex: %.2f%%\n", (flex / (double)totalcarros) * 100);
    printf("Gasolina: %.2f%%\n", (gasosa / (double)totalcarros) * 100);
    printf("Diesel: %.2f%%\n", (diesel / (double)totalcarros) * 100);
    printf("------------------------------------------------------------------------------------------------\n");

    // Veículo mais barato com motor 1.0
    for (int i = 0; i < totalcarros; i++) {
        if (carro[i].valido && carro[i].potencia == 1.0 && carro[i].valor < barato) {
            barato = carro[i].valor;
            indiceBarato = i;
        }
    }
    if (indiceBarato != -1) {
        double prestacao = barato * (0.0149 / (1 - pow(1.0149, -60)));
        printf("Veículo mais barato com motor 1.0:\n");
        printf("Placa: %s | Valor: %.2f | Prestação (60 meses): %.2f\n", 
               carro[indiceBarato].placa, barato, prestacao);
    } else {
        printf("Não existem veículos com motor 1.0 no banco de dados.\n");
    }
    printf("------------------------------------------------------------------------------------------------\n");

    // Veículo mais caro com direção hidráulica e câmbio automático
    for (int i = 0; i < totalcarros; i++) {
        if (carro[i].valido && strcmp(carro[i].direcao, "Hidráulica") == 0 && 
            strcmp(carro[i].cambio, "Automático") == 0 && carro[i].valor > caro) {
            caro = carro[i].valor;
            indiceCaro = i;
        }
    }
    if (indiceCaro != -1) {
        double seguro = caro * 0.066; // 6.6% do valor do veículo
        printf("Veículo mais caro com direção hidráulica e câmbio automático:\n");
        printf("Placa: %s | Valor: %.2f | Seguro estimado: %.2f\n", 
               carro[indiceCaro].placa, caro, seguro);
    } else {
        printf("Não existem veículos com direção hidráulica e câmbio automático no banco de dados.\n");
    }
    printf("------------------------------------------------------------------------------------------------\n");

    // Quantidade e média de quilometragem de veículos com 5 anos ou mais
    for (int i = 0; i < totalcarros; i++) {
        if (carro[i].valido && carro[i].ano <= 2019) {
            qtd++;
            quilometragem += carro[i].km;
        }
    }
    if (qtd > 0) {
        printf("Veículos com 5 anos ou mais:\n");
        printf("Quantidade: %d | Média de quilometragem: %.2f\n", qtd, quilometragem / qtd);
    } else {
        printf("Não existem veículos com 5 anos ou mais no banco de dados.\n");
    }
    printf("------------------------------------------------------------------------------------------------\n");
}



