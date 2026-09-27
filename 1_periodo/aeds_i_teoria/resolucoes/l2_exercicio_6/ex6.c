#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Exercício 6: 
// Autor: Jeann Victor Batista

// Função que retorna a data por extenso como uma string
void data(int dia, int mes, int ano, char *resultado) {
    const char *meses[] = {
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    };

    if (mes < 1 || mes > 12 || dia < 1 || dia > 31) {
        strcpy(resultado, "Data inválida!");
        return;
    }

    // Monta a string no buffer `resultado`
    sprintf(resultado, "%d de %s de %d", dia, meses[mes - 1], ano);
}

int main() {
    int dia, mes, ano;
    char resultado[50];

    printf("Qual o dia?\n");
    scanf("%d", &dia);
    printf("Qual o mês?\n");
    scanf("%d", &mes);
    printf("Qual o ano?\n");
    scanf("%d", &ano);

    // Chama a função e armazena o resultado
    data(dia, mes, ano, resultado);

    // Exibe o resultado
    printf("%s\n", resultado);

    return 0;
}
