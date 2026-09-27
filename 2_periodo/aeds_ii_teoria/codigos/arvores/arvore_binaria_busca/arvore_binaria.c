#include <stdlib.h>
#include <stdio.h>
#include <time.h>

typedef struct no no;
struct no {
    int valor;
    no *dir;
    no *esq;
};

no *insere(no *raiz, no *n) {
    if (raiz == NULL) {
        return n;
    }
    if (raiz->valor == n->valor) {
        printf("Erro: Valor duplicado não permitido.\n");
        free(n);
        return raiz;
    }
    if (raiz->valor > n->valor) {
        raiz->esq = insere(raiz->esq, n);
    } else {
        raiz->dir = insere(raiz->dir, n);
    }
    return raiz;
}
//-------------------------------------------------------------------------------
// Versão Recursiva da Busca
no *buscaR(no *raiz, int k) {
    if (raiz == NULL || raiz->valor == k) {
        return raiz;
    }
    if (raiz->valor > k) {
        return buscaR(raiz->esq, k);
    }
    return buscaR(raiz->dir, k);
}

// Versão Interativa da Busca
no *buscaI(no *raiz, int k) {
    while (raiz != NULL && raiz->valor != k) {
        if (k > raiz->valor) {
            raiz = raiz->dir;
        } else {
            raiz = raiz->esq;
        }
    }
    return raiz;
}

// Versão Recursiva da Busca Pai
no *buscaPaiR(no *raiz, no *n) {
    if (raiz == NULL || raiz == n) {
        return NULL;
    }
    if (raiz->esq == n || raiz->dir == n) {
        return raiz;
    }
    if (n->valor > raiz->valor) {
        return buscaPaiR(raiz->dir, n);
    }
    return buscaPaiR(raiz->esq, n);
}

// Versão Interativa da Busca Pai
no *buscaPaiI(no *raiz, no *n) {
    while (raiz != NULL && raiz != n) {
        if (raiz->esq == n || raiz->dir == n) {
            return raiz;
        }
        if (n->valor > raiz->valor) {
            raiz = raiz->dir;
        } else {
            raiz = raiz->esq;
        }
    }
    return NULL;
}
//-----------------------------------------------------------------------------
no *removeraiz(no *raiz) {
    no *p, *q;
    if (raiz->esq == NULL) {
        q = raiz->dir;
        free(raiz);
        return q;
    }
    p = raiz;
    q = raiz->esq;
    while (q->dir != NULL) {
        p = q;
        q = q->dir;
    }
    if (p != raiz) {
        p->dir = q->esq;
        q->esq = raiz->esq;
    }
    q->dir = raiz->dir;
    free(raiz);
    return q;
}

no *removeNo(no *raiz, int k) {
    no *n = buscaI(raiz, k);
    if (n) {
        no *pai = buscaPaiI(raiz, n);
        if (pai) {
            if (pai->dir == n) {
                pai->dir = removeraiz(n);
            } else {
                pai->esq = removeraiz(n);
            }
        } else {
            raiz = removeraiz(n);
        }
    }
    return raiz;
}
//------------------------------------------------------------------------------
void imprimePreOrdem(no *raiz) {
    if (raiz != NULL) {
        printf("Valor: %d\n", raiz->valor);
        imprimePreOrdem(raiz->esq);
        imprimePreOrdem(raiz->dir);
    }
}

void imprimeEmOrdem(no *raiz) {
    if (raiz != NULL) {
        imprimeEmOrdem(raiz->esq);
        printf("Valor: %d\n", raiz->valor);
        imprimeEmOrdem(raiz->dir);
    }
}

void imprimePosOrdem(no *raiz) {
    if (raiz != NULL) {
        imprimePosOrdem(raiz->esq);
        imprimePosOrdem(raiz->dir);
        printf("Valor: %d\n", raiz->valor);
    }
}
//-------------------------------------------------------------------------------
int verificaValor(no *raiz, int valor) {
    if (raiz == NULL) return 0;
    if (raiz->valor == valor) return 1;
    return verificaValor(raiz->esq, valor) || verificaValor(raiz->dir, valor);
}

int main() {
    int opcao, valor;
    no *raiz = NULL;

    srand(time(NULL));

    do {
        printf("\n=== MENU DE OPERAÇÕES ===\n");
        printf("1. Inserir elemento\n");
        printf("2. Remover elemento\n");
        printf("3. Imprimir Pré-Ordem\n");
        printf("4. Imprimir Em-Ordem\n");
        printf("5. Imprimir Pós-Ordem\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);

        switch (opcao) {
            case 1:
                printf("Digite o valor do novo elemento: ");
                scanf("%d", &valor);
                if (verificaValor(raiz, valor)) {
                    printf("Erro: Valor duplicado não permitido.\n");
                } else {
                    no *novo = malloc(sizeof(no));
                    novo->valor = valor;
                    novo->dir = NULL;
                    novo->esq = NULL;
                    raiz = insere(raiz, novo);
                    printf("Elemento inserido com sucesso!\n");
                }
                break;

            case 2:
                printf("Digite o valor do elemento a remover: ");
                scanf("%d", &valor);
                if (!verificaValor(raiz, valor)) {
                    printf("Erro: Elemento não encontrado!\n");
                } else {
                    raiz = removeNo(raiz, valor);
                    printf("Elemento removido com sucesso!\n");
                }
                break;

            case 3:
                printf("\n=== IMPRIMINDO EM PRÉ-ORDEM ===\n");
                imprimePreOrdem(raiz);
                break;

            case 4:
                printf("\n=== IMPRIMINDO EM ORDEM ===\n");
                imprimeEmOrdem(raiz);
                break;

            case 5:
                printf("\n=== IMPRIMINDO EM PÓS-ORDEM ===\n");
                imprimePosOrdem(raiz);
                break;

            case 0:
                printf("Encerrando o programa...\n");
                break;

            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while (opcao != 0);

    return 0;
}
