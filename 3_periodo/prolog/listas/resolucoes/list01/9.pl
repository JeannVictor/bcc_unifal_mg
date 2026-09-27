/*Exercício 9:
Escreva o predicado Prolog media/2 que calcula a média de uma lista de inteiros.
Exemplo de uso:
?- media([1, 2, 3, 4], X).
X = 2.5
True */
qtd([],0).
qtd([_|Tail],Comp):-
    qtd(Tail,Comp2),
    Comp is Comp2 + 1.

sum([],0).
sum([Head|Tail],Sum):-
    sum(Tail,Sum2),
    Sum is Head + Sum2. 

media([],0).
media([Head|Tail],Media):-
    sum([Head|Tail],Sum),
    qtd([Head|Tail],Comp),
    (Comp > 0),
    Media is Sum/Comp.