/*Exercício 7:
Escreva o predicado Prolog quadrado/2 para escrever um quadrado n x n de um dado
caracter na tela. O primeiro argumento é o valor de n e o segundo o caracter a ser
implementado. Exemplo de uso:
?- quadrado(5, ‘*’).
* * * * *
* * * * *
* * * * *
* * * * *
* * * * *
True */

line(0,_):- !.
line(X,Char):-
    (X > 0),
    write(Char),
    write(' '),
    X2 is X-1,
    line(X2,Char).

quad_aux(_,0,_):- !.
quad_aux(X,Y,Char):-
    (Y > 0),
    line(X,Char),
    nl,
    Y2 is Y - 1,
    quad_aux(X,Y2,Char).

quadrado(X,Char):-
    quad_aux(X,X,Char).