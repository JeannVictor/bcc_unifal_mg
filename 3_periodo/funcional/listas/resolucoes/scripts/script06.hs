import Data.Char (chr, ord)

--------------------------------------------------------------------------------
{- 01. Função que retorna lista de duplas com char e posição na ASCII -}

-- Função para converter número para char
intToChar :: Int -> Char
intToChar 0 = '0'
intToChar x = chr (x + 96)

-- Sem ordem padrão e sem uso do where
listaDuplaCharInt :: Int -> [(Char, Int)]
listaDuplaCharInt 0 = []
listaDuplaCharInt x = (intToChar x, ord (intToChar x)) : listaDuplaCharInt (x-1)

-- Com ordem padrão e uso do where
listaDuplaCharIntW :: Int -> [(Char, Int)]
listaDuplaCharIntW 0 = []
listaDuplaCharIntW x = reverse (aux x)
  where
    aux 0 = []
    aux y = (intToChar y, ord (intToChar y)) : aux (y-1)

--------------------------------------------------------------------------------
{- 02. Função meuChar que pesquisa um char pelo int na lista gerada -}

meuChar :: [(Char, Int)] -> Int -> Char
meuChar [] _ = '\0'
meuChar (x:xs) asc
  | snd x == asc = fst x
  | otherwise    = meuChar xs asc

--------------------------------------------------------------------------------
{- 03. Função meuOrd que pesquisa o int pelo char na lista gerada -}

meuOrd :: [(Char, Int)] -> Char -> Int
meuOrd [] _ = 0
meuOrd (x:xs) y
  | fst x == y = snd x
  | otherwise  = meuOrd xs y

--------------------------------------------------------------------------------
{- 04. Função que ordena uma lista de inteiros -}

insereordenado :: Int -> [Int] -> [Int]
insereordenado x [] = [x]
insereordenado x (y:ys)
  | x < y     = x : (y:ys)
  | otherwise = y : insereordenado x ys

ordenaLista :: [Int] -> [Int]
ordenaLista [] = []
ordenaLista (x:xs) = insereordenado x (ordenaLista xs)

--------------------------------------------------------------------------------
{- 05. Seja o tipo [(Bool, [Int])].
      Faça uma função que ordena [Int] quando o booleano é True.
      Também, passe o Bool para False, quando ordenar [Int].
      
      Exemplo:
      ordenaListaDupla [(True, [3,4,1,0,9]), (False, []), (True, [4,3,2,1,0])]
      retorna: [(False, [0,1,3,4,9]), (False, []), (False, [0,1,2,3,4])]
-}

ordenaListaDupla :: [(Bool, [Int])] -> [(Bool, [Int])]
ordenaListaDupla [] = []
ordenaListaDupla (x:xs)
  | fst x == True = (False, ordenaLista (snd x)) : ordenaListaDupla xs
  | otherwise     = x : ordenaListaDupla xs
