/*
Exercício 14:
Escreva o predicado Prolog divisores/2 que calcula a lista de divisores de um número.
Exemplo de uso:
?- divisores(30, X).
X = [1, 2, 3, 5, 6, 10, 15, 30]
True */
aux(Elem,Cont,[]):-
    (Cont > Elem).
aux(Elem,Cont,[Cont|Tail]):-
    (Cont =< Elem),
    (Elem mod Cont =:= 0),
    (Cont2 is Cont + 1),
    aux(Elem,Cont2,Tail).
aux(Elem,Cont,Tail):-
    (Cont =< Elem),
    (Elem mod Cont =\= 0),
    (Cont2 is Cont + 1),
    aux(Elem,Cont2,Tail).

divisores(0,[]).
divisores(Elem,Result):-
    aux(Elem,1,Result).