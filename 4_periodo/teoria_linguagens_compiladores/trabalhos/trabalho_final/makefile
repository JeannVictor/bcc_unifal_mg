simples : utils.c lexico.l sintatico.y tree.c
	@flex -o lexico.c lexico.l
	@bison -v -d sintatico.y -o sintatico.c
	@gcc sintatico.c -o simples

limpa : 
	@echo "limpando..."
	@rm -f lexico.c sintatico.c sintatico.h sintatico.output simples
	@rm -f *.dot *.svg *.mvs