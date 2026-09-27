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

#ifndef FAT_H
#define FAT_H

#define TAM_GRANULO 3
#define TAM_MEMORIA 30
#define TRUE 1
#define FALSE 0

typedef struct noSet * ptnoSet;

typedef struct noSet {
    int inicio, fim;
    ptnoSet prox;
} noSet;

typedef struct noArq *ptnoArq;

typedef struct noArq {
    char nome[13];
    int caracteres;
    ptnoSet setores;
    ptnoArq prox;
} noArq;

typedef char memoria[TAM_MEMORIA][TAM_GRANULO];

// Funções de inicialização e visualização
void inicia(ptnoSet *Area, ptnoArq *Arq, memoria Memo);
void mostraSetores(ptnoSet S, char *n);
void mostraArquivos(ptnoArq A);
void mostraMemoria(memoria Memo);
void ajuda();

// Operações principais
void gravar(char *nome, char *texto, ptnoSet *areaLivre, ptnoArq *listaArquivos, memoria Memo);
void deletar(char *nome, ptnoArq *listaArquivos, ptnoSet *areaLivre, memoria Memo);
void apresentar(char *nome, ptnoArq *listaArquivos, memoria Memo);
void desfragmentar(ptnoArq *arquivos, ptnoSet *areaLivre, memoria Memo);

// Funções auxiliares
ptnoSet busca_aloca_setores(ptnoSet *areaLivre, int numSetoresNecessarios);
void grava_texto_memoria(memoria Memo, char *texto, ptnoSet setores);
void insere_arquivo(ptnoArq *listaArquivos, char *nome, int caracteres, ptnoSet setoresOcupados);
ptnoArq busca_arquivo(ptnoArq *listaArquivos, char *nome);
void liberar_um_setor(ptnoSet *areaLivre, ptnoSet setoresArquivo);
void liberar_todos_setores(ptnoSet *areaLivre, ptnoSet setoresArquivo);
void limpar_memoria_setores(memoria Memo, ptnoSet setores);
void remove_arquivo_lista(ptnoArq *listaArquivos, ptnoSet *areaLivre, char *nome, memoria Memo);

#endif