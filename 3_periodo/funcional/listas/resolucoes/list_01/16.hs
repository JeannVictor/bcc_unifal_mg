{-16. Escreva uma definição equivalente à exibida abaixo, mas usando apenas uma única cláusula
em casamento de padrão:

funny x y z
    | x > z = True
    | y >= x = False
    | otherwise = True -}

funny:: Int -> Int -> Int -> Bool
funny x y z = (x > z) || (y < x)  