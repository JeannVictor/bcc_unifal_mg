#ifndef TP1_H
#define TP1_H

#define MAX_CAMPO 50
#define MAX_CARROS 100

typedef struct {
    char modelo[MAX_CAMPO];
    char marca[MAX_CAMPO];
    char tipo[MAX_CAMPO];
    int ano;
    int km;
    float potencia;
    char combustivel[MAX_CAMPO];
    char cambio[MAX_CAMPO];
    char direcao[MAX_CAMPO];
    char cor[MAX_CAMPO];
    int portas;
    char placa[MAX_CAMPO];
    float valor;
    int valido; // Indica se o carro está ativo no sistema
} Carro;

// Declaração de funções
int lerArquivo(Carro carro[], const char* nomeArquivo);
void salvarArquivo(Carro carro[], int totalcarros, const char* nomeArquivo);
void adicionarVeiculo(Carro carro[], int *totalcarros);
void buscarVeiculoPorPlaca(Carro carro[], int *totalcarros);
void buscarVeiculoPorTipo(Carro carro[], int totalcarros);
void buscarVeiculoPorCambio(Carro carro[], int totalcarros);
void buscarVeiculoPorIntervaloValor(Carro carro[], int totalcarros);
void gerarRelatorio(Carro carro[], int totalcarros);

#endif
