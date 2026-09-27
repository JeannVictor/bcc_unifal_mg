#include <stdio.h>

// Exercício 8
// Autor: Jeann Victor Batista

// Função para transformar texto minúsculo em maiúsculo.
void maiuscula(char *palavra) {
    for (int i = 0; palavra[i] != '\0'; i++) { 
        if (palavra[i] >= 'a' && palavra[i] <= 'z') {
            palavra[i] -= 32;
        }
    }
}

int main(){
    
    char texto[] = "messi is the goat!!!";

    maiuscula(texto); 
    printf("Texto em maiúsculo: %s\n", texto);

    return 0;
}
