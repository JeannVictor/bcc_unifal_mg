#include "ProjGameofTrones.h"

/*
Calcula a centralidade de betwenness de cada vértice do grafo.
@param grafo: matriz de adjacência do grafo
@param n: número de vértices do grafo
@return vetor com a centralidade de betwenness de cada vértice
*/
double *brandesBetwenness(int **grafo, int n){
    double *betwenness = calloc(n, sizeof(double));
    int pilhaS[n], tamPilhaS; //pilha de vértices da solução do algoritmo de Dijkstra

    /*Árvore minHeap organizada de acordo 
    com as distâncias dos vértices até o vértice fonte s.
    psoHeapQ armazena as posições de cada vérice na heap,
    necessário para atualização das prioridades dos vértices*/
    int heapQ[n], tamHeapQ, posHeapQ[n];

    //lista de adjacência em forma de matriz dos predecessores de cada vértice
    int predcess[n][n-1]; 
    int nPredcess[n]; //número de predecessores de cada vértice
    int nCaminhoCurto[n]; //número de caminhos curtos que passam por cada vértice
    int dist[n]; //distância do vértice fonte s até cada vértice
    

    for (int s=0; s<n; s++){
        tamPilhaS = 0;
        tamHeapQ = 0;

        //inicializa
        for (int t=0; t<n; t++){
            for (int i=0; i<n-1; i++)
                predcess[t][i] = 0;
            nPredcess[t] = 0;
            nCaminhoCurto[t] = 0;
            dist[t] = __INT32_MAX__;
            posHeapQ[t] = -1;
        }

        nCaminhoCurto[s] = 1;
        dist[s] = 0;

        /*árvore minHeap organizada de acordo 
        com as distâncias dos vértices até o vértice fonte s*/
        insereHeap(heapQ, posHeapQ, s, &tamHeapQ, dist);

        //Dijkstra
        while(tamHeapQ > 0){
            int v = removeMin(heapQ, posHeapQ, &tamHeapQ, dist);
            pilhaS[tamPilhaS++] = v;
            
            for (int w = 0; w<n; w++){
                //intera sobre os visinhos de v
                if (grafo[v][w]!=0){
                    //Algoritmo de relaxa que detecta caminhos míminos de pesos iguais
                    if (dist[w] > dist[v] + grafo[v][w]){
                        dist[w] = dist[v] + grafo[v][w];
                        /*caso encontre outro caminho mínimo, 
                        reseta o número de caminhos curtos e os predecessores.
                        Também atualiza a árvore heap com a nova distância do vértice*/
                        nCaminhoCurto[w] = nCaminhoCurto[v];
                        nPredcess[w] = 1;
                        predcess[w][0] = v;
                        insereHeap(heapQ, posHeapQ, w, &tamHeapQ, dist); 
                    }
                    else if (dist[w] == dist[v] + grafo[v][w]){ 
                        /*se o caminho é mínimo, adiciona 
                        o número de caminhos curtos que passam por w*/
                        nCaminhoCurto[w] += nCaminhoCurto[v]; 
                        //adiciona o predecessor v na lista de predecessores de w
                        predcess[w][nPredcess[w]++] = v; 
                    }
                }
            }
        }
        //Acumulação
        double deltha[n]; //dependência de s em cada vértice para o cálculo da betwenness
        
        for (int i=0; i<n; i++) deltha[i] = 0;

        while (tamPilhaS>0){
            //desempilha o último vértice da pilha
            int w = pilhaS[--tamPilhaS]; 

            //intera sobre todos os predecessores de w
            for (int i = 0; i < nPredcess[w]; i++){
                int v = predcess[w][i];                
                deltha[v] += ((double)nCaminhoCurto[v]/nCaminhoCurto[w]) * (1+deltha[w]);                
            }  
            if (w != s)
                betwenness[w] += deltha[w];              
        }
    }
    /*O algoritmo conta ambos os sentidos separadamente,
    como o grafo é não direcionado, é necessário divir por 2*/
    for (int v = 0; v < n; v++) betwenness[v] /= 2.0; 
    return betwenness;
}