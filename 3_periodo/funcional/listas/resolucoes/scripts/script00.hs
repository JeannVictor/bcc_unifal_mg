import Data.Char

type Dia = Int
type Venda = Int

-- Função que retorna a venda de acordo com o dia
f :: Dia -> Venda
f 1 = 9
f 2 = 7
f 3 = 15
f 4 = 14
f 5 = 8
f 6 = 0
f 7 = 3
f x = -1

-- Exercícios:

{- 
  Função que retorne a maior venda da semana 
-}
maiorVenda :: Dia -> Venda -> Venda
maiorVenda 0 v = v
maiorVenda d v
  | f d > v    = maiorVenda (d-1) (f d)
  | otherwise  = maiorVenda (d-1) v

{- 
  Função que retorne o dia em que houve a maior venda
  1° parâmetro = Escolha o período a ser analisado. Ex: 7
  2° parâmetro = Pode ser qualquer valor diferente de 1 a 7.
-}
diaMaiorVenda :: Dia -> Dia -> Int
diaMaiorVenda 0 md = md
diaMaiorVenda d md
  | f d > f md = diaMaiorVenda (d-1) d
  | otherwise  = diaMaiorVenda (d-1) md

{- 
  Função que retorne a quantidade de vendas do período
  1° parâmetro = Escolha o período a ser analisado. Ex: 7
-}
vendasPeriodo :: Dia -> Int
vendasPeriodo 0 = 0
vendasPeriodo x = f x + vendasPeriodo (x-1)

{- 
  Função que retorne a média de vendas 
-}
mediaVendas :: Dia -> Int
mediaVendas 0 = 0
mediaVendas x = vendasPeriodo x `div` x

-----------------------------------------------------------------------------------------
-- Funções que o Eliseu passou em sala de aula:

-- Período de dias padrão
periodo :: Int
periodo = 7

-- Exemplo de resposta
answer :: Int
answer = 42

-- Função que calcula o quadrado de um número
square :: Int -> Int
square x = x * x

-- Função que soma dois números
soma :: Int -> Int -> Int
soma z k = z + k

-- Função que testa se três números são iguais
allEqual :: Int -> Int -> Int -> Bool
allEqual m n p = (m == n) && (n == p)

-- Função que retorna o maior de dois números
maxi :: Int -> Int -> Int
maxi m n
  | m >= n    = m
  | otherwise = n

-- Resultado da maior venda no período
maiorV7 :: Int
maiorV7 = maiorVenda periodo 0
