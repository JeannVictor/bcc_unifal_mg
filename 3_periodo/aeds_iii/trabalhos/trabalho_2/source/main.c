#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

// Struct para armazenar cada cidade.
typedef struct{
    int id;
    double x;
    double y;
}City;

// Função para calcular a distância euclidiana entre dois pontos. √((xb - xa)² + (yb-ya)²)
double calc_dist(City a, City b){
    double dx = b.x - a.x;
    double dy = b.y - a.y;

    return sqrt(dx * dx + dy * dy);
}

// Função auxiliar para trocar dois elementos
void troca(City *a, City *b) {
    City temp = *a;
    *a = *b;
    *b = temp;
}

// Função para calcular o custo total de um tour
double custo_tour(City *cities, int n) {
    double custo_total = 0;
    for (int i = 0; i < n - 1; i++) {
        custo_total += calc_dist(cities[i], cities[i+1]);
    }
    // Adiciona o custo de retornar à cidade inicial
    custo_total += calc_dist(cities[n-1], cities[0]);
    return custo_total;
}

// Função auxiliar para gerar permutações
void permutacao(City *cities, int comeco, int n, City *melhor_tour, double *custo_min) {
    if (comeco == n - 1) {
        double cost = custo_tour(cities, n);
        if (cost < *custo_min) {
            *custo_min = cost;
            memcpy(melhor_tour, cities, n * sizeof(City));
        }
        return;
    }
    
    for (int i = comeco; i < n; i++) {
        troca(&cities[comeco], &cities[i]);
        permutacao(cities, comeco + 1, n, melhor_tour, custo_min);
        troca(&cities[comeco], &cities[i]); // backtrack
    }
}

City* forca_bruta_CV(City* cities, int n) {
    City *melhor_tour = malloc(n * sizeof(City));
    memcpy(melhor_tour, cities, n * sizeof(City));
    
    double custo_min = INFINITY;
    permutacao(cities, 0, n, melhor_tour, &custo_min);
    
    return melhor_tour;
}
// Função de comparação para qsort (ordenação por coordenada X)
int compare_x(const void *a, const void *b) {
    City *cidade_a = (City *)a;
    City *cidade_b = (City *)b;
    
    if (cidade_a->x < cidade_b->x) return -1;
    if (cidade_a->x > cidade_b->x) return 1;
    return 0;
}
City* junta_tours(City *esq_tour, int lado_esq, City *dir_tour, int lado_dir) {
    int tam_total = lado_esq + lado_dir;
    City *junta_tour = malloc(tam_total * sizeof(City));
    
    // Variáveis para rastrear a melhor configuração
    double melhor_custo = INFINITY;
    int melhor_i_esq = 0, melhor_j_dir = 0;
    int melhor_direcao = 0;  // 0 ou 1 para as duas possíveis reconexões
    
    // Tenta todas as combinações de arestas
    for (int i = 0; i < lado_esq; i++) {
        // Pega a aresta (i, i+1) do tour da esquerda (com wrap-around)
        int prox_i = (i + 1) % lado_esq;
        
        for (int j = 0; j < lado_dir; j++) {
            // Pega a aresta (j, j+1) do tour da direita (com wrap-around)
            int prox_j = (j + 1) % lado_dir;
            
            // Calcula o custo da remoção das arestas atuais
            double custo_atual = calc_dist(esq_tour[i], esq_tour[prox_i]) + calc_dist(dir_tour[j], dir_tour[prox_j]);
                                  
            // Calcula os custos das duas possíveis reconexões
            double novo_custo1 = calc_dist(esq_tour[i], dir_tour[j]) + calc_dist(esq_tour[prox_i], dir_tour[prox_j]);
                              
            double novo_custo2 = calc_dist(esq_tour[i], dir_tour[prox_j]) + calc_dist(esq_tour[prox_i], dir_tour[j]);
            
            // Verificar primeira possibilidade
            if (novo_custo1 - custo_atual < melhor_custo) {
                melhor_custo = novo_custo1 - custo_atual;
                melhor_i_esq = i;
                melhor_j_dir = j;
                melhor_direcao = 0;
            }
            
            // Verificar segunda possibilidade
            if (novo_custo2 - custo_atual < melhor_custo) {
                melhor_custo = novo_custo2 - custo_atual;
                melhor_i_esq = i;
                melhor_j_dir = j;
                melhor_direcao = 1;
            }
        }
    }
    
    // Construir o tour mesclado usando a melhor configuração encontrada
    int index = 0;
    
    // Adiciona a primeira parte do tour da esquerda até melhor_i_esq
    for (int i = 0; i <= melhor_i_esq; i++) {
        junta_tour[index++] = esq_tour[i];
    }
    
    // Adiciona o tour da direita na direção apropriada
    if (melhor_direcao == 0) {
        // Direção normal
        for (int i = 0; i < lado_dir; i++) {
            int j = (melhor_j_dir + i + 1) % lado_dir;
            junta_tour[index++] = dir_tour[j];
        }
    } else {
        // Direção reversa
        for (int i = 0; i < lado_dir; i++) {
            int j = (melhor_j_dir - i + lado_dir) % lado_dir;
            junta_tour[index++] = dir_tour[j];
        }
    }
    
    // Adiciona o resto do tour da esquerda
    for (int i = melhor_i_esq + 1; i < lado_esq; i++) {
        junta_tour[index++] = esq_tour[i];
    }
    
    return junta_tour;
}

