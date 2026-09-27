/*6. Desenvolva um predicado em prolog que troca a primeira ocorrencia de um certo inteiro numa
lista de inteiros dando como resultado uma lista com um elemento alterado. Exemplo: altera (3,
4, [1,2,3,4], L), L = [1,2,4,4]*/
altera(X,Y,[X|T],[Y|T]).
altera(X,Y,[H|T],[H|R]):-
    (X \= H),
    altera(X,Y,T,R).