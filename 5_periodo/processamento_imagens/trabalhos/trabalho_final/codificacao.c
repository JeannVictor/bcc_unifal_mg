/*
 * Disciplina: Processamento de Imagens
 * Professor : Luiz Eduardo
 * Aluno     : Jeann Victor Batista
 *
 * Trabalho  : Codificação e Decodificação de Contornos (Código de Cadeia)
 *
 * codificacao.c — Parte II do trabalho.
 *
 * Responsável por transformar o contorno de um objeto, presente em uma
 * imagem PBM binária, na sua representação compacta:
 *   1) Localização do ponto inicial do contorno;
 *   2) Rastreamento do contorno (vizinhança 8-direcional);
 *   3) Conversão da sequência de direções para binário;
 *   4) Compactação do binário em hexadecimal e gravação em arquivo.
 */

#include "codigo_cadeia.h"

const ponto DESLOCAMENTOS_DIRECAO[8] = {
    {0, 1}, {-1, 1}, {-1, 0}, {-1, -1},
    {0, -1}, {1, -1}, {1, 0}, {1, 1}
};

imagem_t ler_imagem_pbm(const char* nome_arquivo, dados_contorno* dados) {
    FILE* arquivo = fopen(nome_arquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo PBM.\n");
        return NULL;
    }

    char numero_magico[256];
    if (fscanf(arquivo, "%255s", numero_magico) != 1 || strcmp(numero_magico, "P1") != 0) {
        printf("Erro: formato PBM inválido (esperado P1).\n");
        fclose(arquivo);
        return NULL;
    }

    /* Descarta comentários (#...) e espaços em branco antes das dimensões */
    int caractere_lido;
    while ((caractere_lido = fgetc(arquivo)) != EOF) {
        if (caractere_lido == '#') {
            while ((caractere_lido = fgetc(arquivo)) != EOF && caractere_lido != '\n');
        } else if (caractere_lido != ' ' && caractere_lido != '\t' && caractere_lido != '\n' && caractere_lido != '\r') {
            ungetc(caractere_lido, arquivo);
            break;
        }
    }

    /* No formato PBM as dimensões vêm como <colunas> <linhas> (largura x altura) */
    if (fscanf(arquivo, "%d %d", &dados->numero_colunas, &dados->numero_linhas) != 2) {
        printf("Erro ao ler dimensões do PBM.\n");
        fclose(arquivo);
        return NULL;
    }

    imagem_t imagem = (imagem_t)malloc(dados->numero_linhas * dados->numero_colunas * sizeof(int));
    if (imagem == NULL) {
        printf("Erro ao alocar memória para a imagem.\n");
        fclose(arquivo);
        return NULL;
    }

    for (int i = 0; i < dados->numero_linhas * dados->numero_colunas; i++) {
        if (fscanf(arquivo, "%d", &imagem[i]) != 1) {
            printf("Erro ao ler pixel %d do PBM.\n", i);
            free(imagem);
            fclose(arquivo);
            return NULL;
        }
    }

    fclose(arquivo);
    return imagem;
}

bool validar_pixel(int linha, int coluna, dados_contorno* dados) {
    return (linha >= 0 && linha < dados->numero_linhas && coluna >= 0 && coluna < dados->numero_colunas);
}

bool eh_contorno(dados_contorno* dados, imagem_t imagem, int linha, int coluna) {
    if (!validar_pixel(linha, coluna, dados) || imagem[linha * dados->numero_colunas + coluna] != 1) {
        return false;
    }

    for (int k = 0; k < 8; k++) {
        int linha_vizinho = linha + DESLOCAMENTOS_DIRECAO[k].i;
        int coluna_vizinho = coluna + DESLOCAMENTOS_DIRECAO[k].j;
        if (validar_pixel(linha_vizinho, coluna_vizinho, dados) &&
            imagem[linha_vizinho * dados->numero_colunas + coluna_vizinho] == 0) {
            return true; /* Tem ao menos um vizinho de fundo (0): é um pixel de contorno */
        }
    }
    return false;
}

bool pontos_iguais(ponto p1, ponto p2) {
    return (p1.i == p2.i && p1.j == p2.j);
}

void localizar_ponto_inicial(dados_contorno* dados, imagem_t imagem) {
    for (int i = 0; i < dados->numero_linhas; i++) {
        for (int j = 0; j < dados->numero_colunas; j++) {
            if (imagem[i * dados->numero_colunas + j] == 1 && eh_contorno(dados, imagem, i, j)) {
                dados->linha_inicial = i;
                dados->coluna_inicial = j;
                return;
            }
        }
    }
    dados->linha_inicial = -1;
    dados->coluna_inicial = -1;
}

