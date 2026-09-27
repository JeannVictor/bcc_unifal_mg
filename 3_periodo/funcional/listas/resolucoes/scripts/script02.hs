{- 
Assunto: Listas

Os conceitos introdutórios sobre listas foram apresentados em sala.
Agora, considerando os casos mais simples, com apenas listas de inteiros,
implemente as funções abaixo, considerando os operadores ++ e :
  ++ (concatena listas)
   : (insere um elemento na lista)
-}

-------------------------------------------------------------------------------
-- 01. Função que soma os elementos de uma lista
sumList :: [Int] -> Int
sumList []     = 0
sumList (x:xs) = x + sumList xs

-------------------------------------------------------------------------------
-- 02. Localiza elemento em lista
searchList :: Int -> [Int] -> Bool
searchList _ [] = False
searchList x (y:ys)
  | x == y    = True
  | otherwise = searchList x ys

-------------------------------------------------------------------------------
-- 03. Remove todas as ocorrências de um número em uma lista
deleteList :: Int -> [Int] -> [Int]
deleteList _ [] = []
deleteList x (y:ys)
  | x == y    = deleteList x ys
  | otherwise = y : deleteList x ys

-------------------------------------------------------------------------------
-- 04. Informa o tamanho de uma lista
lengthList :: [Int] -> Int
lengthList []     = 0
lengthList (_:xs) = 1 + lengthList xs

-------------------------------------------------------------------------------
-- 05. Conta a ocorrência de um número em uma lista
contList :: Int -> [Int] -> Int
contList _ [] = 0
contList x (y:ys)
  | x == y    = 1 + contList x ys
  | otherwise = contList x ys

-------------------------------------------------------------------------------
-- 06. Inverte a lista
reverseList :: [Int] -> [Int]
reverseList []     = []
reverseList (x:xs) = reverseList xs ++ [x]

-------------------------------------------------------------------------------
-- 07. Inverte os elementos das listas internas
revertIntList :: [[Int]] -> [[Int]]
revertIntList []     = []
revertIntList (x:xs) = reverseList x : revertIntList xs

-------------------------------------------------------------------------------
-- 08. Exclui a penúltima ocorrência de um número na lista

-- Conta as ocorrências de um número
contList2 :: Int -> [Int] -> Int
contList2 _ [] = 0
contList2 x (y:ys)
  | x == y    = 1 + contList2 x ys
  | otherwise = contList2 x ys

-- Remove a penúltima ocorrência
penultimo :: Int -> Int -> [Int] -> [Int]
penultimo _ _ [] = []
penultimo x vezes (y:ys)
  | (x == y) && (vezes == 2) = ys
  | (x == y) && (vezes < 2)  = y : ys
  | (x == y) && (vezes > 2)  = y : penultimo x (vezes - 1) ys
  | otherwise                = y : penultimo x vezes ys

-------------------------------------------------------------------------------
{- Exercícios:

   Implementar as funções:
     myHead - recebe uma lista e retorna a cabeça
     myTail - recebe uma lista e retorna a cauda (sem a cabeça)
     myLast - recebe uma lista e retorna o último elemento
     myInit - recebe uma lista e retorna a lista sem o último elemento
-}

-- Retorna a cabeça da lista
myHead :: [x] -> x
myHead (x:_) = x

-- Retorna a cauda da lista
myTail :: [x] -> [x]
myTail (_:xs) = xs

-- Retorna o último elemento da lista
myLast :: [x] -> x
myLast [x]    = x
myLast (_:xs) = myLast xs

-- Retorna a lista sem o último elemento
myInit :: [x] -> [x]
myInit [x]    = []
myInit (x:xs) = x : myInit xs
