/*10. Desenvolva um predicado prolog que a partir de uma posição relativa dentro de uma lista de
inteiros, dê como resultado a lista com os elementos até a posição menos 1. Exemplo: trunca (3,
[1,4,5,6,7], L), L = [1,4].*/
trunca(_,[],[]).
trunca(1, _, []).
trunca(X,[H|T],[H|R]):-
    (X2 is X-1),
    (X2 > 0),
    trunca(X2,T,R).