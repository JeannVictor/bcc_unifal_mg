% 4. Usando um acumulador, e somente as operações (+)(-)(*), desenvolva um predicado
% Prolog para calcular X elevado a Y. Assuma X e Y inteiro
% Função que retorna a potencia
pot(X,Y,Z):-
	pot_aux(X,Y,1,Z).

% Função que realmente faz os cálculos com o acumulador.
pot_aux(_,0,Acc,Acc).
pot_aux(X,Y,Acc,Z):-
    (Y > 0),
    NewAcc is Acc * X,
    (Y1 is Y - 1),
    pot_aux(X,Y1,NewAcc,Z).