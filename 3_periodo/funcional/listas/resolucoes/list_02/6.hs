{-6. Defina a função find utilizada na função positions.
positions :: Eq a => a -> [a] -> [Int]
positions x xs = find x (zip xs [0..n])
where n = (length xs) - 1-}

-- Essa questão utiliza conhecimentos da Classe EQ, como eu ainda não estudei
-- prefiro não fazer-lá por enquanto
positions :: Eq a => a -> [a] -> [Int]
positions x xs = find x (zip xs [0..n])
    where n = (length xs) - 1


