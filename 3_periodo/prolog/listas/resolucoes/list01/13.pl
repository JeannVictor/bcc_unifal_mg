/*
Exercício 13:
Implemente o predicado Prolog ocorrencias/3 que conta o número de ocorrências de um
dada elemento numa lista. Exemplo de uso:
?- ocorrencias(dog, [dog, frog, cat, dog, dog, tiger], N).
N = 3
True*/
ocorrencias(_,[],0).
ocorrencias(Elem,[Head|Tail],Result):-
    (Head == Elem),
    ocorrencias(Elem,Tail,Result2),
    (Result is Result2 + 1).
ocorrencias(Elem,[Head|Tail],Result):-
    (Head \= Elem),
    ocorrencias(Elem,Tail,Result).