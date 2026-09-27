/*
 * Disciplina: Processamento de Imagens
 * Professor : Luiz Eduardo
 * Aluno     : Jeann Victor Batista
 *
 * Trabalho  : Codificação e Decodificação de Contornos (Código de Cadeia)
 *
 * main.c — Ponto de entrada do programa.
 *
 *   1) codificar()               -> Parte II: gera o código de cadeia de uma imagem;
 *   2) decodificar()             -> Parte I : reconstrói a imagem a partir do código de cadeia;
 *   3) codificar_e_decodificar() -> executa as duas etapas em sequência, para validação.
 */

#include "codigo_cadeia.h"

static const char* ARQUIVO_IMAGEM_ENTRADA = "imagem_teste.pbm";
static const char* ARQUIVO_CODIGO_CADEIA = "contorno_codificado.txt";
static const char* ARQUIVO_IMAGEM_RECONSTRUIDA = "imagem.pbm";

/* Parte II — lê uma imagem PBM e grava o código de cadeia correspondente. */
static void codificar(void) {
    printf("--- CODIFICAÇÃO (Parte II) ---\n");
    printf("Lendo imagem PBM...\n");

    dados_contorno dados_originais = {0};
    imagem_t imagem_original = ler_imagem_pbm(ARQUIVO_IMAGEM_ENTRADA, &dados_originais);

    if (imagem_original == NULL) {
        printf("ERRO: Não foi possível ler a imagem '%s'\n", ARQUIVO_IMAGEM_ENTRADA);
        printf("Certifique-se que o arquivo existe no diretório.\n");
        return;
    }

    printf("Imagem carregada: %d x %d\n", dados_originais.numero_linhas, dados_originais.numero_colunas);

    printf("\nCodificando o contorno...\n");
    executar_codificacao(&dados_originais, imagem_original);

    printf("\nCODIFICAÇÃO CONCLUÍDA!\n");
    printf("Arquivo gerado: %s\n\n", ARQUIVO_CODIGO_CADEIA);

    free(imagem_original);
}

/* Parte I — lê o código de cadeia e reconstrói a imagem do contorno. */
static void decodificar(void) {
    printf("--- DECODIFICAÇÃO (Parte I) ---\n");
    printf("Lendo arquivo codificado...\n");

    dados_contorno dados_codificados = ler_arquivo_codificado(ARQUIVO_CODIGO_CADEIA);

    if (dados_codificados.cadeia_hexadecimal == NULL) {
        printf("ERRO: Não foi possível ler o arquivo '%s'\n", ARQUIVO_CODIGO_CADEIA);
        return;
    }

    printf("Arquivo lido com sucesso!\n");
    printf("Dimensões: %d x %d\n", dados_codificados.numero_linhas, dados_codificados.numero_colunas);
    printf("Ponto inicial: (%d, %d)\n", dados_codificados.linha_inicial, dados_codificados.coluna_inicial);
    printf("Número de direções: %d\n", dados_codificados.numero_direcoes);
    printf("Cadeia hexadecimal: %s\n", dados_codificados.cadeia_hexadecimal);

    printf("\nReconstruindo a imagem...\n");
    executar_decodificacao(dados_codificados);

    printf("\nDECODIFICAÇÃO CONCLUÍDA!\n");
    printf("Arquivo gerado: %s\n\n", ARQUIVO_IMAGEM_RECONSTRUIDA);

    free(dados_codificados.cadeia_hexadecimal);
}

/* Executa a codificação e, em seguida, a decodificação, para validar o processo completo. */
static void codificar_e_decodificar(void) {
    codificar();
    decodificar();

    printf("--- COMPARAÇÃO ---\n");
    printf("Compare as imagens:\n");
    printf("  Original:      %s\n", ARQUIVO_IMAGEM_ENTRADA);
    printf("  Reconstruída:  %s\n", ARQUIVO_IMAGEM_RECONSTRUIDA);
    printf("==================================================\n");
}

int main(void) {
    printf("==================================================\n");
    printf("   CODIGO DE CADEIA - CODIFICACAO E DECODIFICACAO\n");
    printf("==================================================\n\n");

    printf("Escolha uma opção:\n");
    printf("  1 - Codificar   (le %s e gera %s)\n", ARQUIVO_IMAGEM_ENTRADA, ARQUIVO_CODIGO_CADEIA);
    printf("  2 - Decodificar (le %s e gera %s)\n", ARQUIVO_CODIGO_CADEIA, ARQUIVO_IMAGEM_RECONSTRUIDA);
    printf("  3 - Codificar e decodificar (executa as duas etapas em sequencia)\n");
    printf("Opção: ");

    int opcao_escolhida = 0;
    if (scanf("%d", &opcao_escolhida) != 1) {
        printf("Opção inválida.\n");
        return 1;
    }

    switch (opcao_escolhida) {
        case 1:
            codificar();
            break;
        case 2:
            decodificar();
            break;
        case 3:
            codificar_e_decodificar();
            break;
        default:
            printf("Opção inválida.\n");
            return 1;
    }

    return 0;
}
