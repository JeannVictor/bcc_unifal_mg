{-4. Um inteiro positivo é perfeito se é igual à soma dos seus fatores, excluindo ele próprio. Utili-
zando list comprehension, defina a função perfects :: Int -> [Int] que retorna a lista de todos
os números perfeitos até o limite fornecido.
--exemplo
Main> perfects 500 = [6, 28, 496]-}

-- Versão Normal 
perfects1::Int -> [Int]
perfects1 x = perfects1_aux x

perfects1_aux :: Int -> [Int]
perfects1_aux x 
    | sum(divs x) == x  = x: perfects1_aux (x-1)
    | otherwise         =    perfects1_aux (x-1)

divs:: Int -> [Int]
divs x = [i | i <- [1 .. (x-1) ] , x `mod` i == 0 ] 

-- Versão com List Comprehension
perfects2:: Int -> [Int]
perfects2 x = [p | p <- [1 ..(x - 1)],sum[n | n <- [1 .. (p-1)], p `mod` n == 0 ] ==  p]


