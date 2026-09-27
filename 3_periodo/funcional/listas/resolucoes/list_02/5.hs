{-5. Mostre como a seguinte list comprehension [(x,y) | x <- [1,2,3], y <- [4,5,6]], com dois geradores,
pode ser reescrita utilizando duas list comprehensions contendo um único gerador. Dica: utilize
a função de concatenação e concatene uma à outra.
Main> [[(x,y)| y <- [4,5,6]] | x <- [1,2,3]] =
[[(1,4),(1,5),(1,6)],[(2,4),(2,5),(2,6)],[(3,4),(3,5),(3,6)]]-}

-- Essa questão pelo menos para mim foi díficil de entender o que realmente era pra fazer
-- Basicamente ele afirma que [(x,y) | x <- [1,2,3], y <- [4,5,6]], com dois geradores,
-- pode ser reescrita utilizando duas list comprehensions contendo um único gerador.
-- E também fornece que a função [[(x,y)| y <- [4,5,6]] | x <- [1,2,3]] gera
-- [[(1,4),(1,5),(1,6)],[(2,4),(2,5),(2,6)],[(3,4),(3,5),(3,6)]].
-- Portanto, a única coisa a se fazer para essa versão que gera os pares em lista de listas
-- é usar a função concat antes, e assim ela se torna uma lista...

croc = concat[[(x,y)| y <- [4,5,6]] | x <- [1,2,3]]








