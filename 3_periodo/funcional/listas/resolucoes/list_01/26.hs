{-26. Faça em Haskell uma solução para o seguinte problema: Dada uma lista de caracteres [Char],
e um caractere a, retornar quantos caracteres da lista são iguais a a.
{-exemplo-}
Main> conta "ABCAABCDDA" "B" = 2-}

conta:: [Char] -> Char -> Int
conta [] _ = 0
conta (x:xs) y 
    | x == y    = 1 + conta xs y
    | otherwise = conta xs y