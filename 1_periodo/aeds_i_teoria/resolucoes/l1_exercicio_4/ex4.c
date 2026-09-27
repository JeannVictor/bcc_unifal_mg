#include <stdio.h>
#include <string.h>

// Exercício 4
// Autor: Jeann Victor Batista

// Estrutura Utilizada 
typedef struct {
    int canal;
    int pessoas;  
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

    while (fgets(linha, sizeof(linha), arquivo) && total < 100) {
        linha[strcspn(linha, "\n")] = 0;
        if (strstr(linha, "FIM") != NULL) break;

        int lidos = sscanf(linha,"%d %d ",&arr[total].canal,&arr[total].pessoas);

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
    int totalLidos = lerArquivo(arr, "canal.txt");

    // Declaração váriaveis
    float globo = 0, sbt = 0, band = 0, record = 0, casanula = 0;
    int totalV = 0;

    // Loop para processar os dados
    for (int i = 0; i < totalLidos; i++) {
        if (arr[i].canal == 0) continue; // Ignorar casas com TV desligada

        if(arr[i].canal == 4)
            globo = arr[i].pessoas;
        else if(arr[i].canal == 5)
            sbt = arr[i].pessoas;
        else if(arr[i].canal == 7)
            band = arr[i].pessoas;
        else if(arr[i].canal == 12)
            record = arr[i].pessoas;    
    }

    // Cálculo de percentagens
    totalV = globo + sbt + band + record;
    float percentglobo = (globo / totalV) * 100;
    float percentsbt = (sbt / totalV) * 100;
    float percentband = (band / totalV) * 100;
    float percentrecord = (record / totalV) * 100;

    // Impressão dos resultados 
    printf("A percentagem de âudiencia da GLobo é de: %.2f%%\n", percentglobo);
    printf("A percentagem de âudiencia da SBT é de: %.2f%%\n", percentsbt);
    printf("A percentagem de âudiencia da Band é de: %.2f%%\n", percentband);
    printf("A percentagem de âudiencia da Record é de: %.2f%%\n",percentrecord);
 
    return 0;
}