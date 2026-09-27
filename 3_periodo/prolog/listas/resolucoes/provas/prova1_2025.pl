% Resolução da Prova 1 de Programação Lógica 2025/1

%--- Questão 1 --- 
% Converta a fórmula (A ∧ ¬B) → (C ∧ D) na Forma Normal Conjuntiva (conjunção de disjunções).  
% Apresente os passos da conversão. Sugestão de operações:  
Passos:
1. ¬(A ∧ ¬B) ∨ (C ∧ D)  (Eliminação da implicação)
2. (¬A ∨ ¬¬B) ∨ (C ∧ D)  (Leis de De Morgan)
3. (¬A ∨ B) ∨ (C ∧ D)    (Eliminação dupla negação)
4. (¬A ∨ B ∨ C) ∧ (¬A ∨ B ∨ D)  (Distributividade)

FNC final:
(¬A ∨ B ∨ C) ∧ (¬A ∨ B ∨ D)

%--- Questão 2 ---   
% Considere a seguinte descrição da "Família Silva":  
% "A família Silva foi uma importante família da Região. João e Maria tiveram os filhos Cláudia e Alberto. 
% Cláudia casou-se com Lucas que era filho de Pedro e Regina e tiveram os filhos Leandro e Leonardo. Alberto casou-se com Jasmine que era filha de Júlio e Júlia e tiveram os filhos chamados Eduardo e Alice."  
% Desenhe a árvore genealógica e represente-a usando as relações familiares pai e mãe.  

% Árvore genealógica da Família Silva:

João e Maria
├── Cláudia (casada com Lucas, filho de Pedro e Regina)
│   ├── Leandro
│   └── Leonardo
└── Alberto (casado com Jasmine, filha de Júlio e Júlia)
    ├── Eduardo
    └── Alice

Representação Prolog:
pai(joao, claudia).
mae(maria, claudia).
pai(joao, alberto).
mae(maria, alberto).

pai(pedro, lucas).
mae(regina, lucas).

pai(lucas, leandro).
mae(claudia, leandro).
pai(lucas, leonardo).
mae(claudia, leonardo).

pai(julio, jasmine).
mae(julia, jasmine).

pai(alberto, eduardo).
mae(jasmine, eduardo).
pai(alberto, alice).
mae(jasmine, alice)

%--- Questão 3 ---  
% Considerando as relações pai e mãe da questão anterior, escreva a regra Prolog para a relação familiar primo.  

primo(X, Y) :-
    % Primas por parte de pai (pai em comum)
    pai(PaiX, X), pai(PaiY, Y), pai(Avo, PaiX), pai(Avo, PaiY), PaiX \= PaiY;
    
    % Primas por parte de mãe (mãe em comum)
    mae(MaeX, X), mae(MaeY, Y), mae(Avo, MaeX), mae(Avo, MaeY), MaeX \= MaeY;
    
    % Caso onde X é filho do pai e Y é filho da mãe (irmãos do mesmo casal)
    pai(PaiX, X), mae(MaeY, Y), pai(Avo, PaiX), mae(Avo, MaeY), \+irmaos(PaiX, MaeY);
    
    % Caso onde X é filho da mãe e Y é filho do pai (irmãos do mesmo casal)
    mae(MaeX, X), pai(PaiY, Y), mae(Avo, MaeX), pai(Avo, PaiY), \+irmaos(MaeX, PaiY).
    
irmaos(X, Y) :- pai(P, X), pai(P, Y), mae(M, X), mae(M, Y), X \= Y.

%--- Questão 4 ---   
% Considere o seguinte predicado Prolog de lista nonono/2:  

%nonono([A, _], A) := !.  
%nonono([_|B], C) := nonono(B,C).  

%a) Qual é o resultado para a consulta: ?- nonono([2,5,1], X).  
O resultado da consulta é 5.

%b) Escolha um nome sugestivo para o predicado nonono.  
penultimo_Lista

%--- Questão 5 ---  
% Escreva um predicado Prolog compara/2, que retorna true se as duas listas são equivalentes (contém o mesmo número de elementos) sem usar outro predicado auxiliar. Exemplo de uso:  

%?- compara([1,2,3],[4,luiz,3]).  
%true  
%?- compara([1,2],[3,4,5]).  
%false.

compara([], []).
compara([_|Cauda1], [_|Cauda2]) :-
    compara(Cauda1, Cauda2).