#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include "ex12.h"
// Função para verificar se o ano é bissexto
bool bissexto(int ano) {
    return (ano % 4 == 0 && ano % 100 != 0) || (ano % 400 == 0);
}
// Função para atribuir as respectivas quantidade de dias dos meses
int diasNoMes(int mes, int ano) {
    switch(mes) {
        case 4: case 6: case 9: case 11:
            return 30;
        case 2:
            return bissexto(ano) ? 29 : 28;
        default:
            return 31;
    }
}

// Função usada para ler o arquivo
int lerArquivo(pessoa dados[], const char *nomeArquivo) {
    FILE *arquivo;
    char linha[300];
    int totalpessoas = 0;

    arquivo = fopen(nomeArquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nomeArquivo);
        return 0;
    }

    while (fgets(linha, sizeof(linha), arquivo) && totalpessoas < MAX_PESSOAS) {
        linha[strcspn(linha, "\n")] = 0; // Remove o caractere de nova linha
        if (strstr(linha, "FIM") != NULL) break;

        // Encontrar os dados (últimos três campos numéricos) no final da linha
        int dia, mes, ano;
        char nomeCompleto[100] = "";

        int lidos = sscanf(
            linha,
            "%[^0-9] %d %d %d", // Lê até encontrar números
            nomeCompleto, &dia, &mes, &ano);

        if (lidos == 4) {
            // Remover espaços extras no final do nome
            nomeCompleto[strcspn(nomeCompleto, "\0") - 1] = '\0';
            strcpy(dados[totalpessoas].nome, nomeCompleto);
            dados[totalpessoas].dia = dia;
            dados[totalpessoas].mes = mes;
            dados[totalpessoas].ano = ano;
            totalpessoas++;
        } else {
            printf("Erro ao processar a linha (esperado: Nome DD MM AAAA):\n'%s'\n", linha);
        }
    }

    fclose(arquivo);
    return totalpessoas;
}

// Função utilizada para salvar o arquivo
void salvarArquivo(pessoa dados[], int totalpessoas, const char* nomeArquivo) {
    FILE *arquivo = fopen(nomeArquivo, "w");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s para escrita\n", nomeArquivo);
        return;
    }

    for (int i = 0; i < totalpessoas; i++) {
            fprintf(
                arquivo,
                "%s %d %d %d\n",
                dados[i].nome,
                dados[i].dia,
                dados[i].mes,
                dados[i].ano);
        }

    fprintf(arquivo, "FIM\n");
    fclose(arquivo);
    }
// Função para calcular a idade da pessoa atraves da data de nascimento.
void idade(int diaD,int mesD,int anoD,int diaATUAL,int mesATUAL,int anoATUAL){
    int dias = 0,meses = 0,anos = 0;
    // Caso em que o mês atual é antes do mês do aniversario
    if(mesATUAL < mesD){
        // Tratamento para dia/mês(aproximado)
        if(diaD >= diaATUAL){ // Caso o dia do aniversario for depois do dia atual
            int diasMesAnterior = diasNoMes(mesATUAL == 1 ? 12 : mesATUAL - 1, anoATUAL);
            dias = diaATUAL - diaD + diasMesAnterior;
            if(dias == diasMesAnterior){
                meses = mesATUAL - mesD + 12;
                dias = 0;
            }else
               meses = mesATUAL - mesD + 11;
        // Caso o dia do aniversario for antes do dia atual        
        }else{               
            dias = diaATUAL - diaD;
            meses = mesATUAL - mesD + 12;
        }

        // Tratamento para ano
        anos = anoATUAL - anoD - 1;
    }

    // Caso em que o mês atual é o mês do aniversario
    if(mesATUAL == mesD)
    {
        if(diaATUAL >= diaD){
            // Tratamento para dia(aproximado)
            dias = diaATUAL - diaD;
            //Tratamento para mês
            meses = 0;
            // Tratamento para ano
            anos = anoATUAL - anoD;      
        }else{
            // Tratamento para dia
            int diasMesAnterior = diasNoMes(mesATUAL == 1 ? 12 : mesATUAL - 1, anoATUAL);
            dias = diasMesAnterior + diaATUAL - diaD  ;
            //Tratamento para mês
            meses = 11;
            // Tratamento para ano
            anos = anoATUAL - anoD - 1;
        }
        printf("Anos: %d,Meses:%d,Dias:%d\n",anos,meses,dias); 
    }
    // Caso em que o mês atual é depois do mês do aniversario
    if(mesATUAL > mesD){
        // Caso o dia do aniversario for depois do dia atual
        if(diaD >= diaATUAL){ 
            int diasMesAnterior = diasNoMes(mesATUAL == 1 ? 12 : mesATUAL - 1, anoATUAL);
            dias = diaATUAL - diaD + diasMesAnterior;
            if(dias == 30){
                meses = mesATUAL - mesD;
                dias = 0;
            }else{
               meses = mesATUAL - mesD -1; 
            }
        // Caso o dia do aniversario for antes do dia atual    
        }else{
            dias = diaATUAL - diaD;
            meses = mesATUAL - mesD;
        }
        // Tratamento para ano
        anos = anoATUAL - anoD;
    }
}

