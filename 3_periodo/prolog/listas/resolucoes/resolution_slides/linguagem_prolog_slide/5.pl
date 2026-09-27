/*5. Escreva um predicado em prolog que apaga de uma lista de inteiros o elemento de uma posição
relativa na lista. Exemplo: apaga (3, [6,7,8,9,1,2,3], L), L = [6,7,9,1,2,3]. Observe que foi
apagado o terceiro elemento da lista.*/
apaga(1,[_|R],R). % Creio estar faltando um caso base
apaga(X,[H|T],[H|R]):-
    (X2 is X -1),
    (X2 >= 1),
    apaga(X2,T,R).