#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

typedef struct Info_{
	unsigned long int numero_eventos;//fila
	double soma_areas;
	double tempo_anterior;
} Info;

void iniciaInfo(Info *info){
	info->numero_eventos = 0;
	info->soma_areas = 0.0;
	info->tempo_anterior = 0.0;
}

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

	Info en;
	Info ew_chegadas;
	Info ew_saidas;
	
	iniciaInfo(&en);
	iniciaInfo(&ew_chegadas);
	iniciaInfo(&ew_saidas);

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
	scanf("%lF", &intervalo_chegadas);
	intervalo_chegadas = 1.0/intervalo_chegadas;
	
	double media_atendimento;
	printf("Informe o tempo médio dos atendimentos: ");
	scanf("%lF", &media_atendimento);
	media_atendimento = 1.0/media_atendimento;

	/**
	 * por quanto tempo esta simulação executa?
	 */

	double tempo_simulacao;
	printf("Informe o tempo total de simulação: ");
	scanf("%lF", &tempo_simulacao);

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
		tempo_decorrido = fila?
			min(chegada_cliente, saida_cliente):
			chegada_cliente;

		printf("tempo decorrido: %lF\n", tempo_decorrido);

		if(tempo_decorrido == chegada_cliente){
			printf("evento --> chegada!\n");
			if(!fila){
				//servidor estava ocioso
				//tempo de atendimento gerado
				saida_cliente = tempo_decorrido + 
					(-1.0/media_atendimento) * log(aleatorio());

				//tempo trabalhando naquele atendimento
				soma_atendimentos += saida_cliente - tempo_decorrido; 
			}
			fila++;
			//gerando a chegada do próximo "cliente"
			chegada_cliente = tempo_decorrido + 
				(-1.0/intervalo_chegadas) * log(aleatorio());

			//calculando qtd media de "clientes"
			en.soma_areas += en.numero_eventos * (tempo_decorrido - en.tempo_anterior);
			en.tempo_anterior = tempo_decorrido;
			en.numero_eventos++;
			
			ew_chegadas.soma_areas += ew_chegadas.numero_eventos * (tempo_decorrido - ew_chegadas.tempo_anterior);
			ew_chegadas.tempo_anterior = tempo_decorrido;
			ew_chegadas.numero_eventos++;
		}else{
			printf("evento --> saída!\n");
			fila--;
			if(fila){
				//servidor começa o atendimento do próximo
				saida_cliente = tempo_decorrido + 
					(-1.0/media_atendimento) * log(aleatorio());
				
				//tempo trabalhando naquele atendimento
				soma_atendimentos += saida_cliente - tempo_decorrido; 
			}
			
			//calculando qtd media de "clientes"
			en.soma_areas += en.numero_eventos * (tempo_decorrido - en.tempo_anterior);
			en.tempo_anterior = tempo_decorrido;
			en.numero_eventos--;


			ew_saidas.soma_areas += ew_saidas.numero_eventos * (tempo_decorrido - ew_saidas.tempo_anterior);
			ew_saidas.tempo_anterior = tempo_decorrido;
			ew_saidas.numero_eventos++;
		}
		printf("fila: %d\n", fila);
		printf("**************\n\n");
		//getchar();
	}
	ew_chegadas.soma_areas += ew_chegadas.numero_eventos * (tempo_decorrido - ew_chegadas.tempo_anterior);
	ew_saidas.soma_areas += ew_saidas.numero_eventos * (tempo_decorrido - ew_saidas.tempo_anterior);
	double lambda = ew_chegadas.numero_eventos / tempo_decorrido;
	double en_final = en.soma_areas/tempo_decorrido;
	double ew_final = (ew_chegadas.soma_areas - ew_saidas.soma_areas)/ew_chegadas.numero_eventos;

	printf("ocupação: %lF\n", soma_atendimentos/tempo_decorrido);
	printf("E[N]: %lF\n", en_final);
	printf("E[W]: %lF\n", ew_final);

	printf("Erro de Little: %lF\n", en_final - (lambda * ew_final));

	exit(0);
}
