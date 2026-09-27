#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Atividade 5: Vetor de Registros
// Autor: Jeann Victor Batista

#define MAX_AMIGOS 100
#define MAX_CAMPO 50

// Estrutura para representar um amigo
typedef struct {
    char nome[MAX_CAMPO];
    char celular[MAX_CAMPO];
    char cidade[MAX_CAMPO];
    char email[MAX_CAMPO];
    int valido;  // Flag para indicar se o registro é válido
} Amigo;

// Função para ler dados do arquivo
int lerArquivo(Amigo amigos[], const char* nomeArquivo) {
    FILE *arquivo;
    char linha[200];
    int totalAmigos = 0;

    arquivo = fopen(nomeArquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nomeArquivo);
        return 0;
    }

    while (fgets(linha, sizeof(linha), arquivo) && totalAmigos < MAX_AMIGOS) {
        linha[strcspn(linha, "\n")] = 0;

        char *token = strtok(linha, "|");
        if (token == NULL) continue;

        strcpy(amigos[totalAmigos].nome, token);
        token = strtok(NULL, "|");
        if (token == NULL) continue;
        strcpy(amigos[totalAmigos].celular, token);

        token = strtok(NULL, "|");
        if (token == NULL) continue;
        strcpy(amigos[totalAmigos].cidade, token);

        token = strtok(NULL, "|");
        if (token == NULL) continue;
        strcpy(amigos[totalAmigos].email, token);

        token = strtok(NULL, "|");
        if (token == NULL) continue;
        amigos[totalAmigos].valido = atoi(token);

        totalAmigos++;
    }

    fclose(arquivo);
    return totalAmigos;
}

// Função para salvar os dados no arquivo
void salvarArquivo(Amigo amigos[], int totalAmigos, const char* nomeArquivo) {
    FILE *arquivo;
    arquivo = fopen(nomeArquivo, "w");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s para escrita\n", nomeArquivo);
        return;
    }

    for (int i = 0; i < totalAmigos; i++) {
        if (amigos[i].valido) {
            fprintf(arquivo, "%s|%s|%s|%s|%d\n", 
                amigos[i].nome, 
                amigos[i].celular, 
                amigos[i].cidade, 
                amigos[i].email, 
                amigos[i].valido);
        }
    }

    fclose(arquivo);
}

int main() {
    // Declaração de váriaveis
    Amigo amigos[MAX_AMIGOS] = {0};
    int totalAmigos = 0;
    int e = 0;
    char name[MAX_CAMPO], number[MAX_CAMPO], city[MAX_CAMPO], gmail[MAX_CAMPO];


    totalAmigos = lerArquivo(amigos, "amigos.txt");

    do {
        printf("\n\n---AGENDA DE CONTATOS---\n");
        printf("0. Sair do programa\n");
        printf("1. Buscar um contato\n");
        printf("2. Excluir um contato\n");
        printf("3. Adicionar um contato\n");
        printf("Escolha uma opção: ");
        scanf(" %d", &e);
        while (getchar() != '\n'); // Limpa o buffer

        while (e < 0 || e > 3) {
            printf("Digite um número de operação válido.\n");
            scanf(" %d", &e);
            while (getchar() != '\n');
        }

        switch (e) {
            case 1:
                printf("Qual é o nome do contato que deseja procurar?\n");
                fgets(name, sizeof(name), stdin);
                name[strcspn(name, "\n")] = 0;

                int existe = 0;
                for (int i = 0; i < totalAmigos; i++) {
                    if (amigos[i].valido && strcmp(amigos[i].nome, name) == 0) {
                        printf("O contato procurado existe!\n");
                        printf("Nome: %s\n", amigos[i].nome);
                        printf("Celular: %s\n", amigos[i].celular);
                        printf("Cidade: %s\n", amigos[i].cidade);
                        printf("Email: %s\n", amigos[i].email);
                        existe = 1;
                    }
                }
                if (!existe) {
                    printf("O contato procurado não está na sua agenda.\n");
                }
                break;

            case 2:
                printf("Qual é o nome do contato que deseja remover?\n");
                fgets(name, sizeof(name), stdin);
                name[strcspn(name, "\n")] = 0;

                existe = 0;
                for (int i = 0; i < totalAmigos; i++) {
                    if (amigos[i].valido && strcmp(amigos[i].nome, name) == 0) {
                        amigos[i].valido = 0;
                        printf("O contato de nome %s foi excluído!\n", amigos[i].nome);
                        existe = 1;
                        break;
                    }
                }
                if (!existe) {
                    printf("O contato procurado não está na sua agenda.\n");
                }
                break;

            case 3:
                if (totalAmigos >= MAX_AMIGOS) {
                    printf("Limite de amigos atingido.\n");
                    break;
                }

                printf("Forneça os dados do novo contato!\n");
                printf("Nome: ");
                fgets(name, sizeof(name), stdin);
                name[strcspn(name, "\n")] = 0;

                int jaExiste = 0;
                for (int i = 0; i < totalAmigos; i++) {
                    if (amigos[i].valido && strcmp(amigos[i].nome, name) == 0) {
                        jaExiste = 1;
                        break;
                    }
                }

                if (jaExiste) {
                    printf("Erro: Um contato com esse nome já existe.\n");
                    break;
                }

                printf("Celular: ");
                fgets(number, sizeof(number), stdin);
                number[strcspn(number, "\n")] = 0;

                printf("Cidade: ");
                fgets(city, sizeof(city), stdin);
                city[strcspn(city, "\n")] = 0;

                printf("Email: ");
                fgets(gmail, sizeof(gmail), stdin);
                gmail[strcspn(gmail, "\n")] = 0;

                Amigo novoAmigo;
                strcpy(novoAmigo.nome, name);
                strcpy(novoAmigo.celular, number);
                strcpy(novoAmigo.cidade, city);
                strcpy(novoAmigo.email, gmail);
                novoAmigo.valido = 1;

                amigos[totalAmigos] = novoAmigo;
                totalAmigos++;

                printf("Amigo adicionado com sucesso!\n");
                break;
        }
    } while (e != 0);

    salvarArquivo(amigos, totalAmigos, "amigos.txt");

    return 0;
}
