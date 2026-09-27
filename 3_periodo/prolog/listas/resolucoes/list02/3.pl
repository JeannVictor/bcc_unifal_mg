% 3. Faça um predicado que gere a pirâmide abaixo. Use o predicado wN/1.
%Exemplo de uso:
%?- xxx(3).
%   0
%  101
% 21012
%3210123

% Versão com Recursão Explicita
%-------------------------------------------------------------------------------
% Função que o enunciado deu
wN(0):-write(0),!.
wN(N):-write(N),N1 is N-1, wN(N1),write(N).

% Função que da a quantidade de espaços de cada linha
space(0) :- !.
space(N) :-
    N > 0,
    write(' '),
    N1 is N - 1,
    space(N1).
    
% Função_Auxiliar que imprime a piramide
xxx_aux(N, Y) :- 
    Y > N, !.
xxx_aux(N,Y):-
    (   Y =< N),
    (   S is N -Y),
    space(S),
    wN(Y),
    nl,
    (   Y1 is Y + 1),
    xxx_aux(N,Y1).
% Função principal com um único parametro.
xxx(N):-
    xxx_aux(N,0).
%-------------------------------------------------------------------------------
% Versão sem Recursão Explicita
% Versão sem recursão explícita
xxx2(N) :-
    forall(between(0, N, Y),( S is N - Y,space(S),wN(Y),nl)).