/*Exercício 3:
Escreva o predicado Prolog troca/4 que troca todas as ocorrências de um dado elemento
(segundo argumento), por outro elemento (terceiro argumento) de uma lista (primeiro
argumento). Exemplo de uso:
?- troca([1, 2, 3, 4, 3, 5, 6, 3], 3, x, List).
List = [1, 2, x, 4, x, 5, 6, x]
True*/
troca([],_,_,[]).
troca([Head|Tail],Elem,Troca,[Troca|Rest]):-
    (Head == Elem),
    troca(Tail,Elem,Troca,Rest).
troca([Head|Tail],Elem,Troca,[Head|Rest]):-
    (Head \= Elem),
    troca(Tail,Elem,Troca,Rest).