% 7. Defina um predicado metIguais/1, que é verdadeiro se uma lista é formada por
% duas metades iguais. Use o append. Seguem dois exemplos de uso.
% ?-metIguais([a,b,c, a,b,c]).
% Yes
% ?-metIguais([a,b,c, a,b,d]).
% No

% Versão de Doente
metIguais(Lista):-
    dividirLista(Lista,P1,P2),
    P1 == P2.
     
dividirLista(Lista,P1,P2):-
    length(Lista,Tam),
    Metade is Tam // 2,
    length(P1,Metade), % Define o tamanho de P1
    append(P1,P2,Lista). % Basicamente joga os valores da lista para P1 e P2 de acordo tam.

%Versão Correta
metIguais2(Lista):-
    append(P1,P2,Lista),P1 == P2.