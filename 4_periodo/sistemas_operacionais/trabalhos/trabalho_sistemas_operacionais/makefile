CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -g
LDFLAGS = -lm  
TARGET = fat_simulator
SOURCES = main.c fat.c
HEADERS = fat.h
OBJECTS = $(SOURCES:.c=.o)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJECTS) $(LDFLAGS)

main.o: main.c $(HEADERS)
	$(CC) $(CFLAGS) -c main.c

fat.o: fat.c $(HEADERS)
	$(CC) $(CFLAGS) -c fat.c

clean:
	rm -f $(OBJECTS) $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: clean run