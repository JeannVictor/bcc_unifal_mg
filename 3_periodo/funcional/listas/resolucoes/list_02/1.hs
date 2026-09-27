{-1. Utilizando list comprehension, gere uma expressão que calcule 12 + 22 + ...1002.-}
-- Versão Normal 
powerOfTwo1::Int -> [Int]
powerOfTwo1 x = reverse(powerOfTwo1_aux x)
powerOfTwo1_aux :: Int -> [Int]
powerOfTwo1_aux 0 = []
powerOfTwo1_aux x = x ^ 2 : powerOfTwo1_aux (x-1)

-- Versão com List Comprehension
powerOfTwo2 :: Int -> [Int]
powerOfTwo2 x = [ n^2 | n <- [1 ..x]]

