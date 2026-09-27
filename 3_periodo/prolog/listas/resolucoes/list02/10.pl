% 10. Faça o predicado merge/3, que junta duas listas ordenadas em uma terceira, mantendo a
% ordem. Como segue:
% ?- merge([a,b,b,k,z], [c,m,n,o], X).
% X=[a,b,b,c,k,,m,n,o,z], yes
merge(X,Y,Ord):-
    append(X,Y,Z),
    ordenaLista(Z,Ord).

ordenaLista([], []).
ordenaLista([A|B], LOrd) :-
    ordenaLista(B, BOrd),
    insOrd(A, BOrd, LOrd).