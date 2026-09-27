-- 21. Defina um operador binário de nome &-, com a semântica: x &- y = x - 2*y.

{- Qual é o resultado da avaliação da expressão 10 &- 3 &- 2?
    Explique esses resultados. -}

-- (a) infixl 6 &-
infixl 6 &-
(&-) :: Int -> Int -> Int
x &- y = x - 2 * y
-- Neste caso, a associatividade é à esquerda.
-- Portanto, a expressão é interpretada como: (10 &- 3) &- 2
-- (10 - 2*3) &- 2 = 4 &- 2 = 4 - 2*2 = 0
-- O resultado dessa operação é: 0
-----------------------------------------------------------------------------------------------------------

-- (b) infixr 6 &-
infixr 6 &-
(&-) :: Int -> Int -> Int
x &- y = x - 2 * y
-- Aqui, a associatividade é à direita.
-- Assim, a expressão é interpretada como: 10 &- (3 &- 2)
-- Primeiro: 3 &- 2 = 3 - 2*2 = -1
-- Depois: 10 &- (-1) = 10 - 2*(-1) = 10 + 2 = 12
-- O resultado dessa operação é: 12
-----------------------------------------------------------------------------------------------------------

-- (c) infix 6 &-
infix 6 &-
(&-) :: Int -> Int -> Int
x &- y = x - 2 * y
-- Neste caso, o operador não possui associatividade.
-- Portanto, a expressão 10 &- 3 &- 2 é ambígua e não pode ser interpretada sem parênteses.
-- Resultado: erro de compilação
-- Mensagem de erro: cannot mix ‘&-’ [infix 6] and ‘&-’ [infix 6] in the same infix expression
-----------------------------------------------------------------------------------------------------------

{- Qual é o resultado da avaliação da expressão 10 &- 3 * 2, caso o operador seja definido
como: (a) infix 6 &-; e (b) infix 8 &-? Explique esses resultados. -}

-- (a) infix 6 &-
infix 6 &-
(&-) :: Int -> Int -> Int
x &- y = x - 2 * y
-- Neste caso, a precedência do operador &- (nível 6) é menor que a da multiplicação (*) (nível 7).
-- Assim, a multiplicação é avaliada primeiro: 3 * 2 = 6
-- Depois: 10 &- 6 = 10 - 2*6 = 10 - 12 = -2
-- O resultado dessa operação é: -2
-----------------------------------------------------------------------------------------------------------

-- (b) infix 8 &-
infix 8 &-
(&-) :: Int -> Int -> Int
x &- y = x - 2 * y
-- Aqui, a precedência do operador &- (nível 8) é maior que a da multiplicação (*) (nível 7).
-- Portanto, a expressão é avaliada como: (10 &- 3) * 2
-- Primeiro: 10 &- 3 = 10 - 2*3 = 4
-- Depois: 4 * 2 = 8
-- O resultado dessa operação é: 8
