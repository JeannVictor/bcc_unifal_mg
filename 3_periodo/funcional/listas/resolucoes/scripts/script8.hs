import Data.Char

--------------------------------
--zip [1,2,3] ["a","bb", "ccc"]
--unzip $$
--------------------------------

{- função que multiplica por x cada elemento de uma lista -}
mult:: Int -> [Int] -> [Int]
mult y xs = [y * x |x <- xs]
----------------------------------------------------------------------------------
{- função que filtra os pares e os multiplica por x-}
multPar:: Int -> [Int] -> [Int]
multPar y xs = [ y * x |x <- xs, x `mod` 2 == 0]

----------------------------------------------------------------------------------
{- função que multiplica por x apenas os números pares de uma lista -}

-- Versão Desordenada
multOnlyPar:: Int -> [Int] -> [Int]
multOnlyPar y xs = [ x| x <- xs , x `mod` 2 /= 0] ++ [x * y| x <- xs , x `mod` 2 == 0]

-- Versão Ordenada
multOnlyParORD:: Int -> [Int] -> [Int]
multOnlyParORD y xs = ordena([ x| x <- xs , x `mod` 2 /= 0] ++ [x * y| x <- xs , x `mod` 2 == 0])

ordena:: [Int] -> [Int]
ordena [] = []
ordena (x:xs) = insere_ord x (ordena xs)

insere_ord :: Int -> [Int] -> [Int]
insere_ord x [] = [x]
insere_ord x (y:ys) 
    | x < y     = x : (y:ys)
    | otherwise = y: insere_ord x ys

----------------------------------------------------------------------------------
{- função que filtra os pares maiores que 5 e os multiplica por x- -}
multParBigger5:: Int -> [Int] -> [Int]
multParBigger5 y xs = [ y * x |x <- xs, x > 5 && x `mod` 2 == 0 ]
----------------------------------------------------------------------------------

{- função que filtra os pares ou maiores que 5 e os multiplica por x- -}
multParOrBigger5:: Int -> [Int] -> [Int]
multParOrBigger5 y xs = [ y * x |x <- xs, x > 5 || x `mod` 2 == 0 ]

----------------------------------------------------------------------------------
-- Função que faz um produto cartesiano entre duas listas
-- sendo uma dada como parâmetro e outra gerada dentro da função
cartesianProduct :: [Int] -> [(Int,Int)]
cartesianProduct xs =  [(x,y) | x <- xs , y <- [1,2 .. (length xs) ] ]