#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "arvores.h"

// Árvore Binária de Busca

// Função para buscar um nó em uma árvore binária de busca de forma iterativa.
noArvore *buscaI(noArvore *raiz, int k) {
    while (raiz != NULL && raiz->valor != k) {
        if (k > raiz->valor) {
            raiz = raiz->dir;
        } else {
            raiz = raiz->esq;
        }
    }
    return raiz;
}

// Função para buscar o pai de um determinado nó de forma iterativa.
noArvore *buscaPaiI(noArvore *raiz, noArvore *n) {
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

// Função para inserir um nó em uma árvore binária de busca.
noArvore *insere(noArvore *raiz, noArvore *n) {
    if (raiz == NULL) {
        return n;
    }
    if (n->valor < raiz->valor) {
        raiz->esq = insere(raiz->esq, n);
    } else if (n->valor > raiz->valor) {
        raiz->dir = insere(raiz->dir, n);
    }
    return raiz;
}

// Função para remover a raiz de uma árvore binária de busca.
noArvore *removeraiz(noArvore *raiz) {
    noArvore *p, *q;
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

// Função para remover um nó de uma árvore binária de busca.
noArvore *removeNo(noArvore *raiz, int k) {
    noArvore *n = buscaI(raiz, k);
    if (n) {
        noArvore *pai = buscaPaiI(raiz, n);
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

// Árvore AVL

// Função para obter a altura de um nó.
int altura(noArvore *N) {
    return (N == NULL) ? 0 : N->altura;
}

// Função para obter o maior valor entre dois inteiros.
int max(int a, int b) {
    return (a > b) ? a : b;
}

/* Função auxiliar para alocar um novo nó com o valor dado,
   e com os ponteiros para esquerda e direita nulos. */
noArvore *novoNo(int valor) {
    noArvore *no = (noArvore *)malloc(sizeof(noArvore));
    no->valor = valor;
    no->esq = NULL;
    no->dir = NULL;
    no->altura = 1; // O novo nó é inicialmente inserido como folha.
    return no;
}

// Função auxiliar para realizar uma rotação à direita em uma subárvore.
noArvore *rotdir(noArvore *y) {
    noArvore *x = y->esq;
    noArvore *tmp = x->dir;

    // Executa a rotação.
    x->dir = y;
    y->esq = tmp;

    // Atualiza as alturas.
    y->altura = max(altura(y->esq), altura(y->dir)) + 1;
    x->altura = max(altura(x->esq), altura(x->dir)) + 1;

    // Retorna a nova raiz.
    return x;
}

// Função auxiliar para realizar uma rotação à esquerda em uma subárvore.
noArvore *rotesq(noArvore *x) {
    noArvore *y = x->dir;
    noArvore *tmp = y->esq;

    // Executa a rotação.
    y->esq = x;
    x->dir = tmp;

    // Atualiza as alturas.
    x->altura = max(altura(x->esq), altura(x->dir)) + 1;
    y->altura = max(altura(y->esq), altura(y->dir)) + 1;

    // Retorna a nova raiz.
    return y;
}

// Função para obter o fator de balanceamento de um nó.
int balance(noArvore *N) {
    return (N == NULL) ? 0 : altura(N->esq) - altura(N->dir);
}

/* Função recursiva para inserir um valor em uma subárvore AVL.
   Retorna a nova raiz da subárvore. */
noArvore *insereAVL(noArvore *no, int valor) {
    // Inserção normal em uma árvore binária de busca.
    if (no == NULL) {
        return novoNo(valor);
    }

    if (valor < no->valor) {
        no->esq = insereAVL(no->esq, valor);
    } else if (valor > no->valor) {
        no->dir = insereAVL(no->dir, valor);
    } else {
        // Valores duplicados não são permitidos em uma árvore AVL.
        return no;
    }

    // Atualiza a altura do nó atual.
    no->altura = 1 + max(altura(no->esq), altura(no->dir));

    // Obtém o fator de balanceamento para verificar se o nó está desbalanceado.
    int balanco = balance(no);

    // Realiza rotações, se necessário.

    // Caso Esquerda-Esquerda.
    if (balanco > 1 && valor < no->esq->valor) {
        return rotdir(no);
    }

    // Caso Direita-Direita.
    if (balanco < -1 && valor > no->dir->valor) {
        return rotesq(no);
    }

    // Caso Esquerda-Direita.
    if (balanco > 1 && valor > no->esq->valor) {
        no->esq = rotesq(no->esq);
        return rotdir(no);
    }

    // Caso Direita-Esquerda.
    if (balanco < -1 && valor < no->dir->valor) {
        no->dir = rotdir(no->dir);
        return rotesq(no);
    }

    return no;
}

noArvore* menorNo(noArvore* no) {
    noArvore* atual = no;

    // Percorre para encontrar o nó mais à esquerda (menor valor).
    while (atual->esq != NULL)
        atual = atual->esq;

    return atual;
}

// Função recursiva para remover um nó com o valor especificado
// da subárvore com a raiz fornecida. Retorna a nova raiz da subárvore modificada.
noArvore* removerNo(noArvore* raiz, int valor) {
    // 1. Realiza a remoção padrão de uma BST (Árvore Binária de Busca).

    if (raiz == NULL)
        return raiz;

    // Se o valor a ser removido é menor que o valor da raiz,
    // continua na subárvore à esquerda.
    if (valor < raiz->valor)
        raiz->esq = removerNo(raiz->esq, valor);

    // Se o valor a ser removido é maior que o valor da raiz,
    // continua na subárvore à direita.
    else if (valor > raiz->valor)
        raiz->dir = removerNo(raiz->dir, valor);

    // Se o valor é igual ao valor da raiz,
    // este é o nó a ser removido.
    else {
        // Caso o nó tenha apenas um filho ou nenhum.
        if ((raiz->esq == NULL) || (raiz->dir == NULL)) {
            noArvore* temp = raiz->esq ? raiz->esq : raiz->dir;

            // Caso sem filhos.
            if (temp == NULL) {
                temp = raiz;
                raiz = NULL;
            } else { // Caso com um único filho.
                *raiz = *temp; // Copia o conteúdo do filho não nulo.
            }

            free(temp);
        } else {
            // Caso o nó tenha dois filhos: encontra o sucessor (menor valor na subárvore direita).
            noArvore* temp = menorNo(raiz->dir);

            // Copia o valor do sucessor para este nó.
            raiz->valor = temp->valor;

            // Remove o sucessor na subárvore direita.
            raiz->dir = removerNo(raiz->dir, temp->valor);
        }
    }

    // Se a árvore tinha apenas um nó, retorna a raiz.
    if (raiz == NULL)
        return raiz;

    // 2. Atualiza a altura do nó atual.
    raiz->altura = 1 + max(altura(raiz->esq), altura(raiz->dir));

    // 3. Obtém o fator de balanceamento do nó
    // para verificar se ele ficou desbalanceado.
    int balanco = balance(raiz);

    // Se o nó ficou desbalanceado, existem 4 casos.

    // Caso Esquerda-Esquerda.
    if (balanco > 1 && balance(raiz->esq) >= 0)
        return rotdir(raiz);

    // Caso Esquerda-Direita.
    if (balanco > 1 && balance(raiz->esq) < 0) {
        raiz->esq = rotesq(raiz->esq);
        return rotdir(raiz);
    }

    // Caso Direita-Direita.
    if (balanco < -1 && balance(raiz->dir) <= 0)
        return rotesq(raiz);

    // Caso Direita-Esquerda.
    if (balanco < -1 && balance(raiz->dir) > 0) {
        raiz->dir = rotdir(raiz->dir);
        return rotesq(raiz);
    }

    return raiz;
}

 int lerArquivoBIN(operacao array[], const char* nomeArquivo) {
    FILE *arquivo;
    char linha[300];
    int totalop = 0;
    noArvore *raiz = NULL;
    
    arquivo = fopen(nomeArquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nomeArquivo);
        return 0;
    }

    while (fgets(linha, sizeof(linha), arquivo) && totalop < 20000) {
        linha[strcspn(linha, "\n")] = 0;
        
        int lidos = sscanf(linha, " %1s %d", array[totalop].comando, &array[totalop].valor);
        
        if (lidos == 2) {
            if(array[totalop].comando[0] == 'I') {
                noArvore* novo = novoNo(array[totalop].valor);
                raiz = insere(raiz, novo);
            }
            
            if(array[totalop].comando[0] == 'R') {
                raiz = removeNo(raiz, array[totalop].valor);
            }
            totalop++;
        } else {
            printf("Erro ao processar a linha: %s\n", linha);
        }
    }

    fclose(arquivo);
    return totalop;
}

int lerArquivoAVL(operacao array[], const char* nomeArquivo) {
    FILE *arquivo;
    char linha[300];
    int totalop = 0;
    noArvore *raiz = NULL;
    
    arquivo = fopen(nomeArquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nomeArquivo);
        return 0;
    }

    while (fgets(linha, sizeof(linha), arquivo) && totalop < 20000) {
        linha[strcspn(linha, "\n")] = 0;
        
        int lidos = sscanf(linha, " %1s %d", array[totalop].comando, &array[totalop].valor);
        
        if (lidos == 2) {
            if(array[totalop].comando[0] == 'I') {
                raiz = insereAVL(raiz, array[totalop].valor);
            }
            
            if(array[totalop].comando[0] == 'R') {
                raiz = removerNo(raiz, array[totalop].valor);
            }
            totalop++;
        } else {
            printf("Erro ao processar a linha: %s\n", linha);
        }
    }

    fclose(arquivo);
    return totalop;
}
