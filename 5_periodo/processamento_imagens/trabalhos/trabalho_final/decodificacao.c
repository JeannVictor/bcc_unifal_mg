/*
 * Disciplina: Processamento de Imagens
 * Professor : Luiz Eduardo
 * Aluno     : Jeann Victor Batista
 *
 * Trabalho  : Codificação e Decodificação de Contornos (Código de Cadeia)
 *
 * decodificacao.c — Parte I do trabalho.
 *
 * Responsável por reconstruir a imagem de um contorno a partir da sua
 * representação compacta (dimensões, ponto inicial, quantidade de
 * direções e cadeia hexadecimal).
 *
 * Passos implementados aqui:
 *   1) Leitura do arquivo com o contorno codificado;
 *   2) Conversão da cadeia hexadecimal de volta para binário;
 *   3) Recuperação da sequência de direções a partir do binário;
 *   4) Reconstrução do contorno pixel a pixel;
 *   5) Geração da imagem reconstruída em formato PBM.
 */

#include "codigo_cadeia.h"

/* Tabela de conversão de um dígito hexadecimal (0-15) para os seus 4 bits. */
static const char* tabela_hex_para_binario[] = {
    "0000", "0001", "0010", "0011",
    "0100", "0101", "0110", "0111",
    "1000", "1001", "1010", "1011",
    "1100", "1101", "1110", "1111"
};

static imagem_t alocar_imagem(int numero_linhas, int numero_colunas) {
    return (imagem_t)malloc(numero_linhas * numero_colunas * sizeof(int));
}

/* Passo 1 – Leitura do arquivo com o contorno codificado */
dados_contorno ler_arquivo_codificado(const char* nome_arquivo) {
    dados_contorno dados = {0};
    int quantidade_lida;
    FILE* arquivo;
    char cadeia_lida[1024]; /* buffer temporário para ler a cadeia do arquivo */

    arquivo = fopen(nome_arquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return dados;
    }

    quantidade_lida = fscanf(arquivo, "%d %d", &dados.numero_linhas, &dados.numero_colunas);
    if (quantidade_lida != 2) {
        printf("Erro ao ler linha e coluna.\n");
        fclose(arquivo);
        return dados;
    }
    quantidade_lida = fscanf(arquivo, "%d %d", &dados.linha_inicial, &dados.coluna_inicial);
    if (quantidade_lida != 2) {
        printf("Erro ao ler linha inicial e coluna inicial.\n");
        fclose(arquivo);
        return dados;
    }
    quantidade_lida = fscanf(arquivo, "%d", &dados.numero_direcoes);
    if (quantidade_lida != 1) {
        printf("Erro ao ler número de direções.\n");
        fclose(arquivo);
        return dados;
    }
    quantidade_lida = fscanf(arquivo, "%1023s", cadeia_lida);
    if (quantidade_lida != 1) {
        printf("Erro ao ler cadeia.\n");
        fclose(arquivo);
        return dados;
    }

    /* Aloca exatamente o tamanho necessário para a cadeia */
    dados.cadeia_hexadecimal = malloc(strlen(cadeia_lida) + 1);
    if (dados.cadeia_hexadecimal == NULL) {
        printf("Erro ao alocar memória para a cadeia.\n");
        fclose(arquivo);
        return dados;
    }
    strcpy(dados.cadeia_hexadecimal, cadeia_lida);

    fclose(arquivo);
    return dados;
}

/* Passo 2 – Conversão da cadeia hexadecimal para binário */
int hex_para_inteiro(char digito_hexadecimal) {
    if (digito_hexadecimal >= '0' && digito_hexadecimal <= '9') {
        return digito_hexadecimal - '0';
    } else if (digito_hexadecimal >= 'A' && digito_hexadecimal <= 'F') {
        return digito_hexadecimal - 'A' + 10;
    } else if (digito_hexadecimal >= 'a' && digito_hexadecimal <= 'f') {
        return digito_hexadecimal - 'a' + 10;
    } else {
        return -1;
    }
}

