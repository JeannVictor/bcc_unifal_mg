% 14. Considere o seguinte problema: “Há dois jarros com capacidades de 3 e 4 litros,
% respectivamente. Nenhum dos jarros contém qualquer medida ou escala, de modo que só
% se pode saber o conteúdo exato quando eles estão cheios. Sabendo-se que podemos
% encher ou esvaziar um jarro, bem como transferir água de um jarro para outro, encontre
% uma sequência de passos que deixe o jarro de 4 litros com exatamente 2 litros de água”.
% Considere que o estado inicial pode ser representado pela lista [0,0], indicando que os
% jarros de 3 e 4 litros estão vazios inicialmente e a meta é [_,2]. Complete os predicados
% transforma abaixo para descrever todas as transformações possíveis de estados desse
% problema.

%transforma('encher o jarro 1', [X,Y], [3,Y]) :- X < 3.
%transforma('enchar o jarro 2', ...
%transforma('esvaziar o jarro 1', ...
%transforma('esvaziar o jarro 2', ...
%transforma('transferir do jarro 1 para o 2', ...
%transforma('transferir do jarro 2 para o 1', ...
%--- considerando que ainda restara agua no jarro de origem
%transforma('transferir do jarro 1 para o 2', ...
%transforma('transferir do jarro 2 para o 1', ...

%Resolução 
transforma('encher o jarro 1', [X,Y], [3,Y]) :- X < 3.
transforma('encher o jarro 2', [X,Y], [X,4]) :- Y < 4.
transforma('esvaziar o jarro 1', [X,Y],[0,Y]):- X > 0.
transforma('esvaziar o jarro 2', [X,Y],[X,0]):- Y > 0.
transforma('transferir do jarro 1 para o 2',[X,Y],[0,T]):- X > 0, Y < 4,X + Y =< 4, T is X+Y.
transforma('transferir do jarro 2 para o 1',[X,Y],[T,0]):- X < 3, Y > 0,X + Y <= 3, T is X+Y.
transforma('transferir do jarro 1 para o 2',[X,Y],[J1,4]):- X > 0, Y < 4, J1 is (X + Y -4).
transforma('transferir do jarro 2 para o 1',[X,Y],[3,J2]):- Y > 0, X < 3, J2 is  (X + Y -3).