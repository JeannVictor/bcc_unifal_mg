#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Estruturas
typedef struct estudante_ {
    int matricula;
    char nome[30];
} estudante;

typedef struct hash_ {
    int qtd, TABLE_SIZE;
    estudante **estudantes;
} hash;

// Funções de hash
int chave_divisao(int chave, int TABLE_SIZE) {
    if (chave < 0) chave *= -1;
    return chave % TABLE_SIZE;
}

int chave_multiplicacao(int chave, int TABLE_SIZE) {
    if (chave < 0) chave *= -1;
    double A = 0.7834729723;
    double val = chave * A;
    val = val - (int)val;
    return (int)(val * TABLE_SIZE);
}

int chave_dobra(int chave, int TABLE_SIZE) {
    if (chave < 0) chave *= -1;
    if (chave < TABLE_SIZE) return chave;

    int numeros[10];
    int inicio = 0;
    int fim = 0;
    int div = chave;
    
    do {
        int resto = div % 10;
        numeros[inicio] = resto;
        if (numeros[inicio]) fim = inicio;
        inicio++;
        div = div / 10;
    } while (inicio < 10);
    
    inicio = 0;
    while (chave > TABLE_SIZE) {
        while (fim > inicio) {
            numeros[inicio] = (numeros[inicio] + numeros[fim]) % 10;
            numeros[fim] = 0;
            inicio++;
            fim--;
        }
        inicio = 0;
        chave = 0;
        int fator = 1;
        while (inicio <= fim) {
            chave += numeros[inicio] * fator;
            fator *= 10;
            inicio++;
        }
        inicio = 0;
    }
    return chave;
}

// Funções de tratamento de colisão
int sondagem_linear(int pos, int i, int TABLE_SIZE) {
    return ((pos + i) % TABLE_SIZE);
}

int sondagem_quadratica(int pos, int i, int TABLE_SIZE) {
    pos = pos + 2 * i + 5 * i * i;
    return (pos % TABLE_SIZE);
}

int duplo_hash(int H1, int chave, int i, int TABLE_SIZE) {
    int H2 = chave_divisao(chave, TABLE_SIZE - 1) + 1;
    return ((H1 + i * H2) % TABLE_SIZE);
}

// Funções principais da tabela hash
estudante* cria_estudante(char* nome, int matricula) {
    estudante* e = malloc(sizeof(estudante));
    e->matricula = matricula;
    strncpy(e->nome, nome, strlen(nome));
    e->nome[strlen(nome)] = '\0';
    return e;
}

hash* cria_hash(int TABLE_SIZE) {
    hash* ha = malloc(sizeof(hash));
    if (ha != NULL) {
        ha->estudantes = malloc(TABLE_SIZE * sizeof(estudante*));
        if (ha->estudantes == NULL) {
            free(ha);
            return NULL;
        }
        ha->TABLE_SIZE = TABLE_SIZE;
        ha->qtd = 0;
        for (int i = 0; i < TABLE_SIZE; i++) {
            ha->estudantes[i] = NULL;
        }
    }
    return ha;
}

void libera_hash(hash* ha) {
    if (ha != NULL) {
        for (int i = 0; i < ha->TABLE_SIZE; i++) {
            if (ha->estudantes[i] != NULL)
                free(ha->estudantes[i]);
        }
        free(ha->estudantes);
        free(ha);
    }
}

int insere_hash_end_aberto(hash* ha, estudante* e) {
    if (ha == NULL || ha->qtd == ha->TABLE_SIZE) {
        return 0;
    }
    
    int pos = chave_dobra(e->matricula, ha->TABLE_SIZE);
    
    for (int i = 0; i < ha->TABLE_SIZE; i++) {
        pos = duplo_hash(pos, e->matricula, i, ha->TABLE_SIZE);
        if (ha->estudantes[pos] == NULL) {
            ha->estudantes[pos] = e;
            ha->qtd++;
            return 1;
        }
    }
    return 0;
}

char* busca_hash_end_aberto(hash* ha, int matricula) {
    int pos = chave_dobra(matricula, ha->TABLE_SIZE);
    
    for (int i = 0; i < ha->TABLE_SIZE; i++) {
        pos = duplo_hash(pos, matricula, i, ha->TABLE_SIZE);
        if (ha->estudantes[pos] == NULL) {
            return NULL;
        } else if (ha->estudantes[pos]->matricula == matricula) {
            return ha->estudantes[pos]->nome;
        }
    }
    return NULL;
}

// Função principal com menu
int main() {
    int opcao, matricula;
    char nome[30];
    hash* ha = cria_hash(1000);
    
    do {
        printf("\n=== MENU DE OPERAÇÕES COM HASH ===\n");
        printf("1. Inserir estudante\n");
        printf("2. Buscar estudante\n");
        printf("3. Mostrar quantidade de elementos\n");
        printf("0. Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);
        
        switch (opcao) {
            case 1:
                printf("Digite a matrícula do estudante: ");
                scanf("%d", &matricula);
                printf("Digite o nome do estudante: ");
                getchar(); // Limpa o buffer
                fgets(nome, 30, stdin);
                nome[strcspn(nome, "\n")] = '\0'; // Remove o \n do final
                
                estudante* e = cria_estudante(nome, matricula);
                if (insere_hash_end_aberto(ha, e)) {
                    printf("Estudante inserido com sucesso!\n");
                } else {
                    printf("Erro ao inserir estudante!\n");
                    free(e);
                }
                break;
                
            case 2:
                printf("Digite a matrícula do estudante: ");
                scanf("%d", &matricula);
                char* nome_encontrado = busca_hash_end_aberto(ha, matricula);
                if (nome_encontrado != NULL) {
                    printf("Estudante encontrado: %s\n", nome_encontrado);
                } else {
                    printf("Estudante não encontrado!\n");
                }
                break;
                
            case 3:
                printf("Quantidade de elementos na tabela: %d\n", ha->qtd);
                break;
                
            case 0:
                printf("Encerrando o programa...\n");
                break;
                
            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    } while (opcao != 0);
    
    libera_hash(ha);
    return 0;
}