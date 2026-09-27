#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Exercício 1
// Autor: Jeann Victor Batista

// Estrutura Utilizada 
typedef struct {
    int idade;
    int resposta;  
} produto;
 
// Função para leitura do arquivo
int lerArquivo(produto arr[], const char* nomeArquivo) {
    FILE *arquivo;
    char linha[300];
    int total = 0;

    arquivo = fopen(nomeArquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nomeArquivo);
        return 0;
    }

    while (fgets(linha, sizeof(linha), arquivo) && total < 200) {
        linha[strcspn(linha, "\n")] = 0;
        if (strstr(linha, "fim") != NULL) break;

        int lidos = sscanf(linha,"%d %d ",&arr[total].idade,&arr[total].resposta);

        if (lidos == 2) {
            total++;
        } else {
            printf("Erro ao processar a linha: %s\n", linha);
        }
    }

    fclose(arquivo);
    return total;
}

int main()
{
    produto arr[200];
    int totalLidos = lerArquivo(arr, "pesquisa_mercado.txt");
    int totalsim = 0,totalnao = 0,medianao = 0,mediasim = 0,novo = 200,velho = -1;

    // Loop para encontrar dados
    for (int i = 0; i < totalLidos; i++) {
        if(arr[i].resposta == 1){
            totalsim++;
            mediasim = arr[i].idade + mediasim;
            if(arr[i].idade < novo) novo = arr[i].idade;
            else if(arr[i].idade > velho) velho = arr[i].idade;
        }
        if(arr[i].resposta == 0){
            totalnao++;
            medianao = arr[i].idade + medianao;
        }
    }

    // Cálculo das médias
    mediasim = mediasim/totalsim;
    medianao = medianao/totalnao;

    // Impressão dos resultados
    printf("Total de respostas SIM: %d\n",totalsim);
    printf("Total de respostas NÃO: %d\n",totalnao);
    printf("Média de idade das pessoas que responderam SIM: %d\n",mediasim);
    printf("Média de idade das pessoas que responderam NÃO: %d\n",medianao);
    printf("A idade da pessoa mais velha a responder SIM foi: %d\n",velho);
    printf("A idade da pessoa mais nova a responder SIM foi: %d\n",novo);
    return 0;
}


    
 



