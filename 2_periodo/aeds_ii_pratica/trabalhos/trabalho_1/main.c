#include <stdio.h>
#include <stdlib.h>

#define MAX_LINHAS 100
#define MAX_COLUNAS 100

typedef struct pilha_ {
    int x;  // Linha
    int y;  // Coluna
    struct pilha_ *prox;
} pilha;

// Adicionar elemento a pilha 
void inserir(int xr, int yr, pilha **top) {
    pilha *new = malloc(sizeof(pilha));
    new->x = xr;
    new->y = yr;
    new->prox = *top;
    *top = new;
}

// Remover elemento da pilha
pilha *remover(pilha **top) {
    if (*top != NULL) {
        pilha *tmp = *top;
        *top = (*top)->prox;
        return tmp;
    }
    return NULL;
}

// Printar a pilha
void printa_pilha(pilha *topo) {
    if (topo == NULL) {
        printf("Pilha vazia!\n");
        return;
    }
    pilha *atual = topo;
    printf("\n=== CAMINHO ATÉ A SAÍDA ===\n");
    while (atual != NULL) {
        printf("%d,%d\n", atual->x, atual->y);
        atual = atual->prox;
    }
}

// Leitura do labirinto 
void lerLabirinto(const char *nomeArquivo, char labirinto[MAX_LINHAS][MAX_COLUNAS], int *linhas, int *colunas) {
    FILE *arquivo = fopen(nomeArquivo, "r");
    if (arquivo == NULL) {
        perror("Erro ao abrir o arquivo");
        exit(EXIT_FAILURE);
    }

    char linha[MAX_COLUNAS];
    int i = 0;
    while (fgets(linha, sizeof(linha), arquivo)) {
        int j = 0;
        while (linha[j] != '\n' && linha[j] != '\0') {
            labirinto[i][j] = linha[j];
            j++;
        }
        *colunas = j; // Número de colunas é igual ao comprimento da linha
        i++;
    }
    *linhas = i; // Número total de linhas

    fclose(arquivo);
}

// Impressão do labirinto
void imprimirLabirinto(char labirinto[MAX_LINHAS][MAX_COLUNAS], int linhas, int colunas) {
    for (int i = 0; i < linhas; i++) {
        for (int j = 0; j < colunas; j++) {
            printf("%c", labirinto[i][j]);
        }
        printf("\n");
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <nome_do_labirinto>\n", argv[0]);
        printf("Exemplo: %s labirintos/labirinto1.txt\n", argv[0]);
        return 1;
    }

    char labirinto[MAX_LINHAS][MAX_COLUNAS];
    int linhas, colunas;

    lerLabirinto(argv[1], labirinto, &linhas, &colunas);
    printf("Labirinto lido! (%dx%d):\n", linhas, colunas);
    imprimirLabirinto(labirinto, linhas, colunas);
    printf("\n");

    pilha *caminho = NULL;
    pilha *buraco = NULL;
    pilha *tmp;


    // Encontra o 'E' dentro do labirinto.
    int inicioX = -1, inicioY = -1;
    for (int i = 0; i < linhas; i++) {
        for (int j = 0; j < colunas; j++) {
            if (labirinto[i][j] == 'E') {
                inicioX = i;
                inicioY = j;
                break;
            }
        }
        if (inicioX != -1) break; 
    }

    if (inicioX == -1 || inicioY == -1) {
        printf("Erro: Entrada não encontrada no labirinto.\n");
        exit(EXIT_FAILURE);
    }

    // Insere a entrada na pilha.
    inserir(inicioX, inicioY, &caminho);

    // Começa a percorrer o labirinto.
    int S = 1; // Quando S for 0, a saída foi encontrada!
    int conta; // Conta o número de caminhos seguintes possíveis.
    int seg;   // Guarda a posição que será analisada.

    while (S == 1) {
        if (caminho == NULL) {
            printf("Erro: caminho vazio.\n");
            exit(EXIT_FAILURE);
        }

        conta = 0; // Reinicia o valor toda vez que o loop começa.
        int xa = caminho->x; // xa = x atual.
        int ya = caminho->y; // ya = y atual.

        // Caso de Posição Acima.
        if (xa > 0) {
            seg = labirinto[xa - 1][ya]; // Posição Acima.
            switch (seg) {
            case '0':
                inserir(xa - 1, ya, &buraco);
                conta++;
                break;
            case 'S':
                inserir(xa - 1, ya, &caminho);
                S = 0;
                conta++;
                break;
            }
        }

        // Caso de posição a esquerda.
        if (ya > 0) {
            seg = labirinto[xa][ya - 1]; // Posição à Esquerda.
            switch (seg) {
            case '0':
                inserir(xa, ya - 1, &buraco);
                conta++;
                break;
            case 'S':
                inserir(xa, ya - 1, &caminho);
                S = 0;
                conta++;
                break;
            }
        }

        // Caso de posição a direita.
        if (ya < colunas - 1) {
            seg = labirinto[xa][ya + 1]; // Posição a direita.
            switch (seg) {
            case '0':
                inserir(xa, ya + 1, &buraco);
                conta++;
                break;
            case 'S':
                inserir(xa, ya + 1, &caminho);
                S = 0;
                conta++;
                break;
            }
        }

        // Caso de posição abaixo.
        if (xa < linhas - 1) {
            seg = labirinto[xa + 1][ya]; // Posição abaixo.
            switch (seg) {
            case '0':
                inserir(xa + 1, ya, &buraco);
                conta++;
                break;
            case 'S':
                inserir(xa + 1, ya, &caminho);
                S = 0;
                conta++;
                break;
            }
        }

        if (S == 1) {
            switch (conta) {
            case 1: // Caso onde só é possivel um caminho. 
                labirinto[xa][ya] = 'J';
                tmp = remover(&buraco);
                if (tmp != NULL) inserir(tmp->x, tmp->y, &caminho);
                break;

            case 2: // Caso onde são possiveis dois caminhos.
                labirinto[xa][ya] = 'J';
                tmp = remover(&buraco);
                if (tmp != NULL) inserir(tmp->x, tmp->y, &caminho);
                inserir(xa, ya, &buraco);
                break;

            case 0: // Caso onde não possui nenhum caminho.
                if (buraco == NULL) {
                    printf("Erro: sem caminhos restantes.\n");
                    exit(EXIT_FAILURE);
                }
                while (caminho->x != buraco->x || caminho->y != buraco->y) {
                    tmp = remover(&caminho);
                    free(tmp);
                }
                remover(&buraco);
                tmp = remover(&buraco);
                if (tmp != NULL) inserir(tmp->x, tmp->y, &caminho);
                break;
            }
        }
    }

    // Deixa a pilha "buraco" vazia para a transferir o caminho correto para ela.
    while (buraco != NULL) {
        tmp = remover(&buraco);
        free(tmp);
    }

    // Transferência da pilha caminho para buraco, para que a ordem de exibição esteja na ordem correta.
    while (caminho != NULL) {
        tmp = remover(&caminho);
        inserir(tmp->x, tmp->y, &buraco);
        free(tmp);
    }

    // Impressão da entrada até a saída do labirinto.
    printa_pilha(buraco);
    
    return 0;
}
