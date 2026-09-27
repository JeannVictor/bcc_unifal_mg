{-19. Implemente a função duplicate::String ->Int->String que recebe uma string s e um número
inteiro n. A função deve retornar a concatenação de n cópias de s. Se n for zero, retorna .
Como dica, usar o operador de concatenação pré-definido (++)::String->String->String.-}

duplicate:: String -> Int -> String
duplicate _ 0 = ""
duplicate x y = x ++ duplicate x (y-1)