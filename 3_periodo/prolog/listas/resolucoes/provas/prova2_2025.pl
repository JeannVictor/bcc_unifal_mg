% Resolução da Prova 2 de Programação Lógica 2025/1

%--- Questão 1 --- 
% Qual é o resultado da seguinte consulta prolog?
% ?- lenght (A,3),maplist (=('a'),A).

A = ['a','a','a'].

%--- Questão 2 --- 
% Implemente o predricado Prolog xxx/3 para obter o mesmo resultado
% da consulta anterior sem usar os metapredicados lenght e maplist
% Exemplo de uso :
% ?- xxx(3,'a',A).

xxx(0,_,[]).
xxx(I,C,[C|Resto]):-
    I > 0,
    I1 is I - 1,
    xxx(I1,C,Resto).

%--- Questão 3 --- 
% Considerando os seguintes predicados?
% ap([],L,L).
% ap([A|B], C, [A|D]) ;- ap(B,C,D).
% nonono(U,L) :- ap(_,[U],L).

% a) Qual é o resultado da consulta abaixo 
O resultado da consulta é 4.

% b) Dê um nome para o predicado nonono
% ?- nonono(X,[1,2,3,4])
Um possivel nome é: ultimoElemento

