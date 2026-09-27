{-9. Escreva, em Haskell, uma função que retorna quantos múltiplos de um determinado inteiro tem
em um intervalo fornecido. Por exemplo, o número 4 tem 2 múltiplos no intervalo de 1 a 10.
howManyMultiples 4 1 10 = 2-}

type Inicio = Int
type Fim    = Int
type Valor  = Int 

howManyMultiples:: Int -> Valor -> Inicio-> Fim
howManyMultiples x y z
  |y > z            = 0 -- Caso base : Se o valor do inicio do intervalo > fim, já foram verificados todos os números.
  |(z `mod` x) == 0 = 1 + howManyMultiples x y (z - 1) -- Se fim do intervalo é múltiplo de x, adiciona 1 e verifica o próximo número.
  |otherwise        = howManyMultiples x y (z - 1) -- Senão apenas se verifica o próximo número
    
    