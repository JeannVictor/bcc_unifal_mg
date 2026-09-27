-- 4. Escreva, em Haskell, a função invertInt::Int->Int que inverta os dígitos de um número inteiro.
-- Main> invertInt 123 = 321

digitos:: Int -> Int
digitos 0 = 0  -- Caso base: número 0 tem 0 dígitos (jeito da minha lógica funcionar).
digitos x = 1 + digitos (x `div` 10)  -- Conta quantos dígitos há em x, removendo um dígito a cada chamada recursiva.

invertInt::Int -> Int
invertInt 0 = 0  -- Caso base: a inversão de 0 continua sendo 0.
invertInt x = ( x `mod` 10 * ( 10 ^ (digitos x - 1))) + invertInt (x `div` 10)  

-- A lógica da função invertInt:
-- 1. Extrai o último dígito de x .
-- 2. Multiplica esse dígito pela potência de 10 correspondente à sua posição final após a inversão.
-- 3. Faz a chamada recursiva para processar os demais dígitos.
-- 4. Soma os valores obtidos em cada chamada, reconstruindo o número invertido.
