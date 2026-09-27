{-13. Utilizando list comprehension, defina a função insertOrd :: Int -> [Int] -> [Int] que, dada uma
lista de inteiros ordenada, insere na lista o parâmetro passado mantendo a lista ordenada.
--exemplo
Main> insertOrd 4 [0,1,2,5,6] = [0,1,2,4,5,6]-}

-- Versão Normal 
insertOrd1:: Int -> [Int] -> [Int]
insertOrd1 x [] = [x]
insertOrd1 x (y:ys)
    | x < y = x : (y:ys)
    | otherwise = y:insertOrd1 x ys

-- Versão com List Comprehension
insertOrd2:: Int -> [Int] -> [Int]
insertOrd2 x ys = [y| y <- ys , y < x] ++ [x] ++ [y| y <- ys, y > x]
