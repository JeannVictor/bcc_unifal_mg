# Disciplina: Processamento de Imagens
# Professor : Luiz Eduardo
# Aluno     : Jeann Victor Batista
#
# Trabalho  : Codificação e Decodificação de Contornos (Código de Cadeia)

CC = gcc
CFLAGS = -Wall -Wextra -std=c11
EXECUTAVEL = main

FONTES = main.c codificacao.c decodificacao.c
OBJETOS = $(FONTES:.c=.o)

$(EXECUTAVEL): $(OBJETOS)
	$(CC) $(CFLAGS) -o $(EXECUTAVEL) $(OBJETOS)

%.o: %.c codigo_cadeia.h
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: run clean

run: $(EXECUTAVEL)
	./$(EXECUTAVEL)

clean:
	rm -f $(OBJETOS) $(EXECUTAVEL)
