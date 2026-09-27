{- Objetivo: Trabalhar tipos distintos entre listas e tuplas -}

import Data.Char

------------------------------------------------------
{- 01 função que separa [(Int,Char)] em ([Int],[Char]) -}

listOfInt :: [(Int, Char)] -> [Int]
listOfInt [] = []
listOfInt (x:xs) = fst x : listOfInt xs

listOfChar :: [(Int, Char)] -> [Char]
listOfChar [] = []
listOfChar (x:xs) = snd x : listOfChar xs

myUnzip :: [(Int, Char)] -> ([Int], [Char])
myUnzip [] = ([], [])
myUnzip (x:xs) = (listOfInt (x:xs), listOfChar (x:xs))

------------------------------------------------------------
{- 02 versão em uma única função -}

myUnzipU :: [(Int, Char)] -> ([Int], [Char])
myUnzipU [] = ([], [])
myUnzipU ((int, chr):xs) = (int : ints, chr : chrs)
    where (ints, chrs) = myUnzipU xs

------------------------------------------------------------
{- 03 função que junta duas listas em lista de duplas -}

myZip :: [Bool] -> [Char] -> [(Bool, Char)]
myZip [] _ = []
myZip _ [] = []
myZip (b:bs) (c:cs) = (b, c) : myZip bs cs

---------------------------------------------------------------
{- 04 função que recebe [Char] e retorna [(Bool,Char)] 
   True se Char for alfanumérico e False, caso contrário -}

setAlfa :: String -> [(Bool, Char)]
setAlfa [] = []
setAlfa (x:xs)
  | isDigit x == True || isAlpha x == True = (True, x) : setAlfa xs
  | otherwise = (False, x) : setAlfa xs

------------------------------------------------------------------
{- 05 função que recebe [(Bool, Char)] e filtra alfanuméricos -}

filtraAlfa :: [(Bool, Char)] -> String
filtraAlfa [] = []
filtraAlfa (x:xs)
  | fst x == True = snd x : filtraAlfa xs
  | otherwise = filtraAlfa xs

------------------------------------------------------------------
{- 06 função que transforma String de alfa em [Int] -}

alfaToInt :: String -> [Int]
alfaToInt [] = []
alfaToInt (x:xs)
  | x >= 'a' && x <= 'z' = (ord x - 96) : alfaToInt xs
  | x >= 'A' && x <= 'Z' = (ord x - 64) : alfaToInt xs
  | otherwise = alfaToInt xs

---------------------------------------------------------------------
{- 07 função que gera tabela ASCII -}

geraASCII :: Int -> [(Int, Char)]
geraASCII x
  | x <= 127  = (x, chr x) : geraASCII (x + 1)
  | otherwise = []
