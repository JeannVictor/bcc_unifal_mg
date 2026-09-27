{-20. Implemente a função pushRight::String->Int->String que recebe uma string s e um número
inteiro n e retorna uma nova string t com k caracteres ’>’ inseridos no início de s. O valor de
k deve ser tal que o comprimento de t seja igual a n. Obs: se n é menor que o comprimento
de s, a função retorna a própria string s.
{-exemplo-}
Main> pushRight "abc" 5 = ">>abc"-}

tam:: String -> Int
tam "" = 0
tam (a:b) = 1 + tam b

pushRight:: String -> Int -> String
pushRight "" _ = ""
pushRight (head:tail) n
    | n <= tam (head:tail) = (head:tail)
    | otherwise            = ">" ++ pushRight(head:tail) (n-1)