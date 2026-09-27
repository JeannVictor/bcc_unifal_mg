% 2. Considere o seguinte programa Prolog:
a:-a(0).
a(X):- X>10,!.
a(X):- write(X),write(’ ’), X1 is X+1,a(X1).
%Qual será o resultado da seguinte consulta Prolog:
%?- a.

% O resultado dessa chamada é: 0 1 2 3 4 5 6 7 8 9 10
