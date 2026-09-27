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
    
    #include "tree.c"
    #define YYSTYPE ptno  
    #include "sintatico.h"
    
    char atomo[100];
    int nLin = 1;  /* variavel para contar as linhas */
    int yyerror(char *);
%}    

identificador [a-zA-Z][a-zA-Z0-9]*
numero        [0-9]+
espaco        [ \t]+
novalinha     [\n]

%x coment

%%
programa                { return T_PROGRAMA; }
inicio                  { return T_INICIO; }
fimprograma             { return T_FIM; }
leia                    { return T_LEIA; }
escreva                 { return T_ESCREVA; }
se                      { return T_SE; }
entao                   { return T_ENTAO; }
senao                   { return T_SENAO; }
fimse                   { return T_FIMSE; }
enquanto                { return T_ENQTO; }
faca                    { return T_FACA; }
fimenquanto             { return T_FIMENQTO; }
"+"                     { return T_MAIS; }
"-"                     { return T_MENOS; }
"*"                     { return T_VEZES; }
"div"                   { return T_DIV; }
">"                     { return T_MAIOR; }
"<"                     { return T_MENOR; }
"="                     { return T_IGUAL; }
"e"                     { return T_E; }
"ou"                    { return T_OU; }
"nao"                   { return T_NAO; }
"<-"                    { return T_ATRIB; }
"("                     { return T_ABRE; }
")"                     { return T_FECHA; }
"inteiro"               { return T_INTEIRO; }
"logico"                { return T_LOGICO; }
"V"                     { return T_V; }
"F"                     { return T_F; }
"//".*                  /* nada */
"/*"                    BEGIN(coment);
<coment>"*/"            BEGIN(INITIAL);
<coment>.               /* nada */
<coment>"\n"            ++nLin;
{identificador}         {
                          yylval = criaNo(IDF, yytext);
                          strcpy(atomo, yytext);
                          return T_IDENTIF;
                        }
{numero}                {
                          yylval = criaNo(NUM, yytext);
                          return T_NUMERO;  
                        }
{espaco}                /* nada */ 
{novalinha}             ++nLin;
.                       yyerror("ERRO LEXICO - simbolo desconhecido!");

%%

int yywrap(void) { 
    return 1; 
}

int yyerror(char *s) {
    printf("\nErro na linha %d: %s próximo de %s\n\n", nLin, s, yytext);
    exit(10);
}