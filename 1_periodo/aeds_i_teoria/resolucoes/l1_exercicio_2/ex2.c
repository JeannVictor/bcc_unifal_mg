#include <stdio.h>
#include <string.h>

// Exercício 2
// Autor: Jeann Victor Batista

// Estrutura Utilizada 
typedef struct {
    char sexo[2];
    int meses;  
} dados;

// Função para leitura do arquivo
int lerArquivo(dados arr[], const char* nomeArquivo) {

    FILE *arquivo= fopen(nomeArquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nomeArquivo);
        return 0;
    }

    char linha[300];
    int total = 0;

    while (fgets(linha, sizeof(linha), arquivo) && total < 200) {
        linha[strcspn(linha, "\n")] = 0;
        if (strstr(linha, "FIM") != NULL) break;

        int lidos = sscanf(linha,"%1s %d ",arr[total].sexo,&arr[total].meses);

        if (lidos == 2) {
            total++;
        } else {
            printf("Erro ao processar a linha: %s\n", linha);
        }
    }

    fclose(arquivo);
    return total;
}

int main() {
    dados arr[200];
    int totalLidos = lerArquivo(arr, "mortalidade.txt");

    float totalM = 0, totalF = 0, mortoM = 0, mortoF = 0, menos24 = 0;

    // Loop para processar os dados
    for (int i = 0; i < totalLidos; i++) {
        if (strcmp(arr[i].sexo, "M") == 0) {
            totalM++;
            if (arr[i].meses == 0) mortoM++;
        } else if (strcmp(arr[i].sexo, "F") == 0) {
            totalF++;
            if (arr[i].meses == 0) mortoF++;
        }
        if (arr[i].meses > 0 && arr[i].meses <= 24) {
            menos24++;
        }
    }

    // Cálculo das porcentagens
    float percentMorto = (mortoM + mortoF) / totalLidos * 100;
    float percentMortoM = mortoM / totalLidos * 100;
    float percentMortoF = mortoF / totalLidos * 100;
    float percentMenos24 = menos24 / totalLidos * 100;

    // Impressão dos resultados
    printf("Total de crianças nascidas no período: %d\n", totalLidos);
    printf("Percentagem de crianças mortas no período: %.2f%%\n", percentMorto);
    printf("Percentagem de crianças do sexo masculino mortas: %.2f%%\n", percentMortoM);
    printf("Percentagem de crianças do sexo feminino mortas: %.2f%%\n", percentMortoF);
    printf("Percentagem de crianças que viveram até 24 meses (não nasceram mortas): %.2f%%\n", percentMenos24);

    return 0;
}
