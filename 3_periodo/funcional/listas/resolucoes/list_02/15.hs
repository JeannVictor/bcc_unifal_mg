{-15. Questão 19 - Lista 1 (Nova proposta): Implemente a função duplicate::String ->Int->String
que recebe uma string s e um número inteiro n, utilizando list comprehension e funções de alta
ordem. A função deve retornar a concatenação de n cópias de s. Se n for zero, retorna . Como
dica, usar o operador de concatenação pré-definido (++)::String->String->String.-}

-- Versão Normal 
duplicate1 :: String -> Int -> String
duplicate1 _ 0 = []
duplicate1 x y = x ++ duplicate1 x (y-1)

-- Versão com List Comprehension
duplicate2 :: String -> Int -> String
duplicate2 x y = concat[ x | _ <- [1 .. y]] 

-- Versão com Funções de Alta Ordem 
duplicate3 :: String -> Int -> String
duplicate3 x y = foldr (++) "" (map (\_ -> x )[1 ..y])

-- A função map é utilizada para gerar a lista de todas as repetições de x 
-- Ex : map (map (\_ -> x )[1 ..y] para x = go e y = 3 gera :
-- ["go","go","go"]
-- Ai entra a função foldr com (++) "" , (++) é a operação a ser aplicada na lista
-- E tem o "" para ser o valor inicial

