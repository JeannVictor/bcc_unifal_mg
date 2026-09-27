--2. Localize, explique e corrija o erro na função que deve calcular o fatorial de um número, como se segue:
--fat::Int->Int
--fat x = x * fat(x-1)

-- O erro dessa função fatorial é não ter uma parada,assim ela vai cair num loop infinito

fat :: Int -> Int
fat 0 = 1 -- Caso base: Fatorial de 0 é 1.
fat x = x * fat(x-1)