/*+=============================================================
|           UNIFAL = Universidade Federal de Alfenas .
|           BACHARELADO EM CIENCIA DA COMPUTACAO.
| Trabalho ..: Construcao Arvore Sintatica e Geracao de Codigo
| Disciplina : Teoria de Linguagens e Compiladores
| Professor .: Luiz Eduardo da Silva
| Aluno .....: Jeann Victor Batista   2024.1.08.014
| Data ......: 30/11/2025
+=============================================================*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TAM_TAB 100
extern int yyerror(char *msg);

enum {
    INT,
    LOG
};

typedef struct {
    char id[100];
    int end;
    int tip;
} elemTabSimb;

elemTabSimb tabSimb[TAM_TAB], elemTab;
int topoTab = 0; 

void insereTabelaSimbolos(elemTabSimb elem) {
    int i;
    if (topoTab == TAM_TAB)
        yyerror("Tabela de símbolos cheia!");
    
    for (i = topoTab - 1; i >= 0 && strcmp(tabSimb[i].id, elem.id); i--);
    
    if (i != -1) {
        char msg[200];
        sprintf(msg, "O identificador [%s] é duplicado", elem.id);
        yyerror(msg);
    }
    tabSimb[topoTab++] = elem;
}

int buscaTabelaSimbolos(char *id) {
    int i;
    if (topoTab == 0) 
        yyerror("Não existem identificadores cadastrados");
    
    for (i = topoTab - 1; i >= 0 && strcmp(tabSimb[i].id, id); i--);
    
    if (i == -1) {
        char msg[200];
        sprintf(msg, "O identificador [%s] não foi encontrado", id);
        yyerror(msg);
    }
    return i; 
}

#define TAM_PIL 100
int pilha[TAM_PIL];
int topoPil = -1;

void empilha(int val) {
    if (topoPil == TAM_PIL - 1)
        yyerror("Pilha cheia!");
    pilha[++topoPil] = val;
}

int desempilha() {
    if (topoPil == -1)
        yyerror("Pilha vazia!");
    return pilha[topoPil--];
}