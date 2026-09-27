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

int main() {
	/**Na Exponencial, E[X] = 1/l
	 *
	 * E[X] = 5 segundos (ex: agencia bancária)
	 * 1/l = 5
	 * logo, l = 1/5
	 */

	double l;
	printf("Informe o tempo médio entre chegadas: ");
	scanf("%lf", &l);
	l = 1.0/l;

	double soma = 0.0;
	int qtdExecucoes = 10000;
	int i = 0;

	/**
	 * iniciando a semente aleatória
	 */

	int sementeAleat = time(NULL);
	//int sementeAleat = 10;
	srand(sementeAleat); // inicia a função de geração de números pseudo-aleatórios

	for(i = 0; i < qtdExecucoes; i++){
		double valor = (-1.0/l) * log(aleatorio());
		// printf("%lF\n", valor);
		// getchar();
		soma += valor;
	}

	printf("media: %lf\n",(soma / qtdExecucoes));
	exit(0);

}

