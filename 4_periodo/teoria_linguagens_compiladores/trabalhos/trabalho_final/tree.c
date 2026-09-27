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

// Enumerador para os tipos de nós na árvore sintática
typedef enum {
    PGR,   // Programa
    IDF,   // Identificador
    DDV,   // Declaração de Variáveis
    LDV,   // Lista de Variáveis
    LDC,   // Lista de Comandos
    TIP,   // Tipo (de identificador)
    LER,   // Leitura
    ESC,   // Escrita
    REP,   // Repetição
    SEL,   // Seleção
    ATR,   // Atribuição
    OU,    // Ou
    E,     // E
    IGUAL, // Igual
    MAI,   // Maior
    MEN,   // Menor
    SUM,   // Soma
    SUB,   // Subtração
    MULT,  // Multiplicação
    DIV,   // Divisão
    NAO,   // Negação
    VAR,   // Variável
    NUM,   // Número
    BOOL   // Booleano
} TipoNo;

typedef struct no *ptno;

struct no {
    char valor[100];
    TipoNo tipo;
    ptno filho;
    ptno irmao;
};

char *tipoToString(TipoNo tipo) {
    switch (tipo) {
        case PGR:   return "Programa";
        case IDF:   return "Identificador";
        case DDV:   return "Declaração de Variáveis";
        case LDV:   return "Lista de Variáveis";
        case LDC:   return "Lista de Comandos";
        case TIP:   return "Tipo";
        case LER:   return "Leitura";
        case ESC:   return "Escrita";
        case REP:   return "Repetição";
        case SEL:   return "Seleção";
        case ATR:   return "Atribuição";
        case OU:    return "Ou";
        case E:     return "E";
        case IGUAL: return "Igual";
        case MAI:   return "Maior";
        case MEN:   return "Menor";
        case SUM:   return "Soma";
        case SUB:   return "Subtrai";
        case MULT:  return "Multiplica";
        case DIV:   return "Divide";
        case NAO:   return "Negação";
        case VAR:   return "Variável";
        case NUM:   return "Número";
        case BOOL:  return "Booleano";
        default:    return "UNKNOWN";
    }
}

ptno criaNo(int tipo, char* valor) {
    ptno novo_no = (ptno)malloc(sizeof(struct no));
    if (!novo_no) {
        return NULL;
    }
    strcpy(novo_no->valor, valor);
    novo_no->tipo = tipo;
    novo_no->filho = NULL;
    novo_no->irmao = NULL;
    return novo_no;
}

void adicionaFilho(ptno pai, ptno filho) {
    if (!pai || !filho) {
        return;
    }
    filho->irmao = pai->filho;
    pai->filho = filho;
}

void geraNos(FILE *fp, ptno raiz) {
    ptno p;
    fprintf(fp, "\tn%p [label=\"%s|%s\"]\n", raiz, tipoToString(raiz->tipo), raiz->valor);
    p = raiz->filho;
    while (p) {
        geraNos(fp, p);
        p = p->irmao;
    }
}

void geraLigacoes(FILE *fp, ptno raiz) {
    ptno p;
    p = raiz->filho;
    while (p) {
        fprintf(fp, "\tn%p -> n%p\n", raiz, p);
        geraLigacoes(fp, p);
        p = p->irmao;
    }
}

void geraDot(ptno raiz, char *nomeArq) {
    char nomeCompleto[100];
    sprintf(nomeCompleto, "%s.dot", nomeArq);
    
    FILE *fp = fopen(nomeCompleto, "wt");
    fprintf(fp, "digraph {\n");
    fprintf(fp, "\tnode [shape=record, height=.1];\n");
    geraNos(fp, raiz);
    geraLigacoes(fp, raiz);
    fprintf(fp, "}\n");
    fclose(fp);
    
    // Gera arquivo SVG
    char comando[200];
    sprintf(comando, "dot -Tsvg %s.dot -o %s.svg", nomeArq, nomeArq);
    system(comando);
}

extern FILE *yyout;
extern elemTabSimb tabSimb[], elemTab;
extern int topoTab;
extern void insereTabelaSimbolos(elemTabSimb elem);
extern int buscaTabelaSimbolos(char *id);
extern void empilha(int val);
extern int desempilha();

int NUM_VAR = 0;
int TIPO_ATUAL = -1;
int ROTULO_ATUAL = 0;

