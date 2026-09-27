{-18. Questão 23 - Lista 1 (Nova proposta): Faça em Haskell uma solução para, dada uma lista
de inteiros, retornar uma dupla de listas de inteiros onde a primeira conterá os elementos
ímpares e a segunda os elementos pares passados como parâmetro. Utilize obrigatoriamente
list comprehension.
--exemplo
Main> separa [1,4,3,4,6,7,9,10] = ([1,3,7,9],[4,4,6,10])-}

-- Versão Normal
impar:: [Int] -> [Int]
impar [] = []
impar (x:xs) 
    | x `mod` 2 /= 0 = x:impar xs
    | otherwise      =   impar xs

par:: [Int] -> [Int]
par [] = []
par (x:xs) 
    | x `mod` 2 /= 1 = x:par xs
    | otherwise      =   par xs

separa1 :: [Int] -> ([Int],[Int])
separa1 x = (impar x,par x)

-- Versão com List Comprehension
separa2 :: [Int] -> ([Int],[Int])
separa2 xs = ([ x|x <- xs, x `mod` 2 /= 0 ],[ x|x <- xs, x `mod` 2 == 0 ])

-- Versão com Funções de Alta Ordem
separa3 :: [Int] -> ([Int],[Int])
separa3 xs = 