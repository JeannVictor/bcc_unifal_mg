{-5. Escreva, em Haskell, a definição de uma função fourPower que retorne o seu argumento elevado
à quarta potência. Use a função square dada em sala de aula na definição de fourPower.
fourPower :: Int -> Int-}
-- Função que dado um 'x', retorna o x².
square :: Int -> Int
square x = x * x

-- Função que dado um 'x', retorna o x⁴ (utilizando o square).
fourPower :: Int -> Int
fourPower x = square(x) * square(x) -- Poderia ser feita x*x*x*x