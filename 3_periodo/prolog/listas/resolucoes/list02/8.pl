% 8. Faça um predicado insOrd/3, que insere um elemento numa lista mantendo-a ordenada.
% Faça duas regras: uma base e uma recursiva.?-insOrd(4,[2,3,5,7],L). L=[2,3,4,5,7] Yes

insOrd(X,[],[X]).
insOrd(X,[A|B],[A|Ord]):-
    X > A,
    insOrd(X,B,Ord).
insOrd(X,[A|B],[X,A|B]).