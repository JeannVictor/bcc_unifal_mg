% Professor: Luiz Eduardo da Silva    Disciplina: Programação Lógica
% Aluno: Jeann Victor Batista         R.A: 2024.1.08.014

%                                   Problema dos Missionários e Canibais
% Considere a solução apresentada em aula para o problema dos Missionários e Canibais:
% "Temos três missionários e três canibais que precisam atravessar um rio com um barco que tem capacidade para transportar,
% no máximo, duas pessoas. A restrição é que, em nenhuma margem, o número de canibais pode ser maior do que o de missionários,
% senão os missionários serão devorados. Pelo menos uma pessoa deve transportar o barco de uma margem para a outra. 
% Encontre a sequência de movimentos que resolva o problema."
% Você deverá implementar uma generalização do problema, onde são definidos:
% (1) o número de missionários e canibais na margem do rio
% (2) a capacidade do barco

%-----------------------------------------------------------------------------------
% REPRESENTAÇÃO DO ESTADO -> [M, C, L]
% "M" = Número de missionários na margem A
% "C" = Número de canibais na margem A
% "L" = Margem onde o barco está ('a' ou 'b')

%-----------------------------------------------------------------------------------
% EXPLICAÇÃO DAS VARIÁVEIS PRINCIPAIS
% "M"   = Número de missionários na margem A (também representado por "MA")
% "C"   = Número de canibais na margem A (também representado por "CA")
% "MB"  = Número de missionários na margem B
% "CB"  = Número de canibais na margem B
% "TM"  = Total de missionários definidos no problema
% "TC"  = Total de canibais definidos no problema
% "MNB" = Número de missionários no barco
% "CNB" = Número de canibais no barco

%-----------------------------------------------------------------------------------
% MODIFICADOR DE PARÂMETROS
total(3,3). % Total de missionários e canibais
capacidade_barco(2). % Capacidade do barco

%-----------------------------------------------------------------------------------
% FUNÇÃO PARA GERAR MOVIMENTOS DE ACORDO COM OS PARÂMETROS DEFINIDOS
movimento(M,C,MNB,CNB):-
    capacidade_barco(MAX),
    between(1,MAX,TotalPessoas), % Gera as possibilidades da qtd de pessoas no barco
    between(0,TotalPessoas,MNB), % Gera a qtd de missinários no barco
    CNB is TotalPessoas - MNB,
    MNB =< M,
    CNB =< C.

%-----------------------------------------------------------------------------------
% FUNÇÃO QUE VERIFICA SE UM ESTADO É SEGURO
% (Não permite mais canibais do que missionários em nenhuma margem)
seguro([M, C, _]):-
    total(TM,TC),
    M >= 0, % Número de Missionarios em A tem que ser maior que 0
    C >= 0, % Número de Canibais em A tem que ser maior que 0
    M =< TM, % Número de Missionários em A tem que ser menor que o total de Missionários
    C =< TC, % Número de Canibais em A tem que ser menor que o total de Canibais
    (M == 0; M >= C), % Verifica se a margem A está segura.
    MB is TM - M, % Obtem qtd de Missionários na margem B
    CB is TC - C, % Obtem qtd de Canibais na margem B
    (MB == 0; MB >= CB). % Verifica se a margem B está segura.

%-----------------------------------------------------------------------------------
% FUNÇÕES RESPONSÁVEIS PELOS MOVIMENTOS DE (IDA/VOLTA)
% IDA (da margem A para a margem B)
oper(EstadoInicial, EstadoFinal):-  
    EstadoInicial = [M,C,a],
    movimento(M,C,MNB,CNB),
    MA is M - MNB, % Missionários na margem A = Missionários anteriores na margem A - Missionários no barco
    CA is C - CNB, % Canibais na margem A = Canibais anteriores na margem A - Canibais no barco
    seguro([MA,CA,b]), % Verifica se o novo estado é seguro
    EstadoFinal = [MA,CA,b]. % Aplica o estado final após a ida da margem A para a margem B

% VOLTA (da margem B para a margem A)
oper(EstadoInicial, EstadoFinal):-  
    EstadoInicial = [M,C,b],
    total(MT,CT),
    MB is MT - M, % Missionários na margem B = Total de missionários - Missionários na margem A
    CB is CT - C, % Canibais na margem B = Total de canibais - Canibais na margem A
    movimento(MB,CB,MNB,CNB), 
    MA is M + MNB, % Missionários na margem A = Missionários anteriores + Missionários no barco
    CA is C + CNB, % Canibais na margem A = Canibais anteriores + Canibais no barco
    seguro([MA,CA,a]), % Verifica se o novo estado é seguro
    EstadoFinal = [MA,CA,a]. % Aplica o estado final após a volta da margem B para a margem A

%-----------------------------------------------------------------------------------
% REPRESENTAÇÃO DOS ESTADOS INICIAL E FINAL
estado_inicial([M, C, a]) :-
    total(M, C).

estado_final([0,0,b]).

%-----------------------------------------------------------------------------------
% ALGORITMO DE BUSCA EM LARGURA (baseado no exemplo do Moodle)

% Funções auxiliares para a busca
inicial(E) :- estado_inicial(E). % Define o estado inicial
meta(E) :- estado_final(E). % Define o estado final

atingemeta([_-E|_]) :- meta(E). % Verifica se o estado atual é o estado final

naorepete(_-E,C) :- not(member(_-E,C)). % Garante que o estado ainda não foi visitado no caminho

% Gera possíveis novos estados a partir do caminho atual
estende([OperacaoX-EstadoA|Caminho], [EstadoB-EstadoB,OperacaoX-EstadoA|Caminho]) :-  
   oper(EstadoA,EstadoB),
   naorepete(EstadoB-EstadoB,Caminho).

%-----------------------------------------------------------------------------------
busca([Caminho|_], Solucao) :- 
    atingemeta(Caminho),
    !,
    Solucao = Caminho.

busca([Caminho|Lista], Solucao) :- 
    findall(UMAEXT, estende(Caminho,UMAEXT), EXT),
    append(EXT, Lista, Lista1),
    busca(Lista1, Solucao).

%-----------------------------------------------------------------------------------
% Funções responsáveis por exibir a solução encontrada
escreve([]).
escreve([Estado-_|Resto]) :-
    write(Estado), write(' -> '),
    escreve(Resto).

resolva :-
    inicial(X),                           
    (   busca([[X-X]], S) ->          
        (   write('Solução encontrada: '), nl,
            reverse(S, L),                
            escreve(L),
            write('Fim da solução'), nl)
        ;   
        (   write('ERRO: Não foi possível encontrar uma solução!'), nl)
    ).
