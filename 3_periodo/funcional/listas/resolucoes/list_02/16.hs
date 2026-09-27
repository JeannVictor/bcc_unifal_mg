{-16. Questão 20 - Lista 1 (Nova proposta): Implemente a função pushRight::String->Int->String,
que recebe uma string s e um número inteiro n e retorna uma nova string t com k caracteres
’>’ inseridos no início de s, utilizando list comprehension e funções de alta ordem. O valor de
k deve ser tal que o comprimento de t seja igual a n. Obs: se n é menor que o comprimento
de s, a função retorna a própria string s.
exemplo
Main> pushRight "abc" 5 = ">>abc"-}

-- Versão Normal 
pushRight1:: String -> Int -> String
pushRight1 x y 
    | y > length x = '>' : pushRight1 x (y-1) 
    | otherwise    =  x 

-- Versão com List Comprehension 
pushRight2 :: String -> Int -> String
pushRight2 x y = ['>'| _ <- [ 1.. (y - length x)]] ++ x

-- Versão com Funções de Alta Ordem
pushRight3 :: String -> Int -> String
pushRight3 x y = (map (\_ -> '>' )[1.. (y - length x)]) ++ x


