{-22. Faça em Haskell uma solução para inverter os elementos de uma lista de Inteiros.
{-exemplo-}
Main> inverte [1,2,3,4,5,6,150] = [150,6,5,4,3,2,1] -}

inverte:: [Int] -> [Int]
inverte [] = []
inverte (head:tail) = inverte (tail) ++ [head]

