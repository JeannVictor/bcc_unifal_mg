/*3. Defina a relação shift (Lista1, Lista2) tal que L2 seja a lista uma rotação para a esquerda. Assim:
shift ([1,2,3], L2) então L2 = [2,3,1]*/

ap([],L,L). %[] ++ L = L
ap([X|L1],L2,[X|L3]):-
    ap(L1,L2,L3).

shift([],[]).
shift([H|T],Resultado):-
    ap(T,[H],Resultado).