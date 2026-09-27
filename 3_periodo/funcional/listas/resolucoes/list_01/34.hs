{-34. Crie uma função que receba os coeficientes de uma equação do segundo grau ax2 + bx + c = 0
na forma (a,b,c) e retorne as raízes imaginárias, indicando um erro.
{-exemplo-}
Main> equacao (1,(-5), 6) = (2, 3)-}
------------------------------------------------------------------------------
-- Funções para acessar os dados da tripla
first :: (a, b, c) -> a
first (a, _, _) = a

second :: (a, b, c) -> b
second (_, b, _) = b

third :: (a, b, c) -> c
third (_, _, c) = c
------------------------------------------------------------------------------
-- Funções auxiliares para encontrar: Delta,Raiz1,Raiz2 da equação.
delta :: (Double, Double, Double) -> Double
delta values = (second values)^2 - 4 * first values * third values

root1 :: (Double, Double, Double) -> Double
root1 values = (-second values - sqrt (delta values)) / (2 * first values)

root2 :: (Double, Double, Double) -> Double
root2 values = (-second values + sqrt (delta values)) / (2 * first values)

------------------------------------------------------------------------------
-- Função que retorna as raízes de uma função quadratica...
bhaskara:: (Double, Double, Double) -> (Double,Double)
bhaskara values
    |delta values > 0 = (root1 values,root2 values)
    |delta values == 0 =(root1 values,root1 values)
    |delta values < 0 = error "Não tem raízes reais"