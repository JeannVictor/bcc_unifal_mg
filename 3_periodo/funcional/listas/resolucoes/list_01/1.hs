{-
  1. Declare, em Haskell, a função abaixo, incluindo o protótipo (cabeçalho):

  (a) f1 : R → R, definida por:

         f1(x) = (x + 4) / (x + 2), se x ≥ 0
         f1(x) = x^2 / 2, se x < 0
-}

f1 :: Float -> Float 
f1 x
    |x >= 0 = (x + 4)/(x + 2) -- Se 'x' é >= ....
    |otherwise =  (x*x)/2 -- Senão ...

{-
    (b) f2 : R² → R, definida por:

         f2(x, y) = x + y, se x ≥ y
                    x - y, se x < y
-}

f2 :: Int -> Int -> Int
f2 x y
    |x >= y = (x + y) -- Se 'x' >= 'y' -> (x+y)
    |otherwise = (x - y) -- Senão (x-y)

{-
(c) f3 : R³ → R, definida por:

         f3(x, y, z) = x + y + z, se (x + y) > z
                        x - y - z, se (x + y) < z
                        0, se (x + y) = z
-}

f3 :: Int -> Int -> Int -> Int
f3 x y z
    |(x + y) > z = x + y + z -- Se (x + y) > z ...
    |(x + y) < z = x - y - z -- Se (x - y) < z ...
    |otherwise = 0 -- Se (x + y) = z, 0

