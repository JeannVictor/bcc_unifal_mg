% 13. Usando findall, defina e teste os predicados pred1/2, pred2/2 e pred3/2 que modificam
% uma lista, conforme ilustrado nos seguintes exemplos:

% ?- pred1([a,b,c,d,e],L).
% L = [[a],[b],[c],[d],[e]]
pred1(X,Y):-
    findall([A],member(A,X),Y).

% ?- pred2([a,b,c,d,e],L).
% L = [pred(a,a),pred(b,b),pred(c,c),pred(d,d),pred(e,e)]
pred2(X,Y):-
    findall(pred(A,A),member(A,X),Y).

% ?- pred3([a,b,c,d,e],L).
% L = [[element,a],[element,b],[element,c],[element,d],[element,e]]
pred3(X,Y):-
    findall([element,A],member(A,X),Y).