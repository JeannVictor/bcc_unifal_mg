/*Exercício 5:
Escreva o predicado Prolog mais_longa/2 que recebe duas listas como argumentos e
verifica se a segunda lista é mais longa (tem mais elementos) que a primeira lista.
Implementar sem usar qualquer operação aritmética (contar o tamanho das listas, por
exemplo). Exemplo de uso:
?- mais_longa([dog,cat,snake], [giraffe,elephant,lion,tiger]).
True
?- mais_longa([1,2,3,4,5], []).
False*/
mais_longa([],[_|_]).
mais_longa([_|Tail1],[_|Tail2]):-
    mais_longa(Tail1,Tail2).