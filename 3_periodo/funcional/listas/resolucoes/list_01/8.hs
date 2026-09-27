-- 8. Considere a função escrita na linguagem C que calcula o máximo denominador comum entre dois números:
-- Escreva uma função, em Haskell, que calcule o MDC de maneira recursiva.

mdc::Int -> Int -> Int
mdc m 0 = m
mdc m n
    | mod m n /= 0 = mdc n ( mod m n)
    | otherwise    = n
    





