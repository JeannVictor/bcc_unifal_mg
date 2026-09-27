{-15. A sequencia de Fibonacci é definida e conhecida na literatura. Os dois primeiros números são
0 e 1, e os seguintes são calculados como a soma dos dois anteriores na sequência. Defina a
função antFib que, dado um valor x, calcule a posição de x na sequencia de Fibonacci. Caso x
não esteja na sequência, retorne (-1).
{-exemplo-}
Main> antFib 13 = 7 -}

fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib x = fib (x - 1) + fib (x - 2)

auxFib :: Int -> Int -> Int
auxFib value cont
    | fib cont == value = cont
    | fib cont > value  = -1
    | otherwise         = auxFib value (cont + 1)

antFib :: Int -> Int
antFib x = auxFib x 0


