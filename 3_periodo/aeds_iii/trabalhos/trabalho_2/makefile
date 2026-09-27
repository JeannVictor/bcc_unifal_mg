PROJ_NAME=tp2

CC=gcc

CFLAGS= -Wall -Wextra -g -O3
LDFLAGS= -lm  

C_SOURCE=$(wildcard ./source/*.c)

H_SOURCE=$(wildcard ./source/*.h)

OBJ=$(subst .c,.o,$(subst source,objects,$(C_SOURCE)))

all: objFolder $(PROJ_NAME)

$(PROJ_NAME): $(OBJ)
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)  


./objects/%.o: ./source/%.c
	$(CC) $(CFLAGS) -c $< -o $@

./objects/main.o: ./source/main.c $(H_SOURCE)
	$(CC) $(CFLAGS) -c $< -o $@

objFolder:
	@mkdir -p objects

clean:
	@rm -rf ./objects/*.o $(PROJ_NAME) *~
	@rmdir objects

.PHONY: all clean objFolder