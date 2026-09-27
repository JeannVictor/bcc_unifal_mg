#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Exercício 7: 
// Autor: Jeann Victor Batista

// Função para transformar dados em segundos
int segundos(int hora,int minuto,int segundo){
    int horas = hora * 3600;
    int minutos = minuto * 60;

    return horas + minutos + segundo;
}

int main(){

    // Criação de váriaveis
    int hora = 0,minuto = 0,segundo = 0;

    // Obtendo valor das váriaveis
    printf("Quantas horas são?\n");
    scanf("%d",&hora);
    printf("Quantos minutos são?\n");
    scanf("%d",&minuto);
    printf("Quantos segundos são?\n");
    scanf("%d",&segundo);

    // Criação váriavel total
    int total = segundos(hora,minuto,segundo); 

    // Impressão dos resultados
    printf("A(s) hora(s): %d em segundos é : %d\n",hora,hora * 3600);
    printf("O(s) minuto(s): %d em segundos é : %d\n",minuto,minuto * 60);
    printf("O(s) segundo(s): %d em segundos é : %d\n",segundo,segundo);
    printf("O total de segundos é: %d\n",total);

    return 0;
}