char* hex_para_binario_string(dados_contorno dados) {
    int tamanho = strlen(dados.cadeia_hexadecimal);
    char* binario = malloc(tamanho * 4 + 1);
    if (binario == NULL) {
        printf("Erro ao alocar memória para binário.\n");
        return NULL;
    }
    binario[0] = '\0';
    for (int i = 0; i < tamanho; i++) {
        int valor = hex_para_inteiro(dados.cadeia_hexadecimal[i]);
        if (valor >= 0 && valor <= 15) {
            strcat(binario, tabela_hex_para_binario[valor]);
        }
    }
    return binario;
}

/* Passo 3 – Recuperação da sequência de direções a partir do binário */
int* obter_direcoes(dados_contorno dados) {
    char* binario = hex_para_binario_string(dados);
    if (binario == NULL) {
        printf("Erro ao converter hexadecimal para binário.\n");
        return NULL;
    }
    int* direcoes = malloc(dados.numero_direcoes * sizeof(int));
    if (direcoes == NULL) {
        printf("Erro ao alocar memória para direções.\n");
        free(binario);
        return NULL;
    }

    char codigo_direcao[4];
    for (int i = 0; i < (dados.numero_direcoes * 3); i += 3) {
        for (int j = 0; j < 3; j++) {
            codigo_direcao[j] = binario[i + j];
        }
        codigo_direcao[3] = '\0';
        direcoes[i / 3] = strtol(codigo_direcao, NULL, 2);
    }
    free(binario);
    return direcoes;
}

/* Passo 4 – Reconstrução do contorno pixel a pixel */
void reconstruir_contorno(dados_contorno dados, int* direcoes, imagem_t imagem) {
    int linha_atual = dados.linha_inicial;
    int coluna_atual = dados.coluna_inicial;

    for (int i = 0; i < dados.numero_direcoes; i++) {
        imagem[linha_atual * dados.numero_colunas + coluna_atual] = 1;
        linha_atual += DESLOCAMENTOS_DIRECAO[direcoes[i]].i;
        coluna_atual += DESLOCAMENTOS_DIRECAO[direcoes[i]].j;
    }
    /* Marca o último pixel, destino da última direção percorrida */
    imagem[linha_atual * dados.numero_colunas + coluna_atual] = 1;
}

/* Passo 5 – Geração da imagem reconstruída em formato PBM */
void gerar_imagem_pbm(dados_contorno dados, imagem_t imagem) {
    FILE* arquivo = fopen("imagem.pbm", "w");
    if (arquivo == NULL) {
        printf("Erro ao criar o arquivo de imagem.\n");
        return;
    }

    fprintf(arquivo, "P1\n%d %d\n", dados.numero_colunas, dados.numero_linhas);

    for (int i = 0; i < dados.numero_linhas; i++) {
        for (int j = 0; j < dados.numero_colunas; j++) {
            fprintf(arquivo, "%d ", imagem[i * dados.numero_colunas + j]);
        }
        fprintf(arquivo, "\n");
    }

    fclose(arquivo);
}

/* Execução completa da decodificação (Parte I) */
void executar_decodificacao(dados_contorno dados) {
    int* direcoes = obter_direcoes(dados);
    if (direcoes == NULL) {
        printf("Erro ao obter direções.\n");
        return;
    }

    imagem_t imagem_reconstruida = alocar_imagem(dados.numero_linhas, dados.numero_colunas);
    if (imagem_reconstruida == NULL) {
        printf("Erro ao alocar memória para a imagem.\n");
        free(direcoes);
        return;
    }

    /* Inicializa todos os pixels com 0 */
    for (int i = 0; i < dados.numero_linhas * dados.numero_colunas; i++)
        imagem_reconstruida[i] = 0;

    reconstruir_contorno(dados, direcoes, imagem_reconstruida);
    free(direcoes);

    gerar_imagem_pbm(dados, imagem_reconstruida);

    free(imagem_reconstruida);
}
