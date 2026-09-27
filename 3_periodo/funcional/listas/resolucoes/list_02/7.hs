{-7. O produto escalar de duas listas de inteiros xs e ys, de tamanho n, é dado pela soma do produto
dos inteiros correspondentes.
n=1
–
\ (xsi * ysi)
/
–
i=0
Mostre como a função scalarproduct :: [Int] -> [Int] -> Int, que retorna o produto escalar
de duas listas, pode ser definida utilizando list comprehension.
{-exemplo-}:
Main> scalarproduct [1,2,3] [4,5,6] = 32-}

-- Versão Normal
scalarproduct1:: [Int] -> [Int] -> Int
scalarproduct1 [] [] = 0
scalarproduct1 (x:xs) (y:ys) = (x*y) + scalarproduct1 xs ys

-- Versão com List Comprehension
scalarproduct2:: [Int] -> [Int] -> Int
scalarproduct2 xs ys  = sum[x * y | (x, y) <- zip xs ys]

-- Função zip, zipa duas os elementos "seguidos" de listas, e assim

