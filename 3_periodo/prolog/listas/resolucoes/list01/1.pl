/*Escreva o predicado Prolog analisa_lista/1 que toma uma lista como argumento e escreve
sua cabeça e cauda na tela. Se a lista está vazia, o predicado deve escrever uma
mensagem. Exemplos de uso:
?- analisa_lista([dog, cat, horse, cow]).
A cabeca da lista eh: dog
A cauda da lista eh: [cat, horse, cow]
True
?- analisa_lisa([]).
A lista esta vazia
True*/

analisa_lista([]) :- 
    write('A lista esta vazia'), nl.

analisa_lista([H|T]) :- 
    write('A cabeça da lista é: '), write(H), nl,
    write('A cauda da lista é: '), write(T), nl.
