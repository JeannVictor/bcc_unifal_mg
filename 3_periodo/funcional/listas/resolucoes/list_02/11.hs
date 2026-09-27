{-11. A função de alta-ordem unfold que retorna uma lista pode ser definida como:
unfold p h t x
    | p x = []
    | otherwise = h x : unfold p h t (t x)
Com a chamada da função unfold, crie uma lista das potências de 2 com limite = 2^10.-}

unfold p h t x
    | p x = []
    | otherwise = h x : unfold p h t (t x)

p:: (a -> Bool)
h:: (a -> b -> b)
t:: (a -> a)

-- x is just a variable
-- p has to be a fuction that return Bool
-- h has to be the fuction that aplies something
-- t has to be a fuction that make the a count ...
-- x is just a variable 

-- Essa questão eu tive que olhar o Chat, pois não estava entendendo direito 
pot2 = unfold (>10) (\x -> 2^x) (+1) 0




















