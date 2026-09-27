# Variáveis
CC = gcc
CFLAGS = -Wall -Wextra -g
TARGET = labirinto
SRC = main.c
BUILD_DIR = build

# Regras principais
all: $(BUILD_DIR) $(BUILD_DIR)/$(TARGET)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(BUILD_DIR)/$(TARGET)

run: all
	@echo "Escolha um labirinto para executar:"
	@ls labirintos/
	@read -p "Digite o nome do arquivo (ex.: labirinto1.txt): " lab; \
	./$(BUILD_DIR)/$(TARGET) labirintos/$$lab

clean:
	rm -rf $(BUILD_DIR)
