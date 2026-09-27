/*Exercício 4:
Uma lista Prolog sem valores duplicados pode ser usada para representar um conjunto.
Escreva um predicado que dado uma lista que representa um conjunto C, produza uma
lista de lista que é o conjunto potência de C. Exemplo de uso:
?- potencia([a, b, c], P).
P = [[a, b, c], [a, b], [a, c], [a], [b, c], [b], [c], []]
True*/

ap([],L,L). %[] ++ L = L
ap([X|L1],L2,[X|L3]):-
    ap(L1,L2,L3).

adiciona(_, [], []).
adiciona(X, [H|T], [[X|H]|R]) :-
    adiciona(X, T, R).

potencia([],[[]]).
potencia([Head|Tail],R):-
    potencia(Tail,R2),
    adiciona(Head,R2,Resultado),
    ap(Resultado,R2,R).