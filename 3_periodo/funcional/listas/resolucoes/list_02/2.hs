{-2. De maneira similar à função length, mostre como a função replicate :: Int -> a -> [a], que
retorna uma lista de elementos idênticos, pode ser definida utilizando list comprehension.
-- exemplo
Main> replicate 3 True = [True, True, True] -}

-- Versão Normal 
replicate1:: Int -> a -> [a]
replicate1 0 _ = []
replicate1 x y = y : replicate1 (x-1) y  

-- Versão com List Comprehension
replicate2:: Int -> a -> [a]
replicate2 x y = [y|_ <- [1 ..x]]