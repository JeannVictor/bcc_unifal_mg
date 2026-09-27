/*+-------------------------------------------------------------+
  |          UNIFAL – Universidade Federal de Alfenas.          |
  | BACHARELADO EM CIENCIA DA COMPUTACAO.                       |
  | Trabalho..: SIMULACAO DE SISTEMA DE ARQUIVOS FAT            |
  | Disciplina: Sistemas Operacionais                           |
  | Professor.: Romario                                         |
  | Aluno(s)..: Jeann Victor Batista                            |
  |             Nicolas Rodrigues Texeira de Oliveira           |
  |             Thallysson Luis Teixeira Carvalho               |
  | Data......: 30/11/2025                                      |
  +-------------------------------------------------------------+*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "fat.h"

void mostrar_comandos() {
    printf("\nCOMANDOS DISPONIVEIS:\n");
    printf("G - Gravar arquivo\n");
    printf("D - Deletar arquivo\n");
    printf("A - Apresentar arquivo\n");
    printf("M - Mostrar estruturas\n");
    printf("C - Desfragmentar disco\n");
    printf("H - Ajuda\n");
    printf("F - Sair\n");
}

int main(void) {
    ptnoSet Area;
    ptnoArq Arq;
    memoria Memo;
    char com[3];
    char nome[13];
    char texto[TAM_MEMORIA * TAM_GRANULO];
    
    inicia(&Area, &Arq, Memo);

    printf("=== SIMULADOR FAT - SISTEMA DE ARQUIVOS ===\n");
    mostrar_comandos();
    
    do {
        printf("\n=> ");
        scanf("%2s", com);
        com[0] = toupper(com[0]);
        
        switch (com[0]) {
            case 'G':
                printf("Digite o nome do arquivo: ");
                scanf("%12s", nome);
                if(busca_arquivo(&Arq, nome) != NULL){
                    printf("Já existe um arquivo com esse nome!\n");
                    break;
                }else{
                    printf("Digite o conteúdo: ");
                    getchar();
                    fgets(texto, sizeof(texto), stdin);
                    texto[strcspn(texto, "\n")] = 0;
                
                    printf("nome = %s\n", nome);
                    printf("texto = %s\n", texto);
                    gravar(nome, texto, &Area, &Arq, Memo);
                    break;
                }

                
            case 'D':
                printf("Digite o nome do arquivo que deseja deletar: ");
                scanf("%12s", nome);
                printf("nome = %s\n", nome);
                deletar(nome, &Arq, &Area, Memo);
                break;
                
            case 'A':
                printf("Digite o nome do arquivo que deseja ver o conteúdo: ");
                scanf("%12s", nome);
                printf("nome = %s\n", nome);
                apresentar(nome, &Arq, Memo);
                break;
                
            case 'M':
                mostraSetores(Area, "Area Livre");
                mostraArquivos(Arq);
                printf("Memoria:\n");
                mostraMemoria(Memo);
                break;
                
            case 'H':
                mostrar_comandos();
                break;
                
            case 'C':
                desfragmentar(&Arq, &Area, Memo);
                break;
                
            case 'F':
                printf("Finalizando...\n");
                break;
                
            default:
                printf("Comando invalido! Digite 'H' para ver os comandos disponiveis.\n");
                break;
        }
    } while (com[0] != 'F');
    
    printf("\nFim da Execucao\n\n");
    return (EXIT_SUCCESS);
}