/*9. Defina um predicado denominado gera2x que gera uma lista de dobro do numero que é passado
como objeto até zero (0). Exemplo: gera2x (5, L), L = [10, 8, 6, 4, 2, 0].*/
gera2x(0,[0]).
gera2x(X,[H|T]):-
    (H is 2 * X),
    (X2 is X-1),
    gera2x(X2,T).
