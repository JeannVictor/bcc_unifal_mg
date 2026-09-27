{-3. Considere a função em Haskell soma::Int->Int->Int que retorna a soma entre os dois parâ-
metros. Assim, faça uma função em Haskell que resulte a multiplicação de dois parâmetros
fazendo uso da função soma.-}

soma::Int -> Int -> Int
soma x 0 = 0 -- Caso Base = Multiplicação por 0 é 0.
soma x y 
    |y > 0  = x + soma x (y-1)     -- Se y > 0,a recursão é com y--
    |y < 0  = (-x) + soma x (y+1) -- Se y < 0,a recursão é com y++
    
    
