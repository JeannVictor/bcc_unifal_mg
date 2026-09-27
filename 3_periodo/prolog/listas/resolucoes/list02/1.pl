% 1. Qual é o resultado das seguintes consultas em Prolog?

?- forall(member(X,[1,2,3]),write(X)).
% O Resultado dessa chamada é: 123.


?- forall(between(1,5,I),(write(I*I),write(' '))).
% O Resultado dessa chamada é: 1*1 2*2 3*3 4*4 5*5
 
?- forall(between(10,20,I),write(I:' ')).
% O resultado dessa chamada é: 10: 11: 12: 13: 14: 15: 16: 17: 18: 19: 20: