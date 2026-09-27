#include "ProjGameofTrones.h"
#include <time.h>

int main() {

    FILE *arq = fopen("A-Storm-of-Swords.txt", "r");
    if (arq == NULL) {
        perror("Erro ao abrir o arq");
        return EXIT_FAILURE;
    }
    // Ler o arq
    clock_t start, end;
    start = clock();
    char word[128];
    int posicao = 0;
    vetor *lista = iniciaVet(16);
    const int n = 10;
    const char *personagens[] = {
        "Arya", "Bran", "Brienne", "Catelyn", "Cersei", 
        "Jaime", "Sam", "Sansa", "Tyrion", "Varys"
    };
    

    /*Ler o arq e comparar com os personagens
      Se o personagem estiver no arq, armazena 
      a posição e o personagem em uma lista*/   
    while (fscanf(arq, " %127s", word) != EOF){
        for (int i=0; i < n; i++){
            if (compSemPontu(word, personagens[i])){   
                posicoes p;            
                p.nome = i;
                p.posicao = posicao;
                insereVet(lista, p);
            }
        }
        posicao++;
    }   
    fclose(arq);


    //Calcula a matriz de relações de personagens de acordo com a posição, -100 a +100    
    int **matrizRelacoes = malloc(n * sizeof(int *));
    matrizRelacoes[0] = calloc(n*n, sizeof(int));
    for (int i = 1; i < n; i++) 
        matrizRelacoes[i] = matrizRelacoes[0] + i * n;
    
        

    for (int i=0; i<lista->tam; i++){
        for (int j = i-1; j>=0 && ((lista->elm[i].posicao)-(lista->elm[j].posicao))<=100; j--){
            matrizRelacoes[lista->elm[i].nome][lista->elm[j].nome]++;
        }
        for (int j = i+1; j<lista->tam && ((lista->elm[j].posicao)-(lista->elm[i].posicao))<=100; j++){
            matrizRelacoes[lista->elm[i].nome][lista->elm[j].nome]++;
        }    
    }
    //Os personagens não podem ter relação com eles mesmos
    for (int i=0; i<n; i++) matrizRelacoes[i][i]=0;

    /*Cria o arquivo CSV e escreve os cabeçalhos com 
    a matriz de relações.Também imprime no console*/
    arq  = fopen("grafo.csv", "w");
    printf("   Nomes");
    for (int i = 0; i < n; i++) {
        fprintf(arq, ",%7s", personagens[i]);
        printf("%7s", personagens[i]);

    }
    fputc('\n', arq);
    putchar('\n');
    for (int i = 0; i < n; i++) {
        printf("%7s", personagens[i]);
        fprintf(arq, "%7s", personagens[i]);
        for (int j = 0; j < n; j++) {           
            fprintf(arq, ",%7d", matrizRelacoes[i][j]);
            printf("%7d", matrizRelacoes[i][j]);
        }
        fputc('\n', arq);
        putchar('\n');
    }
    fclose(arq);

    //Encontra dos valores maximo e minimo dos pesos do grafo
    int min = __INT32_MAX__, max = 0, temp;   
    for (int i=0; i<n; i++){
        for (int j=0; j<n; j++){
            temp = matrizRelacoes[i][j];
            if (temp!=0){
                min = (temp<min) ? temp : min;
                max = (temp>max) ? temp : max;
            }
        }
    }
    //Inverte os valores da matriz utilizando o método de inversão linear: x' = max+min - x
    printf("min: %d, max: %d\n", min, max);
    int inversor = min + max;
    for (int i=0; i<n; i++){
        for (int j=0; j<n; j++){
            temp = matrizRelacoes[i][j];
            if (temp != 0) 
                matrizRelacoes[i][j] = inversor - temp;  
        }
    }


    double *bet = brandesBetwenness(matrizRelacoes, n);
    puts("\nBetweenness centralidade:");
    for (int i = 0; i < n; i++) {
        printf("Personagem %s: %lf\n", personagens[i],2*bet[i]/((n-1)*(n-2)));//bet[i]
    }


    int nConexos = nCompoConexos(matrizRelacoes, n);
    int nArestas = 0;
    for (int i=0; i<n; i++)
        for (int j=0; j<n; j++)
            if (matrizRelacoes[i][j]!=0) nArestas++;

    printf("\nNúmero de componentes conexos: %d\n", nConexos);
    printf("Número de arestas: %d\n", nArestas);
    printf("Circuit rank: %d\n", nArestas - n + nConexos);
    
    end = clock();

    double tempo = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Nomes encontrados: %d\n", lista->tam);
    printf("\nTempo gasto para processar: %lf seconds\n", tempo);

    free(matrizRelacoes[0]);     
    free(matrizRelacoes);
    free(lista->elm);
    free(lista);
    free(bet);

    return 0;
}