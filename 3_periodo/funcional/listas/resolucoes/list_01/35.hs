{-35. Construa uma função que, dado três valores, verifique se os mesmos podem ser os lados de
um triângulo. Se for possível formar o triângulo, retorne uma tupla-2 com o tipo do triângulo
formado (com relação às arestas) e o perímetro do mesmo.
{-exemplo-}
Main> triangulo (7,7,11) = ("Isóceles", 25)-}

------------------------------------------------------------------------------
-- Funções para acessar os dados da tripla
first :: (a, b, c) -> a
first (a, _, _) = a

second :: (a, b, c) -> b
second (_, b, _) = b

third :: (a, b, c) -> c
third (_, _, c) = c
------------------------------------------------------------------------------
-- Função para verificar se é possivel formar o triângulo
isTriangle :: (Double, Double, Double) -> Bool
isTriangle (a, b, c) = a < b + c && b < a + c && c < a + b

-- Função para verificar o tipo do triângulo
typeTr :: (Double, Double, Double) -> String
typeTr (a,b,c)
    | isTriangle (a,b,c) == False = "Nao forma triangulo"
    | isTriangle (a,b,c) == True && (a == b && a == c) = "Equilatero"
    | isTriangle (a,b,c) == True && (a == b || a == c  || b == c) = "Isosceles" 
    | isTriangle (a,b,c) == True = "Escaleno"           

-- Função que calcula o perimetro do triangulo
perimeter::(Double,Double,Double) -> Double
perimeter (a,b,c) = a + b + c

triangulo::(Double,Double,Double)->(String,Double)
triangulo tr 
    | isTriangle tr == False = error "Nao forma triangulo"
    | isTriangle tr == True = (typeTr tr,perimeter tr)