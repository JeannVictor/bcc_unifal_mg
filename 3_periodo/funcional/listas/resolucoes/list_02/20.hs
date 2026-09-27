{- 20.a Questão 26 - Lista 1 (Nova proposta): Faça em Haskell uma solução para o seguinte problema
utilizando list comprehension e/ou funções de alta ordem: Dada uma lista de caracteres [Char],
e um caractere a, retornar quantos caracteres da lista são iguais a a.
{-exemplo-}
Main> conta "ABCAABCDDA" "B" = 2 -}
-- Versão Normal 
conta1 :: String -> Char -> Int
conta1 [] _ = 0
conta1 (x:xs) y
    | x == y = 1 + conta1 xs y
    | otherwise =  conta1 xs y 

-- Versão com List Comprehension
conta2 :: String -> Char -> Int
conta2 xs y = sum[ 1| x <- xs , x == y]

-- Versão com Funções de Alta Ordem
conta3 :: String -> Char -> Int
conta3 xs y = length(filter (\x -> x == y) xs)

{- 20.b Questão 28 - Lista 1 (Nova proposta): Faça uma solução em Haskell utilizando list com-
prehension que, dada uma lista de inteiros, ela retorne uma lista com uma repetição de
cada elemento de acordo com seu valor.
{-exemplo-}
Main> proliferaInt [3,0,2,4,0,1] = [3,3,3,2,2,4,4,4,4,1] -}

-- Versão Normal 
repete:: Int -> Int -> [Int]
repete _ 0 = []
repete x y = x: repete x (y-1)

proliferaInt1:: [Int] -> [Int]
proliferaInt1 [] = []
proliferaInt1 (x:xs) =  repete x x ++ proliferaInt1 xs

-- Versão com List Comprehension
proliferaInt2:: [Int] -> [Int]
proliferaInt2 xs = concat[ replicate x x  | x <-  xs]

-- Versão com Funções de Alta Ordem
proliferaInt3:: [Int] -> [Int]
proliferaInt3 xs = foldr (++) [] (map (\x -> replicate x x) xs)

-- Eu basicamente eu vou concatenar com Foldr as listas, e com map pretendo gerar cada
-- lista de seus x repetidos