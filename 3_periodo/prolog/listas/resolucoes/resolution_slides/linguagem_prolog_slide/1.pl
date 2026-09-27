/*1. Defina os dois predicados prolog. listapar (Lista) - que é verdadeiro quando o número de
elementos da lista for par. E listaimpar (Lista) - que é verdadeiro quando o número de elementos
da lista for impar.*/

comprimento([], 0).
comprimento([_|T], X) :-
    comprimento(T, X2),
    X is X2 + 1.
listapar([H|T]):-
    comprimento([H|T],X),
    (X mod 2 =:= 0).
listaimpar([H|T]):-
    comprimento([H|T],X),
    (X mod 2 =:= 1).