#include <stdio.h>
#include <string.h>

// Exercício 3
// Autor: Jeann Victor Batista

// Estrutura Utilizada 
typedef struct {
    int matricula;
    float nota1;
    float nota2;
    float nota3;
    int frequencia;  
} dados;

// Função para leitura do arquivo
int lerArquivo(dados arr[], const char* nomeArquivo) {

    FILE *arquivo= fopen(nomeArquivo, "r");
    if (arquivo == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nomeArquivo);
        return 0;
    }

    char linha[300];
    int total = 0;

    while (fgets(linha, sizeof(linha), arquivo) && total < 100) {
        linha[strcspn(linha, "\n")] = 0;
        if (strstr(linha, "FIM") != NULL) break;

        int lidos = sscanf(linha,"%d %f %f %f %d ",&arr[total].matricula,&arr[total].nota1,
        &arr[total].nota2,&arr[total].nota3,&arr[total].frequencia);

        if (lidos == 5) {
            total++;
        } else {
            printf("Erro ao processar a linha: %s\n", linha);
        }
    }

    fclose(arquivo);
    return total;
}

int main() {
    dados arr[100];
    int totalLidos = lerArquivo(arr, "alunos.txt");

    // Váriaveis Utilizadas
    float maiornota = -1.0, menornota = 101.0, nota = 0, notamedia = 0; 
    int aprovado = 0,reprovado = 0,reprovadoF = 0,maiori = 0,menori = 0;
    
    for (int i = 0; i < totalLidos; i++) {

        // Nota Final de cada aluno
        float notafinal = (arr[i].nota1 + arr[i].nota2 + arr[i].nota3)/3;
        printf("Matricula %d - Nota Final: %.2f Frêquencia: %d\n", arr[i].matricula, notafinal,arr[i].frequencia);
    
        // Váriavel para cálculo de média
        notamedia += notafinal;

        // Cálculos para maior/menor nota
        if(notafinal > maiornota) {
            maiornota = notafinal;
            maiori = i;
        }
        if(notafinal < menornota) {
            menornota = notafinal;
            menori = i;
        }

        // Aprovação/reprovação
        if(arr[i].frequencia >= 40 && notafinal >= 60.0) {
            aprovado++;
        }
    
        // Se não passou em frequência OU não passou em nota, é reprovado
        if(arr[i].frequencia < 40 || notafinal < 60.0) {
            reprovado++;
        }
    
        // Conta separadamente quem reprovou por frequência, independente da nota
        if(arr[i].frequencia < 40) {
            reprovadoF++;
        }
    }

    // Cálculo da média
    notamedia = (notamedia/totalLidos);

    // Impressão dos resultados
    printf("\n------------------------------------------------------------------------------------\n");
    printf("A nota média da turma foi:%.2f\n",notamedia);
    printf("A maior nota foi do aluno de matricula %d com a nota %f\n",arr[maiori].matricula,maiornota);
    printf("A menor nota foi do aluno de matricula %d com a nota %f\n",arr[menori].matricula,menornota);
    printf("O total de aprovados da turma foi:%d\n",aprovado);
    printf("O total de reprovados da turma foi:%d\n",reprovado);
    printf("O total de reprovados por falta da turma foi:%d\n",reprovadoF);

    return 0;
}