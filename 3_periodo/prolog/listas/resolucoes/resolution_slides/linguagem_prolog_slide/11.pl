/*11. Escreva um predicado que a partir de um valor inteiro gere uma lista de cubos dos valores.
Assim: cubo (3, C), C = [27, 8, 1, 0].*/
cubo(0,[0]).
cubo(X,[H|T]):-
    (H is X ** 3),
    (X2 is X-1),
    cubo(X2,T).