#include "ProjGameofTrones.h"
/*
Algoritmo de busca em profundidade (DFS) para 
visitar todos os vértices visinhosdo grafo.
@param grafo: matriz de adjacência do grafo
@param n: número de vértices do grafo
@param visitado: vetor de booleanos que indica se o vértice foi visitado
@param u: vértice atual
*/
void dfsVisit(int **grafo, int n, bool *visitado, int u){
    visitado[u] = true;
    for (int v = 0; v < n; v++) 
        if (!visitado[v] && grafo[u][v] != 0)
            dfsVisit(grafo, n, visitado, v);
}

/*
Calcula o número de componentes conexos do grafo.
@param grafo: matriz de adjacência do grafo
@param n: número de vértices do grafo
@return número de componentes conexos do grafo
*/
int nCompoConexos(int **grafo, int n){
    bool visitado[n]; 
    int count = 0;
    for (int i = 0; i < n; i++)
        visitado[i] = false; 

    for (int u = 0; u < n; u++)
        if (!visitado[u]){
            dfsVisit(grafo, n, visitado, u);
            count++;
        }
    return count;
}