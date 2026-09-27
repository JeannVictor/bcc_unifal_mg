#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

//retorna um numero pseudo-aleatório entre (0,1]
double aleatorio() {
	double u = rand() / ((double) RAND_MAX + 1);
	u = 1.0 - u; // limitando entre (0,1]
	return (u); 
}

double min(double n1, double n2){
	if(n1 < n2) return n1;
	return n2;
}

int main() {
	//semente aleatória
	int sementeAleat = time(NULL);
	//int sementeAleat = 10;
	srand(sementeAleat); // inicia a função de geração de números pseudo-aleatórios
	
	/**
	 * tempo médio entre chegadas
	 * tempo médio de atendimento
	 */
	double intervalo_chegadas;
	printf("Informe o tempo médio entre chegadas: ");
	scanf("%lf", &intervalo_chegadas);
	intervalo_chegadas = 1.0/intervalo_chegadas;
	
	double media_atendimento;
	printf("Informe o tempo médio dos atendimentos: ");
	scanf("%lf", &media_atendimento);
	media_atendimento = 1.0/media_atendimento;

	/**
	 * por quanto tempo esta simulação executa?
	 */

	double tempo_simulacao;
	printf("Informe o tempo total de simulação: ");
	scanf("%lf", &tempo_simulacao);

	/**
	 * em que tempo estamos?
	 */
	double tempo_decorrido = 0.0;

	/**
	 * chegada do próximo "cliente"
	 */
	double chegada_cliente = (-1.0/intervalo_chegadas) * log(aleatorio());

	/**
	 * fila para "guardar" os clientes
	 */
	unsigned long int fila = 0;

	/**
	 * tempo de saída do "cliente" em atendimento
	 */
	double saida_cliente;

	/**
	 * medidas de interesse
	 */
	double soma_atendimentos = 0.0;//ocupação
	
	/**
	 * "coração da simulação"
	 */
	while(tempo_decorrido < tempo_simulacao){
		tempo_decorrido = fila ? min(chegada_cliente, saida_cliente) : chegada_cliente;

		printf("tempo decorrido: %lf\n", tempo_decorrido);

		if(tempo_decorrido == chegada_cliente){
			printf("evento --> chegada!\n");
			if(!fila){
				//servidor estava ocioso
				//tempo de atendimento gerado
				saida_cliente = tempo_decorrido + (-1.0/media_atendimento) * log(aleatorio());
				//tempo trabalhando naquele atendimento
				soma_atendimentos += saida_cliente - tempo_decorrido; 
			}
			fila++;
			//gerando a chegada do próximo "cliente"
			chegada_cliente = tempo_decorrido + (-1.0/intervalo_chegadas) * log(aleatorio());
		}else{
			printf("evento --> saída!\n");
			fila--;
			if(fila){
				//servidor começa o atendimento do próximo
				saida_cliente = tempo_decorrido + (-1.0/media_atendimento) * log(aleatorio());
				
				//tempo trabalhando naquele atendimento
				soma_atendimentos += saida_cliente - tempo_decorrido; 
			}
		}
		printf("fila: %lu\n", fila);
		printf("**************\n\n");
		//getchar();
	}

	printf("ocupação: %lf\n", soma_atendimentos/tempo_decorrido);

	exit(0);
}
