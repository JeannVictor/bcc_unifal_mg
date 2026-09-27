#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Atividade 4: Operações em vetores
// Autor: Jeann Victor Batista

// Variável global para definir o tamanho máximo do vetor
int MAX = 1000;

int main()
{
    // Inicialização de variáveis para manipulação do vetor
    srand(time(NULL));  // Inicializa o gerador de números aleatórios com seed baseada no tempo atual
    int array[MAX],     // Vetor principal para armazenar os números
        e = 0,          // Variável para armazenar a opção do menu
        number = 0,     // Variável para armazenar valores de busca/remoção
        vezes = 0;      // Contador de ocorrências de um valor
    int inicio = 0,     // Limite inferior para busca por intervalo
        fim = 0;        // Limite superior para busca por intervalo

    // Preenchimento do vetor com números aleatórios entre 1 e 300
    // Utiliza rand() % 300 + 1 para garantir valores no intervalo desejado
    for(int i = 0; i < MAX; i++) {
        array[i] = rand() % 300 + 1;
    }
    
    do {
        // Exibição do menu de opções para manipulação do vetor
        printf("\n\n--- OPERAÇÕES ---\n");
        printf("0. Sair do programa.\n");
        printf("1. Buscar a primeira ocorrência de um valor\n");
        printf("2. Quantidade de ocorrências de um valor\n");
        printf("3. Valores em um intervalo\n");
        printf("4. Inverter o vetor\n");
        printf("5. Excluir um valor\n");
        printf("6. Remover valores repetidos\n");
        scanf("%d",&e);

        // Validação da entrada do menu
        // Garante que a opção escolhida esteja dentro do intervalo válido
        while(e < 0 || e > 6) {
            printf("Digite um número de operação válido.");
            scanf(" %d",&e);
        }

        // Estrutura de seleção para execução da operação escolhida
        switch (e) {
        case 1:
            // Busca pela primeira ocorrência de um valor específico
            int existe = 0;  // Flag para indicar se o valor foi encontrado

            // Solicita ao usuário o valor a ser procurado
            printf("Digite o valor a ser procurado:\n");
            scanf("%d",&number);

            // Percorre o vetor procurando a primeira aparição do número
            for(int i = 0; i < MAX; i++) {
                if(array[i] == number) {
                    // Imprime a posição da primeira ocorrência
                    printf("A primeira ocorrência do valor %d foi na posição %d", number, i);
                    existe = 1;  // Marca que o valor foi encontrado
                    break;  // Interrompe a busca após encontrar a primeira ocorrência
                }                
            }

            // Mensagem caso o número não exista no vetor
            if(existe == 0)
                printf("O valor não existe dentro do vetor.\n");
            break;
    
        case 2:
            // Contagem de ocorrências de um valor específico
            // Solicita ao usuário o valor a ser contado
            printf("Digite o valor a ser procurado:\n");
            scanf("%d",&number);

            // Percorre o vetor contando as aparições do número
            for(int i = 0; i < MAX; i++) {
                if(array[i] == number)
                    vezes++;  // Incrementa contador a cada ocorrência
            }

            // Exibe resultado da contagem
            if(vezes != 0) {
                printf("A quantidade de aparições do número %d foi de %d vezes", number, vezes);
            } else {
                printf("O valor procurado não existe.\n");
            }

            // Reseta o contador para próximas buscas
            vezes = 0;
            break;

        case 3:
            // Busca de valores dentro de um intervalo específico
            printf("O inicio deve ser um número não negativo menor que o fim\n");

            // Solicita os limites do intervalo ao usuário
            printf("Digite o inicio do intervalo\n");
            scanf("%d",&inicio);  

            printf("Digite o fim do intervalo\n");
            scanf("%d",&fim);

            // Validação do intervalo
            // Garante que o início seja menor que o fim e não negativo
            while(inicio >= fim || inicio < 0) {
                printf("Digite valores válidos!\n");
                printf("Digite o começo do intervalo\n");
                scanf("%d",&inicio);    
                printf("Digite o fim do intervalo\n");
                scanf("%d",&fim);
            }

            // Impressão dos valores que estão dentro do intervalo especificado
            printf("Os valores que estão dentro do intervalo são:"); 
            for(int i = 0; i < MAX; i++) {
                if(array[i] >= inicio && array[i] <= fim)
                    printf("%d, ", array[i]);      
            }
            break;

        case 4:
            // Inversão da ordem dos elementos do vetor
            printf("O vetor será invertido!\n");

            // Algoritmo de inversão usando troca de elementos
            // Percorre metade do vetor, trocando elementos simétricos
            for(int i = 0, j = MAX - 1; i < j; i++, j--) {
                int tmp = array[i];
                array[i] = array[j];
                array[j] = tmp;
            }

            printf("O vetor foi invertido com sucesso.");
            break; 

        case 5:
            // Exclusão de todas as ocorrências de um valor específico
            // Solicita o valor a ser removido
            printf("Qual valor deseja excluir do vetor ?\n");
            scanf("%d",&number);

            // Flag para verificar se o número existe no vetor
            existe = 0;
            int MAX2 = MAX;

            // Percorre o vetor removendo todas as ocorrências do valor
            for(int i = 0; i < MAX; i++) {
                if(array[i] ==  number) {
                    existe = 1;
                    // Desloca elementos para preencher o "buraco" deixado
                    for(int j = i; j < MAX; j++) {
                        array[j] = array[j + 1];                     
                    }
                    array[MAX - 1] = 0;  // Limpa a última posição
                    MAX--;  // Reduz o tamanho efetivo do vetor
                    i--;    // Decrementa índice para não pular elemento após remoção
                }
            }

            // Tratamento de caso onde o valor não foi encontrado
            if(existe == 0) {
                printf("O valor não existe no vetor.\n");     
            } else {
                // Imprime os 10 primeiros elementos após remoção
                for(int i = 0; i < MAX2; i++)
                    printf("%d ", array[i]);
            }
            break;
    
        case 6:
            // Remoção de valores repetidos do vetor
            printf("Todos os valores repetidos serão removidos\n");

            // Algoritmo de remoção de duplicatas
            // Percorre o vetor comparando elementos
            for(int i = 0; i < MAX; i++) {
                for(int j = i + 1; j < MAX;) {
                    // Se encontrar elemento repetido
                    if(array[i] == array[j]) {
                        // Desloca elementos para remover duplicata
                        for(int k = j; k < MAX; k++)
                            array[k] = array[k + 1];
                        MAX--;  // Reduz tamanho do vetor
                    } else {
                        j++;  // Avança para próximo elemento se não for repetido
                    }
                }
            }

            // Impressão do vetor após remoção de repetidos
            for(int i = 0; i < MAX ; i++) {
                printf("%d ", array[i]);
            }
    
            break;
        }
    } while(e != 0);  // Continua executando até que a opção de saída seja escolhida

    return 0;
}
