-- Provas de 2025/1 de Programação Funcional

{-1. (20 pt) Faça, em Haskell, uma solução que receba um Int a e uma [Int] b. Como saída,
teremos um Bool que informa se a ∈ b.-}

-- Versão com guardas
f_in1:: Int -> [Int] -> Bool
f_in1 _ [] = False
f_in1 a (x:xs) 
    | a == x = True
    | otherwise = f_in1 a xs

-- Versão com Casamento de Padrão.
-- Obs: Essa era a versão que o Eliseu não tirava ponto
f_in2 :: Int -> [Int] -> Bool
f_in2 _ [] = False
f_in2 a (x:_) | a == x    = True
f_in2 a (_:xs)            = f_in2 a xs

---------------------------------------------------------------------------------------------------
{-2.(20 pt) Considerando f _in, faça, em Haskell, uma solução que receba um Int x e uma [[Int]] l.
Como saída, teremos uma [(Bool, [Int])] s que informa, para cada sublista li de l, se o elemento
x pertence ou não à li.
f2::Int->[[Int]]->[(Bool,[Int])]-}

f2::Int->[[Int]]->[(Bool,[Int])]
f2 _ [] = []
f2 x (y:ys) = (f_in2 x y,y): f2 x ys

---------------------------------------------------------------------------------------------------
{-3. (20 pt) Considerando f 2, faça, em Haskell, uma solução que receba um Int x e uma [[Int]] l.
Como saída, teremos uma (Int, [(Bool, [Int])]) s que informa o Int x e, para cada sublista li
de l, se o elemento x pertence ou não à li.-}

f3::Int->[[Int]]->(Int,[(Bool,[Int])])
f3 x y = (x ,f2 x y)

---------------------------------------------------------------------------------------------------
{-4. (20 pt) Faça, em Haskell, uma solução que receba uma (Int,[(Bool,[Int])]) e gere uma [[Int]]
com apenas as listas [Int] cujo Bool da dupla é False.-}

f4::(Int,[(Bool,[Int])])->[[Int]]
f4 (_,[]) = []
f4 (y,(x:xs))
    | not(fst x) = snd x : f4 (y,xs)
    | otherwise  =         f4 (y,xs)

---------------------------------------------------------------------------------------------------
{-5. (15 pt) Faça, em Haskell, uma solução que receba duas strings S e R, cuja menor tem tamanho
n. Sua solução deverá retornar uma lista de Bool B de tamanho n, de modo que cada Bi será
a informação se Si é igual ou diferente de Ri, para 0 ≤ i < n.-}

-- Versão com Guardas 
f5_1::String->String->[Bool]
f5_1 _ [] = []
f5_1 [] _ = []
f5_1 (x:xs) (y:ys) 
    | x == y = True: f5_1 xs ys
    | otherwise = False : f5_1 xs ys

-- Versão apenas com casamento de padrão. (Estilo que Eliseu gosta)
f5_2::String->String->[Bool]
f5_2 _ [] = []
f5_2 [] _ = []
f5_2 (x:xs) (y:ys) = (x == y) : f5_2 xs ys

-- Versão com List Comprehension
f5_3:: String -> String -> [Bool]
f5_3 xs ys = [x == y | (x,y) <- zip xs ys]
