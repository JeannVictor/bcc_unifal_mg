{- Assunto: Listas e Tuplas -}

periodo :: Int
periodo = 7

maxi :: Int -> Int -> Int
maxi m n
  | m >= n    = m
  | otherwise = n

-- Tabela de vendas
vendas :: Int -> Int
vendas 0 = 0
vendas 1 = 41
vendas 2 = 72
vendas 3 = 48
vendas 4 = 0
vendas 5 = 91
vendas 6 = 55
vendas 7 = 30

-------------------------------------------------------------------------------
-- 01. Função que retorna uma lista de vendas
listaVendas :: Int -> [Int]
listaVendas (-1) = []
listaVendas x    = vendas x : listaVendas (x - 1)
-------------------------------------------------------------------------------
-- 02. Função que retorna [[Int]] com listas de dia e venda
listaDiaVendas :: Int -> [[Int]]
listaDiaVendas (-1) = []
listaDiaVendas d    = [d, vendas d] : listaDiaVendas (d - 1)

-------------------------------------------------------------------------------
-- 03. Função que ordena uma lista de inteiros
insere_ord :: Int -> [Int] -> [Int]
insere_ord x [] = [x]
insere_ord x (h:hs)
  | x < h     = x : h : hs
  | otherwise = h : insere_ord x hs

ordenaLista :: [Int] -> [Int]
ordenaLista []     = []
ordenaLista (x:xs) = insere_ord x (ordenaLista xs)

-------------------------------------------------------------------------------
-- 04. Função que ordena [[Int]] pelo primeiro Int de cada lista
ordenaListaLista :: [[Int]] -> [[Int]]
ordenaListaLista []     = []
ordenaListaLista (x:xs) = ordenaLista x : ordenaListaLista xs

-------------------------------------------------------------------------------
-- 05. Função que ordena as listas internas de [[Int]] e, em seguida, ordena a [[Int]]
insereListaOrdenada :: [Int] -> [[Int]] -> [[Int]]
insereListaOrdenada x [] = [x]
insereListaOrdenada x (h:hs)
  | head x <= head h = x : h : hs
  | otherwise        = h : insereListaOrdenada x hs

ordenaLILE :: [[Int]] -> [[Int]]
ordenaLILE []     = []
ordenaLILE (x:xs) = insereListaOrdenada (ordenaLista x) (ordenaLILE xs)

-------------------------------------------------------------------------------
-- 06. Função que gera uma lista de tuplas com dia e venda
listaTuplaDiaVenda :: Int -> [(Int, Int)]
listaTuplaDiaVenda (-1) = []
listaTuplaDiaVenda d    = (d, vendas d) : listaTuplaDiaVenda (d - 1)

-------------------------------------------------------------------------------
-- 07. Função que gera o total de vendas
totalVendasT :: [(Int, Int)] -> Int
totalVendasT []         = 0
totalVendasT ((_,b):xs) = b + totalVendasT xs

-------------------------------------------------------------------------------
-- 08. Função que retorna a maior venda
maiorVendaT :: Int -> [(Int, Int)] -> Int
maiorVendaT mv []          = mv
maiorVendaT mv ((_,b):xs) = maiorVendaT (maxi mv b) xs

-- 08b. Como implementar apenas com os parâmetros
maiorVendaT2 :: [(Int, Int)] -> Int
maiorVendaT2 [] = 0
maiorVendaT2 (x:xs)
  | snd x > maiorVendaT2 xs = snd x
  | otherwise               = maiorVendaT2 xs
  
-------------------------------------------------------------------------------
-- 09. Função que retorna os dias das maiores vendas
bigSales :: [(Int, Int)] -> Int -> [Int]
bigSales [] _ = []
bigSales ((d,v):xs) y
  | v == y    = d : bigSales xs y
  | otherwise = bigSales xs y

