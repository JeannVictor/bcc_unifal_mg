% 11. O que está errado no programa abaixo? Rode-o com trace, para:
% ?- max(4,3,M) e
% ?- max(3,4,M)
max(X,Y,M):- X>Y, M=X.
max(X,Y,M):-!, X=<Y, M=Y.
% O erro do programa acima é: A primeira parte do predicado possuia um 'Stop' que faz com 
% que a segunda parte não seja feita, por isso quando se realizava alguma chamada do tipo
% ?- max(3,4,M), não rodava. Pois o programa parava apos a tentativa da primeira parte.
% Outro erro é que o "menor ou igual" foi escrito como <=, porém o correto é =<.