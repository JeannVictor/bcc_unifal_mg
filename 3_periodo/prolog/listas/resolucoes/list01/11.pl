/*Exercício 11:
Escreva o predicado intervalo/3 que gera uma lista de inteiros dado o limite inferior e
superior como primeiro e segundo argumento. O resultado é uma lista de inteiros
retornado como terceiro argumento. Exemplos de uso:
?- intervalo(3, 11, X).X = [3, 4, 5, 6, 7, 8, 9, 10, 11]
True
?- intervalo(7, 4, X).
X = []
True*/
intervalo(Inicio,Inicio,[Inicio]).
intervalo(Inicio,Fim,[Inicio|Resto]):-
    (Inicio =< Fim),
    (Inicio2 is Inicio +1),
    intervalo(Inicio2,Fim,Resto).