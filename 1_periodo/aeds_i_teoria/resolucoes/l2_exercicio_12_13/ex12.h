#include <stdbool.h>
#ifndef EX12_H
#define EX12_H

#define MAX_PESSOAS 1000

// Estrutura utilizada
typedef struct {
    char nome[100];
    int dia;
    int mes;
    int ano;
} pessoa;

// Declaração de funções
// Funções auxiliares
bool bissexto(int ano);
int diasNoMes(int mes, int ano);
// Funções de cálculo
void diastotais(int diaD,int mesD,int anoD,int diaATUAL,int mesATUAL,int anoATUAL);
void idade(int diaD, int mesD, int anoD, int diaATUAL, int mesATUAL, int anoATUAL);
// Funções de add/search
void adicionarpessoa(pessoa *dado, int *totalpessoas);
void buscarPessoaporNome(pessoa dado[], int *totalpessoas);
// Funções de ler/escrever/salvar arquivo
int lerArquivo(pessoa dados[], const char* nomeArquivo);
void salvarArquivo(pessoa dados[], int totalpessoas, const char* nomeArquivo);

#endif
