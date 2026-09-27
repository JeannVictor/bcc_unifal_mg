{-32. Construa uma função em Haskell que recebe 4 inteiros e devolve uma tupla-4 com os quatros
valores originais, só que ordenados.
{-exemplo-}
Main> ordena 3 5 1 (-3) = (-3, 1, 3, 5)-}

insere_ord:: Int -> [Int] -> [Int]
insere_ord x [] = [x]
insere_ord x (y:ys)
    | x < y     = x :(y:ys)
    | otherwise = y: insere_ord x ys

ordena_lista:: [Int] -> [Int]
ordena_lista [] = []
ordena_lista (x:xs) = insere_ord x (ordena_lista xs)

ord_tup:: [Int] -> (Int,Int,Int,Int)
ord_tup [a,b,c,d] = (a,b,c,d)

ordenaT:: Int ->Int ->Int ->Int ->(Int,Int,Int,Int)
ordenaT a b c d = ord_tup (ordena_lista [a,b,c,d])