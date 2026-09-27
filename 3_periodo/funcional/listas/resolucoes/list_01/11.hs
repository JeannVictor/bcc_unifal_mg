{-11. Escreva, em Haskell, uma função que retorna o dígito de um número inteiro de acordo com a
posição informada.
anyDigit 0 7689 = 7
anyDigit 2 7689 = 8
anyDigit 9 7689 = -1-}

digitos:: Int -> Int
digitos 0 = 1  -- Caso base: número 0 tem 0 dígitos (jeito da minha lógica funcionar).
digitos x = 1 + digitos (x `div` 10)  -- Conta quantos dígitos há em x, removendo um dígito a cada chamada recursiva.

anyDigit:: Int -> Int -> Int
anyDigit dig num
    |dig >= digitos num = -1
    

-- A minha ideia é trabalhar com o numero invertido, depois que eu inverter o numero eu iria fazer o resto da divisão ate a 
--quantidade de vezes que a pessoa quer o digito, OU seja dado  0 123, tenho que retornar um, inverto pra 321 e faço o resto da divisão por 10 uma vez
-- Tenho a função que inverte o valor,tenho a função que identifica a quantidade de digitos e creio que precisaria implementar algo para meio que contar
-- quantas vezes posso fazer o resto da divisão

--  0 123, tenho que fazer uma função auxiliar que divida um o numero dig -1 vezes ...