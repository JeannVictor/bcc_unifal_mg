/*Exercício 2:
Implemente o predicado Prolog remove_duplicados/2 que remove todos os elementos
duplicados de uma lista dada como primeiro argumento e retorna o resultado no segundo
argumento. Exemplo de uso:
?- remove_duplicados([a, b, a, c, d, d], List).
List = [b, a, c, d]
True*/
pertence(X,[X|_]).
pertence(X,[Head|Tail]):-
    (Head \= X),
    pertence(X,Tail).

remove_duplicados([],[]).
remove_duplicados([Head|Tail],Result):-
    pertence(Head,Tail),
    remove_duplicados(Tail,Result).
remove_duplicados([Head|Tail],[Head|Result]):-
    \+ pertence(Head,Tail),
    remove_duplicados(Tail,Result).