void diastotais(int diaD,int mesD,int anoD,int diaATUAL,int mesATUAL,int anoATUAL){
    int diasTotais = 0;
    // Adiciona dias dos anos completos
    for(int ano = anoD + 1; ano < anoATUAL; ano++) {
        if(bissexto(ano) == 1){
            diasTotais += 366;
        }else
            diasTotais += 365; 
    }
    
    // Adiciona dias dos meses restantes do ano de nascimento
    for(int mes = mesD + 1; mes <= 12; mes++) {
        diasTotais += diasNoMes(mes, anoD);
    }
    
    // Adiciona dias dos meses restantes do ano atual
    for(int mes = 1; mes < mesATUAL; mes++) {
        diasTotais += diasNoMes(mes, anoATUAL);
    }
    
    // Adiciona dias do mês de nascimento (parcial)
    diasTotais += diasNoMes(mesD, anoD) - diaD;
    
    // Adiciona dias do mês atual (parcial)
    diasTotais += diaATUAL;
    
    printf("Dias Totais: %d\n",diasTotais);
}

void adicionarpessoa(pessoa *dado, int *totalpessoas) {
    // Verifica se o limite de pessoas foi atingido.
    if (*totalpessoas >= MAX_PESSOAS) {
        printf("Limite do banco de dados atingido.\n");
        return;
    }

    pessoa novaPessoa;

    // Dados da nova pessoa
    printf("Forneça os dados da nova pessoa!\n");
    
    printf("Nome: ");
    fgets(novaPessoa.nome, sizeof(novaPessoa.nome), stdin);
    novaPessoa.nome[strcspn(novaPessoa.nome, "\n")] = 0;
    if (strlen(novaPessoa.nome) == 0) {
        printf("Entrada encerrada pelo usuário.\n");
        return;
    }

    printf("Dia: ");
    scanf("%d", &novaPessoa.dia);
    while (novaPessoa.dia < 1 || novaPessoa.dia > 31) {
        printf("Digite um dia válido (1 a 31)!\n");
        scanf("%d", &novaPessoa.dia);
    }
    while (getchar() != '\n'); // Limpa o buffer

    printf("Mês: ");
    scanf("%d", &novaPessoa.mes);
    while (novaPessoa.mes < 1 ||  novaPessoa.mes > 12) {
        printf("Digite um mês válido (1 a 12)!\n");
        scanf("%d", &novaPessoa.dia);
    }
    while (getchar() != '\n'); // Limpa o buffer

    printf("Ano: ");
    scanf("%d", &novaPessoa.ano);
    while (getchar() != '\n'); // Limpa o buffer

    dado[*totalpessoas] = novaPessoa;
    (*totalpessoas)++;

    printf("Pessoa adicionada com sucesso!\n");
}

// Função para realizar a busca no banco de dados pelo nome
void buscarPessoaporNome(pessoa dado[], int *totalpessoas) {
    int diaA = 0,mesA = 0,anoA = 0;
    char pessoa[100];
    int existe = 0, opcao;

    // Obter a placa a ser buscada
    printf("Digite o nome da pessoa para buscá-lo: ");
    fgets(pessoa, sizeof(pessoa), stdin);
    pessoa[strcspn(pessoa, "\n")] = 0;

    // Loop para busca e desejo de idade
    for (int i = 0; i < *totalpessoas; i++) {
        if (strcmp(dado[i].nome, pessoa) == 0) {
            existe = 1;
            printf("A pessoa de nome %s foi encontrado no banco de dados!\n", dado[i].nome);
            printf("Você gostaria de saber a idade da pessoa? (1 = SIM, 0 = NÃO): ");
            scanf("%d", &opcao);
            while (getchar() != '\n'); // Limpa o buffer

            // Caso a pessoa deseje saber a idade
            if (opcao == 1) {

                // Obtendo data atual.
                time_t t = time(NULL);
                struct tm *dataAtual = localtime(&t);

                // Obtendo o dia, mês e ano
                int diaATUAL = dataAtual->tm_mday;
                int mesATUAL = dataAtual->tm_mon + 1; 
                int anoATUAL = dataAtual->tm_year + 1900; 
                
                // Cálculos para descobrir idade da pessoa
                idade(dado[i].dia,dado[i].mes,dado[i].ano,diaATUAL,mesATUAL,anoATUAL);
                diastotais(dado[i].dia,dado[i].mes,dado[i].ano,diaATUAL,mesATUAL,anoATUAL);

                return;
            // Caso a pessoa não deseje saber a idade.
            } else 
                return;
        }
    }

    if (!existe) 
        printf("O nome da pessoa digitada não foi encontrado no banco de dados.\n");
}


    
