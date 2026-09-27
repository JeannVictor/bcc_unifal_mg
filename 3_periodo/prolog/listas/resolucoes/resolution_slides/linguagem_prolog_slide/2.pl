/*2. Defina a relação reversa (Lista, ListaReversa). Por exemplo: reversa ([a,b,c,d], X) X=[d,c,b,a].
reversa([],[]).*/
reversa([X],[X]).
reversa([X|Y], Resultado) :-
    reversa(Y, R),
    ap(R, [X], Resultado).