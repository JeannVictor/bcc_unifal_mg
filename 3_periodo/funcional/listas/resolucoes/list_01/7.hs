{-7. Escreva, em Haskell, uma função que informa de quantas maneiras é possível escolher n objetos
em uma coleção original de m objetos, para m ≥ n.-}

fat :: Int -> Int
fat 0 = 1 -- Caso base: Fatorial de 0 é 1.
fat x = x * fat(x-1) 

cfBinomial:: Int -> Int -> Int
cfBinomial m n = (fat m)`div`((fat n)* (fat (m-n))) 

-- Basicamente utilizei da fórmula de Análise combinatória:
-- É chamada de fórmula do coeficiente binomial
-- Exemplo para m e n:  (m!)/((n!)*(m-n)!)
