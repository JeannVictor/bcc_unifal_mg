{-14. Questão 9 - Lista 1 (Nova proposta): Escreva, em Haskell, uma função que retorna quantos
múltiplos de um determinado inteiro tem em um intervalo fornecido utilizando list comprehen-
sion e funções de alta ordem. Por exemplo, o número 4 tem 2 múltiplos no intervalo de 1 a
10.
howManyMultiples 4 1 10 = 2 -}

-- Versão Normal
howManyMultiples1:: Int -> Int -> Int -> Int
howManyMultiples1 num inicio fim
    | inicio > fim = 0
    | inicio `mod` num == 0 = 1 + howManyMultiples1 num (inicio + 1) fim
    | otherwise             =     howManyMultiples1 num (inicio + 1) fim

-- Versão com List Comprehension
howManyMultiples2:: Int -> Int -> Int -> Int
howManyMultiples2 num inicio fim = sum[ 1| n <- [inicio ..fim], n `mod` num == 0 ]

-- Versão com Funções de Alta Ordem 
howManyMultiples3 :: Int -> Int -> Int -> Int
howManyMultiples3 num inicio fim = length (filter (\x -> x `mod` num == 0)[inicio ..fim])
-- Nessa versão eu basicamente gerei uma lista onde apenas os elementos que satisfaziam o filtro
-- entraram, ou seja, variei o x de inicio a fim, e usei o length apenas para conseguir o tam 
-- da lista que equivalente ao numero de elementos ....
