% 6. Defina o predicado palindromo/1, que é verdadeiro se a lista é um palı́ndromo,
% por exemplo, [a,b,c,d,c,b,a].

palindromo(L) :- reverse(L, L).
% Se o inverso de L == L , esta correto...