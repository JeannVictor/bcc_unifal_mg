/*Exercício 10:
Escreva o predicado minimo/2 que encontra o menor valor numérico de uma dada lista de
números. Exemplo de uso:
?- minimo([4, 6, 8, 3, 5, 7], Result).
Result = 3
True*/
minimo([X],X).
minimo([Head|Tail],Min):-
    minimo(Tail,MinT),
    ((Head < MinT)-> Min = Head;Min = MinT).  