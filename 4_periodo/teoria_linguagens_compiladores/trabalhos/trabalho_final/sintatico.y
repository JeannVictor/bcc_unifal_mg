%{
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
    #include "utils.c"
    #include "lexico.c"

    extern int yyerror(char *);
    extern char atomo[100];
    int yylex(void); 
    
    extern FILE *yyin, *yyout;

    ptno raiz;
    char nomePrograma[100];
%}

%token T_PROGRAMA T_INICIO T_FIM T_IDENTIF T_LEIA T_ESCREVA
%token T_ENQTO T_FACA T_FIMENQTO T_SE T_ENTAO T_SENAO T_FIMSE
%token T_ATRIB T_VEZES T_DIV T_MAIS T_MENOS T_MAIOR T_MENOR T_IGUAL
%token T_E T_OU T_V T_F T_NUMERO T_NAO T_ABRE T_FECHA
%token T_LOGICO T_INTEIRO

%start programa

%left T_OU
%left T_E
%left T_IGUAL
%left T_MAIOR T_MENOR
%left T_MAIS T_MENOS
%left T_VEZES T_DIV
%right T_NAO

%%

programa
    : cabecalho variaveis T_INICIO lista_comandos T_FIM
    {
        raiz = criaNo(PGR, "");
        adicionaFilho(raiz, $4);
        adicionaFilho(raiz, $2);
        adicionaFilho(raiz, $1);
        
        // Gera arquivo .dot e .svg
        geraDot(raiz, nomePrograma);
        
        // Gera código MVS
        geraCodigo(raiz);
    }
    ;

cabecalho
    : T_PROGRAMA T_IDENTIF
    {
        strcpy(nomePrograma, $2->valor);
        $$ = $2;
    }
    ;

variaveis
    :
    {
        $$ = NULL;
    }
    | declaracao_variaveis
    ;

declaracao_variaveis
    : tipo lista_variaveis declaracao_variaveis
    {
        ptno n = criaNo(DDV, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $2);
        adicionaFilho(n, $1);
        $$ = n;
    }
    | tipo lista_variaveis
    {
        ptno n = criaNo(DDV, "");
        adicionaFilho(n, $2);
        adicionaFilho(n, $1);
        $$ = n;
    }
    ;

tipo
    : T_LOGICO
    { 
        $$ = criaNo(TIP, "logico"); 
    }
    | T_INTEIRO
    { 
        $$ = criaNo(TIP, "inteiro"); 
    }
    ;

lista_variaveis
    : T_IDENTIF
    {
        ptno n = criaNo(LDV, "");
        adicionaFilho(n, $1);
        $$ = n;
    }
    | T_IDENTIF lista_variaveis 
    {
        ptno n = criaNo(LDV, "");
        adicionaFilho(n, $2);
        adicionaFilho(n, $1);
        $$ = n;
    }
    ;   

lista_comandos
    : 
    {
        $$ = NULL;
    }
    | comando lista_comandos
    {
        ptno n = criaNo(LDC, "");
        adicionaFilho(n, $2);
        adicionaFilho(n, $1);
        $$ = n;
    }
    ;

comando
    : leitura
    { $$ = $1; }
    | escrita
    { $$ = $1; }
    | repeticao
    { $$ = $1; }
    | selecao
    { $$ = $1; }
    | atribuicao
    { $$ = $1; }
    ;

leitura 
    : T_LEIA T_IDENTIF 
    {
        ptno n = criaNo(LER, "");
        adicionaFilho(n, $2);
        $$ = n;
    } 
    ;

escrita 
    : T_ESCREVA expressao 
    {
        ptno n = criaNo(ESC, "");
        adicionaFilho(n, $2);
        $$ = n;
    } 
    ;

repeticao 
    : T_ENQTO expressao T_FACA lista_comandos T_FIMENQTO 
    {
        ptno n = criaNo(REP, "");
        adicionaFilho(n, $4);
        adicionaFilho(n, $2);
        $$ = n;
    } 
    ;

selecao 
    : T_SE expressao T_ENTAO lista_comandos T_SENAO lista_comandos T_FIMSE
    {
        ptno n = criaNo(SEL, "");
        adicionaFilho(n, $6);
        adicionaFilho(n, $4);
        adicionaFilho(n, $2);
        $$ = n;
    } 
    ;

atribuicao 
    : T_IDENTIF T_ATRIB expressao 
    {
        ptno n = criaNo(ATR, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $1);
        $$ = n;
    }
    ;

expressao
    : expressao T_OU expressao
    {
        ptno n = criaNo(OU, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $1);
        $$ = n;
    }
    | expressao T_E expressao
    {
        ptno n = criaNo(E, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $1);
        $$ = n;
    }
    | expressao T_IGUAL expressao
    {
        ptno n = criaNo(IGUAL, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $1);
        $$ = n;
    }
    | expressao T_MAIOR expressao
    {
        ptno n = criaNo(MAI, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $1);
        $$ = n;
    }
    | expressao T_MENOR expressao
    {
        ptno n = criaNo(MEN, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $1);
        $$ = n;
    }
    | expressao T_MAIS expressao
    {
        ptno n = criaNo(SUM, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $1);
        $$ = n;
    }
    | expressao T_MENOS expressao
    {
        ptno n = criaNo(SUB, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $1);
        $$ = n;
    }
    | expressao T_VEZES expressao
    {
        ptno n = criaNo(MULT, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $1);
        $$ = n;
    }
    | expressao T_DIV expressao
    {
        ptno n = criaNo(DIV, "");
        adicionaFilho(n, $3);
        adicionaFilho(n, $1);
        $$ = n;
    }
    | T_NAO expressao
    {
        ptno n = criaNo(NAO, "");
        adicionaFilho(n, $2);
        $$ = n;
    }
    | termo 
    ;

termo
    : T_IDENTIF 
    {
        ptno n = $1;
        n->tipo = VAR;
        $$ = n;
    }
    | T_NUMERO
    { $$ = $1; }
    | T_V
    { $$ = criaNo(BOOL, "V"); }
    | T_F
    { $$ = criaNo(BOOL, "F"); }
    | T_ABRE expressao T_FECHA
    { $$ = $2; }
    ;

%%

int main(int argc, char **argv) {
    char nameIn[100], nameOut[100], *p;
    
    if (argc < 2) {
        printf("Uso:\n\t%s <nome_programa>[.simples]\n\n", argv[0]);
        exit(1);
    }
    
    p = strstr(argv[1], ".simples");
    if (p) *p = 0;
    
    strcpy(nameIn, argv[1]);
    strcpy(nameOut, argv[1]);
    strcpy(nomePrograma, argv[1]);

    strcat(nameIn, ".simples");
    strcat(nameOut, ".mvs");
    
    yyin = fopen(nameIn, "rt");
    if (!yyin) {
        printf("Erro ao abrir arquivo de entrada: %s\n", nameIn);
        exit(1);
    }
    
    yyout = fopen(nameOut, "wt");
    if (!yyout) {
        printf("Erro ao criar arquivo de saída: %s\n", nameOut);
        exit(1);
    }

    yyparse();
    
    fclose(yyin);
    fclose(yyout);
    
    printf("Compilação concluída com sucesso!\n");
    printf("Arquivos gerados:\n");
    printf("  - %s.dot\n", nomePrograma);
    printf("  - %s.svg\n", nomePrograma);
    printf("  - %s.mvs\n", nomePrograma);
    
    return 0;
}