void geraCodigo(ptno cod) {
    if (!cod) return;
    
    ptno cod1, cod2, cod3;
    int pos, x, y;
    
    switch (cod->tipo) {
        case PGR:
            cod1 = cod->filho; 
            cod2 = cod1->irmao;
            if (cod2) 
                cod3 = cod2->irmao;
            else 
                cod3 = NULL;

            fprintf(yyout, "\tINPP\n");
            geraCodigo(cod2);
            
            fprintf(yyout, "\tAMEM\t%d\n", NUM_VAR);
            empilha(NUM_VAR);
            geraCodigo(cod3);

            int conta = desempilha();
            fprintf(yyout, "\tDMEM\t%d\n", conta);
            fprintf(yyout, "\tFIMP\n");
            break;
            
        case DDV:
            cod1 = cod->filho;
            cod2 = cod1->irmao;
            cod3 = cod2->irmao;
            geraCodigo(cod1);
            geraCodigo(cod2);
            if (cod3) {
                geraCodigo(cod3);
            }
            break;
            
        case TIP:
            if (strcmp(cod->valor, "inteiro") == 0) {
                TIPO_ATUAL = INT;
            } else {
                TIPO_ATUAL = LOG;
            }
            break;
            
        case LDV:
            cod1 = cod->filho;

            strcpy(elemTab.id, cod1->valor);
            elemTab.end = NUM_VAR++;
            elemTab.tip = TIPO_ATUAL;
            insereTabelaSimbolos(elemTab);

            cod2 = cod1->irmao;
            if (cod2) {
                geraCodigo(cod2);
            }
            break;
            
        case LDC:
            cod1 = cod->filho;
            geraCodigo(cod1);
            cod2 = cod1->irmao;
            if (cod2) {
                geraCodigo(cod2);
            }
            break;
            
        case LER:
            cod1 = cod->filho;
            pos = buscaTabelaSimbolos(cod1->valor);
            fprintf(yyout, "\tLEIA\n");
            fprintf(yyout, "\tARZG\t%d\n", tabSimb[pos].end);
            break;
            
        case ESC:
            cod1 = cod->filho;
            geraCodigo(cod1);
            fprintf(yyout, "\tESCR\n");
            break;
            
        case REP:
            cod1 = cod->filho; // Expressao
            cod2 = cod1->irmao; // Lista de comandos
            
            x = ROTULO_ATUAL++;
            y = ROTULO_ATUAL++;

            fprintf(yyout, "L%d\tNADA\n", x);
            geraCodigo(cod1);
            fprintf(yyout, "\tDSVF\tL%d\n", y);
            geraCodigo(cod2);
            fprintf(yyout, "\tDSVS\tL%d\n", x);
            fprintf(yyout, "L%d\tNADA\n", y);
            break;
            
        case SEL:
            cod1 = cod->filho; // Expressao
            cod2 = cod1->irmao; // Lista de comandos SE
            cod3 = cod2->irmao; // Lista de comandos SENAO

            x = ROTULO_ATUAL++;
            y = ROTULO_ATUAL++;

            geraCodigo(cod1);
            fprintf(yyout, "\tDSVF\tL%d\n", x);
            geraCodigo(cod2);
            fprintf(yyout, "\tDSVS\tL%d\n", y);
            fprintf(yyout, "L%d\tNADA\n", x);
            if (cod3) {
                geraCodigo(cod3);
            }
            fprintf(yyout, "L%d\tNADA\n", y);
            break;
            
        case ATR:
            cod1 = cod->filho; // Variavel
            cod2 = cod1->irmao; // Expressao
            pos = buscaTabelaSimbolos(cod1->valor);
            geraCodigo(cod2);
            fprintf(yyout, "\tARZG\t%d\n", tabSimb[pos].end);
            break;
            
        case OU:
            cod1 = cod->filho;
            cod2 = cod1->irmao;
            geraCodigo(cod1);
            geraCodigo(cod2);
            fprintf(yyout, "\tDISJ\n");
            break;
            
        case E:
            cod1 = cod->filho;
            cod2 = cod1->irmao;
            geraCodigo(cod1);
            geraCodigo(cod2);
            fprintf(yyout, "\tCONJ\n");
            break;
            
        case IGUAL:
            cod1 = cod->filho;
            cod2 = cod1->irmao;
            geraCodigo(cod1);
            geraCodigo(cod2);
            fprintf(yyout, "\tCMIG\n");
            break;
            
        case MAI:
            cod1 = cod->filho;
            cod2 = cod1->irmao;
            geraCodigo(cod1);
            geraCodigo(cod2);
            fprintf(yyout, "\tCMMA\n");
            break;
            
        case MEN:
            cod1 = cod->filho;
            cod2 = cod1->irmao;
            geraCodigo(cod1);
            geraCodigo(cod2);
            fprintf(yyout, "\tCMME\n");
            break;
            
        case SUM:
            cod1 = cod->filho;
            cod2 = cod1->irmao;
            geraCodigo(cod1);
            geraCodigo(cod2);
            fprintf(yyout, "\tSOMA\n");
            break;
            
        case SUB:
            cod1 = cod->filho;
            cod2 = cod1->irmao;
            geraCodigo(cod1);
            geraCodigo(cod2);
            fprintf(yyout, "\tSUBT\n");
            break;
            
        case MULT:
            cod1 = cod->filho;
            cod2 = cod1->irmao;
            geraCodigo(cod1);
            geraCodigo(cod2);
            fprintf(yyout, "\tMULT\n");
            break;
            
        case DIV:
            cod1 = cod->filho;
            cod2 = cod1->irmao;
            geraCodigo(cod1);
            geraCodigo(cod2);
            fprintf(yyout, "\tDIVI\n");
            break;
            
        case VAR:
            pos = buscaTabelaSimbolos(cod->valor);
            fprintf(yyout, "\tCRVG\t%d\n", tabSimb[pos].end);
            break;
            
        case NUM:
            fprintf(yyout, "\tCRCT\t%s\n", cod->valor);
            break;
            
        case BOOL:
            if (strcmp(cod->valor, "V") == 0) {
                fprintf(yyout, "\tCRCT\t1\n");
            } else {
                fprintf(yyout, "\tCRCT\t0\n");
            }
            break;
            
        default:
            break;
    }
}