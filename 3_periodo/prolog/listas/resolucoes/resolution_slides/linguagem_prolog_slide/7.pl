/*7. Implemente um predicado de nome menor que encontre o menor elemento numa lista de
inteiros. Exemplo: menor ([1,5,4,3,0,9,8,7], X), X = 0*/
menor([X],X).
menor([H|T],X):-
    menor(T,X2),
    ((H < X2) ->  X = H;X = X2).