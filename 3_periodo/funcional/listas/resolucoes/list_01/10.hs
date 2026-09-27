{-Escreva, em Haskell, uma função que retorna o último dígito de um número inteiro.
lastDigit 1234 = 4 -}

lastDigit :: Int -> Int
lastDigit x
  |x >= 0 = x`mod`10 -- Se 'x' >= 0,usa o `mod`(Resto da divisão), por 10 
  |otherwise = x`rem`10 -- Se 'x' < 0,usa o `rem`(Resto inteiro da divisão),por 10