#include "ProjGameofTrones.h"

//“”—’,.?!;:()
/*
Função que verifica se o caractere é uma pontuação.
@param c: caractere a ser verificado
@return true se for pontuação, false caso contrário
*/
int ePontuacao(char c){
    switch (c){   
        case ',':
        case '.':
        case '?':
        case '!':
        case ';':
        case ':':
        case '(':
        case ')':   
            return true;
    }
    return false;
}

/*
Compara duas strings desconsiderando pontuações.
@param str1: primeira string a ser comparada
@param str2: segunda string a ser comparada
@return true se as strings são iguais desconsiderando pontuações, false caso contrário
*/
bool compSemPontu(char *str1, const char *str2) {
    while (*str1!='\0' && *str2 !='\0'){
        /*Caracteres utf-8 são caracteres 
          multybyte onde cada byte é um número negativo.
          Necessário para ignorar as pontuações: “ ” — ’ */
        if (*str1 < 0 || ePontuacao(*str1)){  
            str1++;
            continue;
        }
        if (*str1 != *str2){
            return false;
        }
        str1++;
        str2++;       
    }
    return (*str1 != '\0' || *str2 == '\0');
}

/*
Inicializa um vetor de posições.
@param tam_inicial: tamanho inicial do vetor
@return ponteiro para o vetor inicializado
*/
vetor *iniciaVet(int tam_inicial){
    vetor *vet = malloc(sizeof(vetor));
    vet->tam_alocado = tam_inicial;
    vet->tam = 0;
    vet->elm = malloc(tam_inicial * sizeof(posicoes));
    return vet;
}

/*
Insere um elemento no vetor de posições, redimensionando se necessário.
@param vet: ponteiro para o vetor
@param valor: valor a ser inserido
*/
void insereVet(vetor *vet, posicoes valor){
    int tam = vet->tam, tam_alocado = vet->tam_alocado;
    if (tam >= tam_alocado){       
        tam_alocado <<= 1; // Multiplica por 2
        vet->elm = realloc(vet->elm, tam_alocado * sizeof(posicoes));
        vet->tam_alocado = tam_alocado;       
    }    
    vet->elm[tam] = valor;
    vet->tam++;
}


/*
Sift up: sobe o vértice heap[i] na heap, atualizando as posições
@param heap: heap de vértices
@param pos: vetor de posições dos vértices na heap
@param i: índice do vértice a ser subido
@param dist: vetor de distâncias dos vértices
*/
void siftUp(int heap[], int pos[], int i, int dist[]) {
    while (i > 0) {
        int pai = (i - 1)>>1;
        if (dist[heap[i]] < dist[heap[pai]]) {
            // troca heap[i] com heap[pai]
            int tmp = heap[i];
            heap[i] = heap[pai];
            heap[pai] = tmp;

            // atualiza as posições
            pos[heap[i]] = i;
            pos[heap[pai]] = pai;

            i = pai;
        } else break;
    }
}

/*
Desce o vértice heap[i] na heap, atualizando as posições
@param heap: heap de vértices
@param pos: vetor de posições dos vértices na heap
@param i: índice do vértice a ser subido
@param dist: vetor de distâncias dos vértices
@param tamHeap: tamanho atual da heap
*/
void siftDown(int heap[], int pos[], int i, int tamHeap, int dist[]) {
    while (1) {
        int menor = i;
        int esq = (i<<1) + 1;
        int dir = (i<<1) + 2;

        if (esq < tamHeap && dist[heap[esq]] < dist[heap[menor]]) menor = esq;
        if (dir < tamHeap && dist[heap[dir]] < dist[heap[menor]]) menor = dir;

        if (menor != i) {
            int tmp = heap[i];
            heap[i] = heap[menor];
            heap[menor] = tmp;

            //atualiza as posições
            pos[heap[i]] = i;
            pos[heap[menor]] = menor;

            i = menor;
        } else break;
    }
}

/*
Insere um vértice na heap, caso o vértice não esteja na heap, 
ou atualiza a posição do vértice na heap, caso já esteja.
@param heap: heap de vértices
@param pos: vetor de posições dos vértices na heap
@param v: índice do vértice a ser inserido ou atualizado
@param tamHeap: tamanho atual da heap
@param dist: vetor de distâncias dos vértices
*/
void insereHeap(int heap[], int pos[], int v, int *tamHeap, int dist[]) {
    if (pos[v] == -1) {
        heap[*tamHeap] = v;
        pos[v] = *tamHeap;
        siftUp(heap, pos, *tamHeap, dist);
        (*tamHeap)++;
    } else {
        // Assume que dist[v] já foi atualizado
        siftUp(heap, pos, pos[v], dist);
    }
}

/*
Remove o menor vértice da heap e atualiza as posições
@param heap: heap de vértices
@param pos: vetor de posições dos vértices na heap
@param tamHeap: tamanho atual da heap
@param dist: vetor de distâncias dos vértices
@return o menor vértice da heap
*/
int removeMin(int heap[], int pos[], int *tamHeap, int dist[]) {
    int min = heap[0];
    pos[min] = -1;

    (*tamHeap)--;
    if (*tamHeap > 0) {
        heap[0] = heap[*tamHeap];
        pos[heap[0]] = 0;
        siftDown(heap, pos, 0, *tamHeap, dist);
    }
    return min;
}