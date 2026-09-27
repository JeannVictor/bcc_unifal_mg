{-12. Um programador especificou a função allDifferent para identificar se três números inteiros são
todos diferentes entre si, da seguinte forma:
allDifferent::Int->Int->Int->Bool
allDifferent m n p = (m/=n) && (n/=p) -}

--(a) O que está errado nessa definição?
-- M ser diferente de N, não indica que M é diferente de P

--(b) Especifique corretamente uma função allDifferent para o propósito necessário.
allDifferent:: Int -> Int -> Int -> Bool
allDifferent m n p = (m /= n) && (n /= p) && (m /= p)