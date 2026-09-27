/*+-------------------------------------------------------------+
  |          UNIFAL – Universidade Federal de Alfenas.          |
  | BACHARELADO EM CIENCIA DA COMPUTACAO.                       |
  | Trabalho..: SIMULACAO DE SISTEMA DE ARQUIVOS FAT            |
  | Disciplina: Sistemas Operacionais                           |
  | Professor.: Romario                                         |
  | Aluno(s)..: Jeann Victor Batista                            |
  |             Nicolas Rodrigues Texeira de Oliveira           |
  |             Thallysson Luis Teixeira Carvalho               |
  | Data......: 30/11/2025                                      |
  +-------------------------------------------------------------+*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
#include "fat.h"

void mostraSetores(ptnoSet S, char *n) {
    printf("%s = [", n);
    while (S) {
        printf("(%d,%d)", S->inicio, S->fim);
        S = S->prox;
        if (S) printf(",");
    }
    printf("]\n");
}

void mostraArquivos(ptnoArq A) {
    printf("Arquivos:\n");
    while (A) {
        printf("  %12s, %2d caracter(es).  ", A->nome, A->caracteres);
        mostraSetores(A->setores, "Setores");
        A = A->prox;
    }
    printf("\n");
}

void mostraMemoria(memoria Memo) {
    int i, j;
    for (i = 0; i < TAM_MEMORIA; i++) {
        printf("%3d:[", i);
        for (j = 0; j < TAM_GRANULO - 1; j++)
            printf("%c,", Memo[i][j]);
        printf("%c]", Memo[i][TAM_GRANULO - 1]);
        if ((i + 1) % 10 == 0)
            printf("\n");
    }
}

void inicia(ptnoSet *Area, ptnoArq *Arq, memoria Memo) {
    int i, j;
    *Area = (ptnoSet) malloc(sizeof(noSet));
    (*Area)->inicio = 0;
    (*Area)->fim = TAM_MEMORIA - 1;
    (*Area)->prox = NULL;
    *Arq = NULL;
    for (i = 0; i < TAM_MEMORIA; i++)
        for (j = 0; j < TAM_GRANULO; j++)
            Memo[i][j] = ' ';
}

void ajuda() {
    printf("\nCOMANDOS DISPONIVEIS:\n");
    printf("G <arquivo> <texto> - Grava arquivo com conteudo\n");
    printf("D <arquivo>         - Deleta arquivo\n");
    printf("A <arquivo>         - Apresenta conteudo do arquivo\n");
    printf("M                   - Mostra estruturas utilizadas\n");
    printf("C                   - Desfragmenta o disco\n");
    printf("H                   - Apresenta lista de comandos\n");
    printf("F                   - Fim da simulacao\n");
}

// Funções Auxiliares para Gravar
//-----------------------------------------------------------------------------------------------------
ptnoSet busca_aloca_setores(ptnoSet *areaLivre, int numSetoresNecessarios){
    ptnoSet temp = *areaLivre;
    int setoresLivres = 0;
    // Verifica quanto de área livre ainda existe
    while(temp != NULL){
        setoresLivres += (temp->fim - temp->inicio + 1);
        temp = temp->prox;
    }

    // Verifica se há espaço suficiente...
    if(setoresLivres < numSetoresNecessarios)
        return NULL;
    
    ptnoSet listaSetoresArquivo = NULL;
    int setoresRestantes = numSetoresNecessarios;
    while(setoresRestantes > 0 && *areaLivre != NULL){
        // 1. Calcular quantos setores pegar desta área
        int sDisponivel = (*areaLivre)->fim - (*areaLivre)->inicio + 1;
        int sPegos;
        if(sDisponivel < setoresRestantes){
            sPegos = sDisponivel;
        }else{
            sPegos = setoresRestantes;
        }
        
        int inicioArquivo = (*areaLivre)->inicio;
        int fimArquivo = ((sPegos + inicioArquivo) - 1 );
        
        // 2. Criar nó para lista de setores do arquivo
        ptnoSet novoSetor = (ptnoSet) malloc(sizeof(noSet));
        novoSetor->inicio = inicioArquivo;
        novoSetor->fim    = fimArquivo;
        novoSetor->prox = NULL; 

        // 3. Inserir o nó na lista de setores do arquivo
        if(listaSetoresArquivo == NULL){
            listaSetoresArquivo = novoSetor;
        }else{
            ptnoSet ultimo = listaSetoresArquivo;
            while(ultimo->prox != NULL){
                ultimo = ultimo->prox; 
            }
            ultimo->prox = novoSetor;
        }
        // 4. Atualizar ou remover a área livre atual
        if(sPegos == sDisponivel){
            ptnoSet temp = *areaLivre;
            *areaLivre = (*areaLivre)->prox;
            free(temp);
        }else{
            (*areaLivre)->inicio = novoSetor->fim + 1; 
        }
        // 5. Decrementar setoresRestantes
        setoresRestantes -= sPegos;
    }
    return listaSetoresArquivo;
}

// Grava o conteúdo do texto nos setores da memória
void grava_texto_memoria(memoria Memo, char *texto, ptnoSet setores){
    size_t i = 0; 
    int j;
    size_t texto_len = strlen(texto); // Calcular uma vez só
    ptnoSet atual = setores;
    
    while(atual != NULL && i < texto_len){
        for(int numSetor = atual->inicio; numSetor <= atual->fim; numSetor++){
            for(j = 0; j < TAM_GRANULO; j++){
                if(i < texto_len){
                    Memo[numSetor][j] = texto[i++];
                }else{
                    Memo[numSetor][j] = ' ';
                }
            }
        }
        atual = atual->prox; 
    }
}

// Insere um novo arquivo na lista de arquivos
void insere_arquivo(ptnoArq *listaArquivos, char *nome, int caracteres, ptnoSet setoresOcupados){
    ptnoArq novoArq = (ptnoArq) malloc(sizeof (noArq));
    strcpy(novoArq->nome, nome);
    novoArq->caracteres = caracteres;
    novoArq->setores = setoresOcupados;
    novoArq->prox = NULL;
    if(*listaArquivos == NULL){
        *listaArquivos= novoArq;
    }else{
        ptnoArq ultimo = *listaArquivos;
        while(ultimo->prox != NULL){
            ultimo = ultimo->prox; 
        }
        ultimo->prox = novoArq;
    }  
}

//------------------------------------------------------------------------------------------------------
void gravar(char *nome, char *texto, ptnoSet *areaLivre, ptnoArq *listaArquivos, memoria Memo){
    // Calcula número de setores necessários sem usar ceil
    int numSetoresNecessarios = (strlen(texto) + TAM_GRANULO - 1) / TAM_GRANULO;

    ptnoSet setoresAloc = busca_aloca_setores(areaLivre, numSetoresNecessarios);
    if(setoresAloc == NULL){
        printf("Não é possivel gravar esse arquivo, pois não há espaço suficiente!\n");
        return;
    }
    
    grava_texto_memoria(Memo, texto, setoresAloc);
    insere_arquivo(listaArquivos, nome, strlen(texto), setoresAloc);

    printf("O arquivo '%s' foi gravado com sucesso!\n",nome);
}

//-----------------------------------------------------------------------------------------------------------
// Funções auxiliares para deletar
ptnoArq busca_arquivo(ptnoArq *listaArquivos, char *nome){
    ptnoArq temp = *listaArquivos;
    while(temp != NULL){
        if(strcmp(temp->nome, nome) == 0){
            return temp;
        }else{
            temp = temp->prox;
        }
    }
    return NULL;
}

void liberar_um_setor(ptnoSet *areaLivre, ptnoSet setoresArquivo){
    ptnoSet temp = *areaLivre;
    ptnoSet anterior = NULL;

    if(temp == NULL){
        setoresArquivo->prox = NULL;
        *areaLivre = setoresArquivo;
        return;
    }

    while(temp != NULL){
        // Caso de liberar area entre duas 
        if(temp->fim == (setoresArquivo->inicio - 1) && temp->prox != NULL && temp->prox->inicio == (setoresArquivo->fim + 1)){
            temp->fim = temp->prox->fim;
            ptnoSet tmp = temp->prox;
            temp->prox = temp->prox->prox;
            free(tmp);
            free(setoresArquivo);
            return;
        }
         // Caso a direita
        if(temp->fim == (setoresArquivo->inicio -1)){
            temp->fim = setoresArquivo->fim;
            free(setoresArquivo);
            return;
        }
        // Caso a esquerda
        if(temp->inicio == (setoresArquivo->fim + 1)){
            temp->inicio = setoresArquivo->inicio;
            free(setoresArquivo);
            return;
        }
        anterior = temp;
        temp = temp->prox;
    }
    // Caso onde não havia como juntar intervalos
    if(anterior == NULL){ // insere no começo
        setoresArquivo->prox = *areaLivre;
        *areaLivre = setoresArquivo;
    } else { // insere depois do anterior
        setoresArquivo->prox = anterior->prox;
        anterior->prox = setoresArquivo;
    }
}

void liberar_todos_setores(ptnoSet *areaLivre, ptnoSet setoresArquivo){
    ptnoSet temp = setoresArquivo;
    ptnoSet prox = NULL;

    while(temp != NULL){
        prox = temp->prox;
        liberar_um_setor(areaLivre,temp);
        temp = prox;
    }
}    

void limpar_memoria_setores(memoria Memo, ptnoSet setores) {
    ptnoSet temp = setores;
    while(temp != NULL){
        for(int i = temp->inicio; i <= temp->fim;i++){
            for(int j = 0;j < TAM_GRANULO;j++){
                Memo[i][j] = ' ';
            } 
        }
        temp = temp->prox;
    }
}

void remove_arquivo_lista(ptnoArq *listaArquivos, ptnoSet *areaLivre,char *nome,memoria Memo){
    ptnoArq temp = *listaArquivos;
    ptnoArq anterior = NULL;
    while(temp != NULL){
        if(strcmp(temp->nome, nome) == 0){
            if(anterior == NULL){
                *listaArquivos= temp->prox;
            }else{
                anterior->prox = temp->prox;
            }
            limpar_memoria_setores(Memo,temp->setores);
            liberar_todos_setores(areaLivre,temp->setores);
            free(temp);
            return; 
        }
        anterior = temp; 
        temp = temp->prox;
    }
}

//-----------------------------------------------------------------------------------------------------------
void desfragmentar(ptnoArq *arquivos, ptnoSet *areaLivre, memoria Memo){
    printf("Iniciando desfragmentação...\n");
    
    // Verifica se há arquivos para desfragmentar
    if(*arquivos == NULL) {
        printf("Nenhum arquivo para desfragmentar.\n");
        return;
    }
        
    int posDestino = 0;  // Posição onde o próximo arquivo será colocado
    ptnoArq arqAtual = *arquivos;
    
    // Processar cada arquivo na ordem
    while(arqAtual != NULL) {
        ptnoSet setorAtual = arqAtual->setores;
        int novoInicio = posDestino;
        
        // Calcular total de setores necessários
        int totalSetores = 0;
        ptnoSet temp = setorAtual;
        while(temp != NULL) {
            totalSetores += (temp->fim - temp->inicio + 1);
            temp = temp->prox;
        }
        
        // Mover dados para a posição contígua no início
        setorAtual = arqAtual->setores;
        while(setorAtual != NULL) {
            for(int origem = setorAtual->inicio; origem <= setorAtual->fim; origem++) {
                // Copiar apenas se origem != destino 
                if(origem != posDestino) {
                    for(int j = 0; j < TAM_GRANULO; j++) {
                        Memo[posDestino][j] = Memo[origem][j];
                    }
                }
                posDestino++;
            }
            setorAtual = setorAtual->prox;
        }
        
        // Liberar lista antiga de setores
        setorAtual = arqAtual->setores;
        while(setorAtual != NULL) {
            ptnoSet prox = setorAtual->prox;
            free(setorAtual);
            setorAtual = prox;
        }
        
        // Criar novo setor contíguo para o arquivo
        ptnoSet novoSetor = (ptnoSet)malloc(sizeof(noSet));
        novoSetor->inicio = novoInicio;
        novoSetor->fim = posDestino - 1;
        novoSetor->prox = NULL;
        arqAtual->setores = novoSetor;
        
        printf("Arquivo movido para setores [%d-%d]\n", novoInicio, posDestino - 1);
        
        arqAtual = arqAtual->prox;
    }
    
    // Limpar área restante 
    for(int i = posDestino; i < TAM_MEMORIA; i++) {
        for(int j = 0; j < TAM_GRANULO; j++) {
            Memo[i][j] = ' ';
        }
    }
    
    // Reconstruir área livre como um único bloco contíguo
    ptnoSet setLivre = *areaLivre;
    while(setLivre != NULL) {
        ptnoSet prox = setLivre->prox;
        free(setLivre);
        setLivre = prox;
    }
    
    if(posDestino < TAM_MEMORIA) {
        *areaLivre = (ptnoSet)malloc(sizeof(noSet));
        (*areaLivre)->inicio = posDestino;
        (*areaLivre)->fim = TAM_MEMORIA - 1;
        (*areaLivre)->prox = NULL;
        printf("Nova área livre: setores [%d-%d]\n", posDestino, TAM_MEMORIA - 1);
    } else {
        *areaLivre = NULL;
        printf("Disco completamente ocupado.\n");
    }
    
    printf("Desfragmentação concluída com sucesso!\n");
    puts("");
    mostraMemoria(Memo);
    puts("");
}
//-----------------------------------------------------------------------------------------------------------
void deletar(char *nome, ptnoArq *listaArquivos, ptnoSet *areaLivre,memoria Memo){
    ptnoArq arquivo = busca_arquivo(listaArquivos, nome);  
    if(arquivo == NULL){
        printf("Esse arquivo não existe!\n");
        return;
    }
    remove_arquivo_lista(listaArquivos, areaLivre, nome,Memo);
    printf("O arquivo foi removido com sucesso!\n");
}

void apresentar(char *nome, ptnoArq *listaArquivos, memoria Memo){
    ptnoArq arquivo = busca_arquivo(listaArquivos, nome);
    if(arquivo == NULL){
        printf("Esse arquivo não existe!\n");
        return;
    }
    
    ptnoSet S = arquivo->setores;
    printf("O conteúdo do arquivo '%s' é:\n", nome);
    int chars_impressos = 0;
    while(S != NULL && chars_impressos < arquivo->caracteres){
        for(int i = S->inicio; i <= S->fim && chars_impressos < arquivo->caracteres; i++){
            for(int j = 0; j < TAM_GRANULO && chars_impressos < arquivo->caracteres; j++){
                printf("%c", Memo[i][j]);
                chars_impressos++;
            }
        }
        S = S->prox;
    }
    printf("\n");  
}