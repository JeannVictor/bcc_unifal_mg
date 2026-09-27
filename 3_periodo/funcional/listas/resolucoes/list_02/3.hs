{-3. Uma tupla (x, y, z) de número inteiros é pitagórica se x2 + y2 = z2. Utilizando list comprehen-
sion, defina a função pyths :: Int -> [(Int, Int, Int)] que, dado um limite, retorne todas as
tuplas de (x, y, z) que são pitagóricas até o limite fornecido.
--exemplo
Main> pyths 10 = [(3,4,5), (4,3,5),(6,8,10),(8,6,10)]-}
-- Versão normal
-- Vou ficar devendo k

-- Versão com List Comprehension
pyths :: Int -> [(Int,Int,Int)] 
pyths i = [(x,y,z)| x <- [1 ..i],y <- [1 ..i],z <- [1 ..i] , (x^2 + y^2 == z^2)] 