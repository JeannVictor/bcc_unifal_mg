-- 27. Para uma lista de inteiros ordenada qualquer,
-- fazer uma função que retorne uma lista ordenada sem elementos repetidos.

-- Inserção ordenada de um elemento em uma lista
insereOrdenado :: Int -> [Int] -> [Int]
insereOrdenado x [] = [x]
insereOrdenado x (h:s)
    | x < h     = x : (h:s)
    | otherwise = h : insereOrdenado x s

-- Ordena uma lista usando inserção
ordenaLista :: [Int] -> [Int]
ordenaLista [] = []
ordenaLista (h:t) = insereOrdenado h (ordenaLista t)

--------------------------------------------------------

-- Verifica se um número existe na lista
verifica :: Int -> [Int] -> Bool
verifica _ [] = False
verifica n (x:xs)
    | n == x    = True
    | otherwise = verifica n xs

-- Verifica se o primeiro elemento da lista aparece novamente no resto da lista
pertence :: [Int] -> Bool
pertence (x:xs) = verifica x xs

-- Remove elementos duplicados de uma lista
removedup :: [Int] -> [Int]
removedup [] = []
removedup (x:xs)
    | pertence (x:xs) = removedup xs
    | otherwise       = x : removedup xs

--------------------------------------------------------

-- Junta a remoção de duplicados e a ordenação
purifica :: [Int] -> [Int]
purifica (x:xs) = ordenaLista (removedup (x:xs))

--------------------------------------------------------

-- Versão alternativa para verificar se um número pertence à lista
pertence2 :: Int -> [Int] -> Bool
pertence2 _ [] = False
pertence2 y (x:xs)
    | y /= x    = pertence2 y xs
    | otherwise = True

-- Outra função para remover duplicados (independente de ser ordenada ou não)
remove_dup :: [Int] -> [Int]
remove_dup [] = []
remove_dup [x] = [x]
remove_dup (x:xs)
    | pertence2 x xs = remove_dup xs
    | otherwise      = x : remove_dup xs