/* Define a ordem em que os 8 vizinhos serão testados a partir do pixel atual.
 * A busca recomeça logo após a direção de onde se veio, andando no sentido
 * horário, garantindo que o contorno seja percorrido de forma consistente. */
void altera_ordem_busca(int* ordem_busca, int ultima_direcao) {
    int inicio = (ultima_direcao + 3) % 8;
    for (int k = 0; k < 8; k++) {
        ordem_busca[k] = (inicio - k + 8) % 8;
    }
}

int* rastrear_contorno(dados_contorno* dados, imagem_t imagem) {
    int capacidade = dados->numero_linhas * dados->numero_colunas;
    int* ordem_direcoes = malloc(capacidade * sizeof(int));
    int qtd_direcoes = 0;
    int total_colunas = dados->numero_colunas;

    if (ordem_direcoes == NULL) {
        printf("Erro ao alocar memória para ordem_direcoes.\n");
        return NULL;
    }

    localizar_ponto_inicial(dados, imagem);
    if (dados->linha_inicial == -1 || dados->coluna_inicial == -1) {
        printf("Nenhum pixel de contorno encontrado na imagem.\n");
        free(ordem_direcoes);
        return NULL;
    }

    int ordem_busca[8] = {0, 7, 6, 5, 4, 3, 2, 1};

    ponto ponto_inicial = {dados->linha_inicial, dados->coluna_inicial};
    ponto ponto_atual = ponto_inicial;
    ponto segundo_ponto;
    ponto proximo_ponto;
    int ultima_direcao = -1;
    int encontrou_primeiro_vizinho = 0;

    /* Busca o primeiro vizinho de contorno a partir do ponto inicial */
    for (int k = 0; k < 8; k++) {
        int codigo_direcao = ordem_busca[k];
        proximo_ponto.i = ponto_atual.i + DESLOCAMENTOS_DIRECAO[codigo_direcao].i;
        proximo_ponto.j = ponto_atual.j + DESLOCAMENTOS_DIRECAO[codigo_direcao].j;

        if (validar_pixel(proximo_ponto.i, proximo_ponto.j, dados) &&
            imagem[proximo_ponto.i * total_colunas + proximo_ponto.j] == 1 &&
            eh_contorno(dados, imagem, proximo_ponto.i, proximo_ponto.j)) {

            ultima_direcao = codigo_direcao;
            segundo_ponto = proximo_ponto;
            ordem_direcoes[qtd_direcoes++] = ultima_direcao;
            ponto_atual = proximo_ponto;
            encontrou_primeiro_vizinho = 1;
            break;
        }
    }

    if (!encontrou_primeiro_vizinho) {
        printf("Não foi encontrado vizinho de contorno a partir do ponto inicial.\n");
        return ordem_direcoes;
    }

    /* Percorre o restante do contorno até fechar o laço no ponto inicial
     * (critério de parada de Jacob: voltar ao ponto inicial pela mesma
     * direção usada na primeira vez). */
    int terminou = 0;
    while (!terminou) {
        altera_ordem_busca(ordem_busca, ultima_direcao);

        for (int k = 0; k < 8; k++) {
            int codigo_direcao = ordem_busca[k];
            proximo_ponto.i = ponto_atual.i + DESLOCAMENTOS_DIRECAO[codigo_direcao].i;
            proximo_ponto.j = ponto_atual.j + DESLOCAMENTOS_DIRECAO[codigo_direcao].j;

            if (!validar_pixel(proximo_ponto.i, proximo_ponto.j, dados) ||
                imagem[proximo_ponto.i * total_colunas + proximo_ponto.j] != 1 ||
                !eh_contorno(dados, imagem, proximo_ponto.i, proximo_ponto.j)) {
                continue;
            }

            ultima_direcao = codigo_direcao;

            if (pontos_iguais(ponto_atual, ponto_inicial) && pontos_iguais(proximo_ponto, segundo_ponto)) {
                terminou = 1;
                break;
            }

            ordem_direcoes[qtd_direcoes++] = ultima_direcao;
            ponto_atual = proximo_ponto;
            break;
        }
    }

    dados->numero_direcoes = qtd_direcoes;
    return ordem_direcoes;
}