City* divisao_e_conquista(City* cities, int n) {
    if (n <= 3) {
        // Caso base: use força bruta
        return forca_bruta_CV(cities, n);
    }

    // Ordenar cidades por coordenada X
    qsort(cities, n, sizeof(City), compare_x);

    int meio = n / 2;

    City* esq = divisao_e_conquista(cities, meio);
    City* dir = divisao_e_conquista(cities + meio, n - meio);

    // Combinar as duas soluções
    City* mescla = junta_tours(esq, meio, dir, n - meio);
    
    // Liberar a memória das soluções parciais
    free(esq);
    free(dir);
    
    return mescla;
}

/*TODO: Implementação dos 3 algoritmos + matriz de distâncias*/

/************************************************************************************************************************************
*                                                  DESCRIÇÃO DO PROJETO                                                             
*                                                                                                                                   
*  Neste trabalho, foram implementados três diferentes algoritmos para a resolução do problema do Caixeiro Viajante, cada um        
*  obedecendo a um paradigma de projeto de algoritmos, sendo eles:                                                                  
*    - Backtracking                                                                                                                 
*    - Algoritmo Guloso                                                                                                             
*    - Programação Dinâmica                                                                                                         
*                                                                                                                                  
*  Os algoritmos podem ser avaliados por 20 instâncias diferentes da biblioteca TSPLIB, bastando o usuário passar o
*  nome do arquivo instância como argumento para a execução do projeto.
*
*  Obs: Não é necesário passar o caminho completo, apenas o nome da instância, o próprio código é capaz de buscar o caminho.
*                                                                                                                                   
*  Alunos: Thiago Martins | Pedro Augusto | Jeann Victor | Nicolas Rodrigues                                                        
************************************************************************************************************************************/


int main(int argc, char** argv){
    if(argc != 2){
        printf("\nA Quantidade de argumentos passada é inválida!");
        return 1;
    }
    
    char full_path[100] = "./instancias/";
    strcat(full_path, argv[1]);

    FILE *arch = fopen(full_path, "r");
    if(!arch){
        printf("\nO arquivo instância não foi aberto corretamente!");
        return 1;
    }

    int dimension = 0;
    char line[128];

    while( fgets(line, sizeof(line), arch)){
        if(strncmp(line, "DIMENSION", 9) == 0){
            sscanf(line, "DIMENSION: %d", &dimension);
        }
        if(strncmp(line, "NODE_COORD_SECTION", 18) == 0){
            break;
        }
    }

    if(dimension == 0){
        printf("\nErro: Dimensão não encontrada!");
        return 1;
    }

    City *cities = malloc(sizeof(City) * dimension);
    for(int i = 0; i < dimension; i++){
        fscanf(arch, "%d %lf %lf", &cities[i].id, &cities[i].x, &cities[i].y);
    }

    fclose(arch);

    // Alocação da matriz de distâncias, deve ser ** por se tratar de uma matriz, ou seja, precisa duplamente de alocação.
    double** dist = malloc(sizeof(double*) * dimension);
    for(int i = 0; i < dimension; i++){
        dist[i] = malloc(dimension * sizeof(double));
    }

    // Preenchendo a matriz de distâncias.
    for(int i = 0; i < dimension; i++){
        for(int j = 0; j < dimension; j++){
            dist[i][j] = calc_dist(cities[i], cities[j]);
        }
    }

    // Desalocando a alocação secudária da matriz de distâncias.
    for(int i = 0; i < dimension; i++){
        free(dist[i]);
    }

    //----------------------------------------------------------------------------------------------

    // Iniciar a medição do tempo
    clock_t inicio, fim;
    double tempo_execucao;
    
    inicio = clock();
    
    // Executar o algoritmo Divide and Conquer
    City *melhor_tour = divisao_e_conquista(cities, dimension);
    
    // Finalizar a medição do tempo
    fim = clock();
    tempo_execucao = ((double) (fim - inicio)) / CLOCKS_PER_SEC;

    // Calcular o custo do tour encontrado
    double custo_total = 0;
    for (int i = 0; i < dimension - 1; i++) {
        custo_total += calc_dist(melhor_tour[i], melhor_tour[i+1]);
    }
    // Adicionar o custo de retornar à primeira cidade
    custo_total += calc_dist(melhor_tour[dimension-1], melhor_tour[0]);

    // Exibir resultados
    printf("\nResultado do algoritmo Divide and Conquer:");
    printf("\nCusto total do tour: %.2f", custo_total);
    printf("\nTempo de execução: %.6f segundos\n", tempo_execucao);

    // Opcionalmente, exibir o tour completo
    printf("Tour encontrado: ");
    for (int i = 0; i < dimension; i++) {
        printf("%d ", melhor_tour[i].id);
    }
    printf("\n");

    //----------------------------------------------------------------------------------------------

    // Liberar a memória alocada pelo algoritmo
    free(melhor_tour);
    free(cities);
    free(dist);

    return 0;
}
