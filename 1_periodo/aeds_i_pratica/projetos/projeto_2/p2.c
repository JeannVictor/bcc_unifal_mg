#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Atividade 2: Números Aleatórios
// Autor: Jeann Victor Batista

int main()
{
    // Criação de Váriaveis
    float menor = 2.30 , maior = 0.0,somaALT = 0;
    int altos = 0;   
    srand(time(NULL));

    // Loop para criação e verificação dos dados.
    for(int i = 0;i < 1000;i++){
        float altura = ( 150 + rand()%81)/100.0; // Geração de alturas entre 1,50M e 2,30M.
        somaALT = altura + somaALT;
        
        // Descobrir a maior altura.
        if(altura > maior){
            maior = altura;
        }
        // Descobrir a menor altura.
        if(altura < menor){
            menor = altura;
        }
        // Descobrir as alturas > 2.0M.
        if(altura > 2.0){
            altos ++;    
        }
    }
    
    // Resultados 
    printf("A média de altura foi: %.2f metros\n", somaALT/1000.0);
    printf("A maior altura foi: %.2f metros\n", maior);
    printf("A menor altura foi: %.2f metros\n", menor);
    printf("A porcentagem de pessoas com mais de 2.0 metros foi: %.2f%%\n",(altos / 1000.0) * 100 );
 
    return 0;
}