char* direcoes_para_binario(int* ordem_direcoes, int qtd_direcoes) {
    if (ordem_direcoes == NULL || qtd_direcoes <= 0) {
        return NULL;
    }

    int tamanho_total = (qtd_direcoes * 3) + 1;
    char* direcoes_em_binario = malloc(tamanho_total * sizeof(char));
    if (direcoes_em_binario == NULL) {
        printf("Erro ao alocar memória.\n");
        return NULL;
    }
    direcoes_em_binario[0] = '\0';

    static const char* BITS_POR_DIRECAO[8] = {
        "000", "001", "010", "011", "100", "101", "110", "111"
    };

    for (int i = 0; i < qtd_direcoes; i++) {
        int direcao = ordem_direcoes[i];
        if (direcao < 0 || direcao > 7) {
            printf("Direção inválida: %d\n", direcao);
            free(direcoes_em_binario);
            return NULL;
        }
        strcat(direcoes_em_binario, BITS_POR_DIRECAO[direcao]);
    }

    return direcoes_em_binario;
}

char converter_4bits_para_hex(char* bits_4) {
    const char* tabela_binario_para_hex[16] = {
        "0", "1", "2", "3", "4", "5", "6", "7",
        "8", "9", "A", "B", "C", "D", "E", "F"
    };

    int valor = 0;
    for (int i = 0; i < 4; i++) {
        valor = (valor << 1) | (bits_4[i] - '0');
    }

    return tabela_binario_para_hex[valor][0];
}

char* binario_para_hexadecimal(char* direcoes_em_binario) {
    if (direcoes_em_binario == NULL || strlen(direcoes_em_binario) == 0) {
        return NULL;
    }

    int tamanho_binario = strlen(direcoes_em_binario);
    int resto_num_binario = tamanho_binario % 4;

    char* bin_com_padding;
    if (resto_num_binario != 0) {
        int total_bits = tamanho_binario + (4 - resto_num_binario);
        bin_com_padding = malloc((total_bits + 1) * sizeof(char));
        strcpy(bin_com_padding, direcoes_em_binario);
        int zeros = 4 - resto_num_binario;
        for (int i = 0; i < zeros; i++) {
            bin_com_padding[tamanho_binario + i] = '0';
        }
        bin_com_padding[total_bits] = '\0';
    } else {
        bin_com_padding = malloc((tamanho_binario + 1) * sizeof(char));
        if (bin_com_padding == NULL) {
            return NULL;
        }
        strcpy(bin_com_padding, direcoes_em_binario);
    }

    int tamanho_hex = strlen(bin_com_padding) / 4;
    char* cadeia_hexadecimal = malloc((tamanho_hex + 1) * sizeof(char));
    if (cadeia_hexadecimal == NULL) {
        free(bin_com_padding);
        return NULL;
    }
    cadeia_hexadecimal[0] = '\0';

    for (int i = 0; i < (int)strlen(bin_com_padding); i += 4) {
        char bloco_4_bits[5];
        for (int k = 0; k < 4; k++) {
            bloco_4_bits[k] = bin_com_padding[i + k];
        }
        bloco_4_bits[4] = '\0';
        cadeia_hexadecimal[i / 4] = converter_4bits_para_hex(bloco_4_bits);
    }
    cadeia_hexadecimal[tamanho_hex] = '\0';

    free(bin_com_padding);
    return cadeia_hexadecimal;
}

void criar_arquivo_saida(int numero_linhas, int numero_colunas, int linha_inicial,
                          int coluna_inicial, int numero_direcoes, char* hexadecimal) {
    const char* nome_arquivo = "contorno_codificado.txt";

    FILE* arquivo = fopen(nome_arquivo, "w");
    if (arquivo == NULL) {
        printf("Erro ao criar o arquivo %s.\n", nome_arquivo);
        return;
    }

    fprintf(arquivo, "%d %d\n", numero_linhas, numero_colunas);
    fprintf(arquivo, "%d %d\n", linha_inicial, coluna_inicial);
    fprintf(arquivo, "%d\n", numero_direcoes);
    fprintf(arquivo, "%s\n", hexadecimal);

    fclose(arquivo);
}

void executar_codificacao(dados_contorno* dados, imagem_t imagem) {
    int* direcoes = rastrear_contorno(dados, imagem);
    if (direcoes == NULL) {
        return;
    }

    char* direcoes_em_binario = direcoes_para_binario(direcoes, dados->numero_direcoes);
    char* cadeia_hexadecimal = binario_para_hexadecimal(direcoes_em_binario);
    if (cadeia_hexadecimal == NULL) {
        printf("Erro: não foi possível converter a cadeia para hexadecimal.\n");
        free(direcoes);
        free(direcoes_em_binario);
        return;
    }

    criar_arquivo_saida(dados->numero_linhas, dados->numero_colunas, dados->linha_inicial,
                         dados->coluna_inicial, dados->numero_direcoes, cadeia_hexadecimal);

    free(direcoes);
    free(direcoes_em_binario);
    free(cadeia_hexadecimal);
}
