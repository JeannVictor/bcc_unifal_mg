% 9. Faça um predicado que particiona/3 uma lista em duas, de tamanho igual se o número de
% elementos for par, senão uma delas terá um elemento a mais. Tire dois elementos de uma
% lista (se possível) e ponha cada um em uma lista resultado.

% Função que particiona uma lista em duas
particiona(Lista,P1,P2):-
    length(Lista,Tam),
    Metade is Tam // 2,
    length(P1,Metade), % Define o tamanho de P1
    append(P1,P2,Lista). % Basicamente joga os valores da lista para P1 e P2 de acordo tam.

% Função que põe os um elemento de cada lista em uma.
resultL(Lista,Resultado):-
    particiona(Lista,[A|_],[C|_]),
    append([A],[C],Resultado).