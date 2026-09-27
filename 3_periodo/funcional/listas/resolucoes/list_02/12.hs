{-12. Defina a função evenCubes :: Int -> [Int] que, dado um limite, retorne a lista do cubo dos nú
pares até o limite fornecido.
--exemplo
Main> evenCubes 10 = [8, 64, 216, 512]-}

-- Versão Normal
evenCubes1:: Int -> [Int]
evenCubes1 x = reverse (evenCubes1_aux x)

evenCubes1_aux:: Int -> [Int]
evenCubes1_aux 1 = []
evenCubes1_aux x
    | (x-1) `mod` 2 == 0  = (x-1)^3 :evenCubes1_aux (x-1)
    | otherwise           =  evenCubes1_aux (x-1)

-- Versão com List Comprehension
evenCubes2:: Int -> [Int]
evenCubes2 x = [p^3| p <- [2..(x-1)], (mod) p 2 == 0] 

