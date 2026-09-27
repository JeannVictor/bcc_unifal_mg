{-17. Questão 22 - Lista 1 (Nova proposta): Faça em Haskell uma solução para inverter os elementos
de uma lista de Inteiros utilizando list comprehension e funções de alta ordem.
{-exemplo-}
Main> inverte [1,2,3,4,5,6,150] = [150,6,5,4,3,2,1]-}

-- Função Normal 
inverte1 :: [a] -> [a]
inverte1 [] = []
inverte1 (x:xs) = inverte1 xs ++ [x]

-- Função com List Comprehension
inverte2:: [a] -> [a]
inverte2 xs = [xs !! x | x <- [length xs - 1, length xs - 2 .. 0]]

-- Versão com Funções de Alta Ordem
inverte3:: [a] -> [a]
inverte3 xs = foldr (:) [] (map (\x -> xs !! x) [length xs-1,length xs-2 ..0])

-- Versão com Funções de Alta Ordem (Chat)
inverte4 :: [a] -> [a]
inverte4 = foldr (\x acc -> acc ++ [x]) []
