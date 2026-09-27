# Compilador
CC = gcc

# Flags de compilação
CFLAGS = -Wall -Wextra -g

# Nome do executável
TARGET = tp3

# Arquivos fonte
SOURCES = main.c funcoes.c

# Arquivos objeto gerados a partir dos sources
OBJECTS = $(SOURCES:.c=.o)

# Header files
HEADERS = tp3.h

# Regra principal
all: $(TARGET)

# Regra para gerar o executável
$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(TARGET)

# Regra para compilar os arquivos objeto
%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

# Regra para limpar arquivos temporários e executável
clean:
	rm -f $(OBJECTS) $(TARGET)

# Regra para executar o programa
run: $(TARGET)
	./$(TARGET)

# Define as regras que não são arquivos
.PHONY: all clean run