/*4. Defina a relação traducao (Lista1, Lista2) para traduzir uma lista de números de 0 a 9 para a
lista dos números por extenso. Exemplo: traducao ([1,3,9], L2), L2 = [um, tres, nove].
Usar o seguinte predicado auxiliar:
significa (0, zero).
significa (1, um).
(...)
significa (9, nove).*/
significa(0, zero).
significa(1, um).
significa(2, dois).
significa(3, tres).
significa(4, quatro).
significa(5, cinco).
significa(6, seis).
significa(7, sete).
significa(8, oito).
significa(9, nove).

traducao([],[]).
traducao([H|T],[Num|R]):-
    significa(H,Num),
    traducao(T,R).