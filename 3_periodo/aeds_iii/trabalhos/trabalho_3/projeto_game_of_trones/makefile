# Nome do projeto
PROJ_NAME = ProjetoGameOfTrones.bin

# Diretório para os arquivos .o e .d
OBJ_DIR = obj

# Arquivos .c
C_SOURCE = $(wildcard *.c)

# Arquivos objeto
OBJ = $(patsubst %.c, $(OBJ_DIR)/%.o, $(C_SOURCE))

# Compilador
CC = gcc

# Flags (opções) para o compilador
CC_FLAGS = -O2 -std=c99 -c -Wall -Wextra -MMD -MP -lm

#########################
# Compilação e linkagem #
#########################
all: $(PROJ_NAME)

# Regra para linkar o executável
$(PROJ_NAME): $(OBJ)
	$(CC) $^ -o $@ -lm

# Regra para compilar os arquivos objeto
$(OBJ_DIR)/%.o: %.c | $(OBJ_DIR)
	$(CC) $(CC_FLAGS) -o $@ $<

# Regra para criar o diretório de objetos
$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

# Regra para limpar os arquivos gerados
clean:
	rm -rf $(OBJ_DIR) *~ $(PROJ_NAME)

# Incluindo automaticamente as dependências geradas
-include $(OBJ:.o=.d)