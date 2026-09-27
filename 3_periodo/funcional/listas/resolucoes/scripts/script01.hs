-- Definição dos tipos básicos
type Dia = Int
type VendaR = Int

-- Define o período de recursão
periodo :: Int
periodo = 7

-- Tabela de vendas - função que retorna o valor de venda para cada dia
f :: Int -> Int
f 1 = 41
f 2 = 72
f 3 = 48
f 4 = 2
f 5 = 91
f 6 = 55
f 7 = 30
f _ = 0

{- 
  Retorna o total de vendas do período 
  Complexidade: O(d) onde d é o número de dias
-}
totalVendas :: Int -> Int
totalVendas 0 = 0
totalVendas d = f d + totalVendas (d-1)

----------------------------------------------------------------------
{-
  Encontra o dia em que mais se vendeu no período - versão 01
  Retorna uma tupla com o dia de maior venda e o número de testes realizados
-}

-- Função auxiliar para comparar as vendas de dois dias
compara :: Int -> Int -> (Int, Int) -> (Int, Int)
compara x t (dia_anterior, t_anterior)
  | f x >= f dia_anterior = (x, t)
  | otherwise             = (dia_anterior, t_anterior)

-- Função principal que encontra o dia de maior venda
diaMaiorVenda01 :: Int -> Int -> (Int, Int)
diaMaiorVenda01 1 t = (1, t)
diaMaiorVenda01 x t = compara x t (diaMaiorVenda01 (x-1) (t+1))

----------------------------------------------------------------------
{-
  Encontra o dia em que mais se vendeu no período - versão 02
  Tem como parâmetros o período, a maior venda e o contador de testes
-}
diaMaiorVenda02 :: Int -> Int -> Int -> (Int, Int)
diaMaiorVenda02 1 _ t = (1, t)
diaMaiorVenda02 y v t
  | f y == v  = (y, t+1)
  | otherwise = diaMaiorVenda02 (y-1) v (t+1)

------------------------------------------------------------------------
{- 
  Encontra o maior valor entre dois inteiros 
  Retorna uma tupla com o maior valor e o contador de testes atualizado
-}
maxi :: Int -> Int -> Int -> (Int, Int)
maxi m n t
  | m >= n    = (m, t)
  | otherwise = (n, t)

------------------------------------------------------------------------
{- 
  Encontra a maior venda - versão 01
  Implementação com apenas dois parâmetros e usando maxi no código interno
  Retorna uma tupla com o valor da maior venda e o número de testes realizados
-}
maiorVenda01 :: Int -> Int -> (Int, Int)
maiorVenda01 0 t = (0, t)
maiorVenda01 x t = maxi (f x) (fst (maiorVenda01 (x-1) (t+1))) (snd (maiorVenda01 (x-1) (t+1)))

------------------------------------------------------------------------
{- 
  Encontra a maior venda - versão 02 
  Abordagem alternativa que mantém o maior valor encontrado até o momento
-}
maiorVenda02 :: Int -> Int -> Int -> (Int, Int)
maiorVenda02 0 y t = (y, t)
maiorVenda02 x y t
  | f (x-1) > y = maiorVenda02 (x-1) (f (x-1)) (t+1)
  | otherwise   = maiorVenda02 (x-1) y (t+1)

