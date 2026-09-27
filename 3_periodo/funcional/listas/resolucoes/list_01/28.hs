{-28. Faça uma solução em Haskell que, dada uma lista de inteiros, ela retorne uma lista com uma
repetição de cada elemento de acordo com seu valor.
{-exemplo-}
Main> proliferaInt [3,0,2,4,0,1] = [3,3,3,2,2,4,4,4,4,1]-}

repete:: Int ->Int -> [Int]
repete _ 0  = []
repete x y
    | y > 0 = x : repete x (y-1) 

proliferaInt:: [Int] -> [Int]
proliferaInt [] = []
proliferaInt (x:xs) = repete x x ++ proliferaInt(xs)
