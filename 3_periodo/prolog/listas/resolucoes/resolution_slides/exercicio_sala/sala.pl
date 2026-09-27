% Exercício 1
% Escreva um predicado Prolog empacota/2, que, se uma lista
% contém elementos repetidos consecutivos, eles sejam colocados em
% sublistas separadas.
% Exemplo:
% ?- empacota([a,a,a,a,b,c,c,a,a,d,e,e,e,e],X).
% X = [[a,a,a,a],[b],[c,c],[a,a],[d],[e,e,e,e]]

% Caso onde o próximo elemento é igual
empacota([],[]). 
empacota([X,A|Y],[[X|Z]|W]):-
    X == A,
    empacota([A|Y],[Z|W]),!.

% Caso onde o próximo elemento é diferente
empacota([X|Y],[[X]|W]):- 
    empacota(Y,W).
%------------------------------------------------------------------------
% Exercício 2
% Use o resultado do problema do exercício 1 para implementar o
% método de compressão de dados conhecido como codificação
% run-length (comprimento da corrida). Elementos duplicados
% consecutivos são codificados como termos [N,E], onde N é o
% número de duplicatas do elemento E.
% Exemplo:
% ?- codifica1([a,a,a,a,b,c,c,a,a,d,e,e,e,e],X).
% X = [[4,a],[1,b],[2,c],[2,a],[1,d],[4,e]]

% Função que gera cada tupla
tupla([],[]).
tupla([[H|T]|W],[[Tam,H]|Resto]):-
    length([H|T],Tam),
    tupla(W,Resto).

% Função que empacota as listas e depois cria as tuplas
codifica1([],[]).
codifica1(A,C):-
    empacota(A,T),
    tupla(T,C).
%------------------------------------------------------------------------
% Exercício 3
% Modifique o resultado do problema do exercício 2 de forma que, se
% um elemento não tiver duplicatas, ele seja simplesmente copiado
% para a lista resultante. Apenas elementos com duplicatas devem
% ser transferidos como termos [N,E].
% Exemplo:
% ?- codifica2([a,a,a,a,b,c,c,a,a,d,e,e,e,e],X).
% X = [[4,a],b,[2,c],[2,a],d,[4,e]]

% Função que gera cada tupla
tupla2([],[]).
tupla2([[H|T]|W],[H|Resto]):-
    length([H|T],Tam),
    Tam == 1,
    tupla2(W,Resto).
tupla2([[H|T]|W],[[Tam,H]|Resto]):-
    length([H|T],Tam),
    tupla2(W,Resto).

% Função que empacota as listas e depois cria as tuplas
codifica2([],[]).
codifica2(A,C):-
    empacota(A,T),
    tupla2(T,C).
%------------------------------------------------------------------------
% Exercício 4
% Dada uma lista codificada com run-length, gerada conforme
% especificado no problema do exercício 3, construa sua versão
% descomprimida.

% Função que recebe um número e um elemento, e gera uma lista
constroeLista(0,_,[]):-!.
constroeLista(A,B,[B|Resto]):-
    A > 0,
    A1 is A - 1,
    constroeLista(A1,B,Resto).

% Função que reconstrói a lista original a partir da codificação
junta([],[]).
junta([[Tam,Elem]|Resto],Final):-
    constroeLista(Tam,Elem,L1),
    junta(Resto,L2),
    append(L1,L2,Final).
junta([Elem|Resto],[Elem|Lista]):-
    junta(Resto,Lista).