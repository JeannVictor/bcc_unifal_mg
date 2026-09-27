{-13. Escreva uma função howManyEqual que retorne quantos dos três números inteiros fornecidos
como argumentos são iguais. A resposta poderá ser 3 (todos iguais), 2 (dois iguais e o terceiro
diferente) ou 0 (todos diferentes).
howManyEqual::Int->Int->Int->Int -}

howManyEqual::Int->Int->Int->Int
howManyEqual x y z
    | (x == y) && (y == z)             = 3 -- Se os 3 forem iguais = 3
    | (x /= y) && (y /= z) && (x /= z) = 0 -- Se nenhum for igual = 0
    | otherwise                        = 2 -- Se nenhuma das condições anteriores forem satisfeitas, 2
