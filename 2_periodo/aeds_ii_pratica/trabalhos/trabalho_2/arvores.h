#ifndef _H_ARVORES
#define _H_ARVORES

// Implementar qualquer struct que for necessária aqui

double arvore_binaria(int instancia_num);
double arvore_balanceada(int instancia_num);

typedef struct noArvore_ noArvore;
struct noArvore_
{
    int valor;
    noArvore *esq;
    noArvore *dir;
    int altura;
};

typedef struct Operacao_ {
    char comando[2];
    int valor;
} operacao;

// Funções da Árvore Binária de Busca
noArvore *buscaI(noArvore *raiz, int k);
noArvore *buscaPaiI(noArvore *raiz, noArvore *n);
noArvore *insere(noArvore *raiz, noArvore *n);
noArvore *removeraiz(noArvore *raiz);
noArvore *removeNo(noArvore *raiz, int k);

// Funções da Árvore AVL
int altura(noArvore *N);
int max(int a, int b);
noArvore *novoNo(int valor);
noArvore *rotdir(noArvore *y);
noArvore *rotesq(noArvore *x);
int balance(noArvore *N);
noArvore *insereAVL(noArvore *no, int valor);
noArvore* menorNo(noArvore* no);
noArvore* removerNo(noArvore* raiz, int valor);

// Funções para abertura de arquivos + operações
int lerArquivoBIN(operacao array[], const char* nomeArquivo);
int lerArquivoAVL(operacao array[], const char* nomeArquivo);

#endif // _H_ARVORES