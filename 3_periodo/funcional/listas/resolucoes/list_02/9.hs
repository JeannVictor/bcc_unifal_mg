{-9. Mostre como a seguinte list comprehension [f x | x <- xs, p x] pode ser reescrita utilizando
funções de alta-ordem como map e filter. Tente entender e aplicar o seguinte exemplo:
Main> [(+7) x | x <- [1..10], odd x].-}

-- Versão em List Comprehension
[f x | x <- xs, p x] 
-- Versão em Funções de Alta Ordem
map f (filter p xs) 
-- Chamada para função de Alta Ordem
map (+7)(filter odd [1,2,3,4,5,6,7,8,9,10]) 

