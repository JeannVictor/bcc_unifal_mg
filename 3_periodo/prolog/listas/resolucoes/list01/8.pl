/*Exercício 8:
Escreva o predicado Prolog elemento_n/3, que dado uma lista é um número natural n,
retorna o n-ésimo elemento da lista. Exemplo de uso:
?- elemento_n([tiger, dog, teddy_bear, horse, cow], 3, X).
X = teddy_bear
True
?- elemento_n([a, b, c, d], 27, X).
False
 */
elemento_n([X|_],1,X).
elemento_n([_|Tail],Pos,Elem):-
    (Pos > 1),
    (Pos2 is Pos-1),
    elemento_n(Tail,Pos2,Elem).