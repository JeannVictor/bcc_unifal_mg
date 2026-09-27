/*8. Escreva um predicado em prolog que encontra o maior valor numa lista de inteiros. Exemplo:
maior ([1,2,3,9,5,4,6], Y), Y = 9.*/
maior([X],X).
maior([H|T],X):-
    maior(T,X2),
    ((H > X2) ->  X = H;X = X2).