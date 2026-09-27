/*
 * Disciplina: Processamento de Imagens
 * Professor : Luiz Eduardo
 * Aluno     : Jeann Victor Batista
 *
 * Trabalho  : Codificação e Decodificação de Contornos
 *             usando Código de Cadeia (Chain Code) de Freeman, 8 direções.
 *
 * Este cabeçalho reúne os tipos de dados e as funções que são
 * compartilhados entre os arquivos codificacao.c, decodificacao.c e main.c.
 */

#ifndef CODIGO_CADEIA_H
#define CODIGO_CADEIA_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

/* Imagem binária representada como um vetor linear de 0s e 1s.
 * O pixel da linha "l" e coluna "c" fica na posição l * numero_colunas + c. */
typedef int* imagem_t;

/* Um ponto (coordenada) dentro da imagem. */
typedef struct {
    int i, j;
} ponto;

/* Guarda todas as informações de um contorno: dimensões da imagem,
 * ponto inicial, quantidade de direções percorridas e a cadeia já
 * compactada em hexadecimal. */
typedef struct {
    int numero_linhas;
    int numero_colunas;
    int linha_inicial;
    int coluna_inicial;
    int numero_direcoes;
    char* cadeia_hexadecimal;
} dados_contorno;

/* Deslocamento (linha, coluna) de cada uma das 8 direções do código de
 * cadeia de Freeman, na ordem 0=Leste, 1=Nordeste, ..., 7=Sudeste.
 * Definida uma única vez em codificacao.c e reaproveitada em todo o
 * projeto para evitar repetir essa tabela em cada função. */
extern const ponto DESLOCAMENTOS_DIRECAO[8];

/* codificacao.c — Parte II: gera o código de cadeia a partir de uma
 * imagem PBM contendo um contorno. */

imagem_t ler_imagem_pbm(const char* nome_arquivo, dados_contorno* dados);

bool validar_pixel(int linha, int coluna, dados_contorno* dados);
bool eh_contorno(dados_contorno* dados, imagem_t imagem, int linha, int coluna);
bool pontos_iguais(ponto p1, ponto p2);

void localizar_ponto_inicial(dados_contorno* dados, imagem_t imagem);
void altera_ordem_busca(int* ordem_busca, int ultima_direcao);
int* rastrear_contorno(dados_contorno* dados, imagem_t imagem);

char* direcoes_para_binario(int* ordem_direcoes, int qtd_direcoes);
char converter_4bits_para_hex(char* bits_4);
char* binario_para_hexadecimal(char* direcoes_em_binario);

void criar_arquivo_saida(int numero_linhas, int numero_colunas, int linha_inicial,
                          int coluna_inicial, int numero_direcoes, char* hexadecimal);

void executar_codificacao(dados_contorno* dados, imagem_t imagem);

/* decodificacao.c — Parte I: reconstrói o contorno a partir do código
 * de cadeia compactado em hexadecimal. */

dados_contorno ler_arquivo_codificado(const char* nome_arquivo);

int hex_para_inteiro(char digito_hexadecimal);
char* hex_para_binario_string(dados_contorno dados);
int* obter_direcoes(dados_contorno dados);

void reconstruir_contorno(dados_contorno dados, int* direcoes, imagem_t imagem);
void gerar_imagem_pbm(dados_contorno dados, imagem_t imagem);

void executar_decodificacao(dados_contorno dados);

#endif /* CODIGO_CADEIA_H */
