--14. Para o exemplo da função sales::Int->Int dada em sala de aula faça o que se pede:
vendas :: Int -> Int
vendas 0 = 0
vendas 1 = 41
vendas 2 = 72
vendas 3 = 48
vendas 4 = 0
vendas 5 = 91
vendas 6 = 55
vendas 7 = 30

{-(a) Implemente a função howManyLess que calcule quantos dias as vendas foram inferiores
a um dado valor, dentro de um intervalo de dias dentro do período total. O primeiro
parâmetro de howManyLess indica o valor mínimo de vendas, o segundo parâmetro indica
o dia do início do intervalo e o terceiro parâmetro é o dia do fim do intervalo desejado
dentro do período total de dias da função;-}
--parameters: value; interval beginning; interval ending; return value
howManyLess::Int->Int->Int->Int
howManyLess min inicio fim
    | inicio > fim         = 0 
    | vendas inicio >= min = 1 + howManyLess min (inicio + 1) fim
    | otherwise            =  howManyLess min (inicio + 1) fim

{-(b) Implemente a função noZeroInPeriod::Int->Bool que retorna True somente se não há
nenhum dia no período em que o número de vendas da função sales foi zero.-}
noZeroInPeriod::Int->Bool
noZeroInPeriod (-1) = True
noZeroInPeriod x 
    | vendas x == 0 = False
    | otherwise     = noZeroInPeriod (x-1)

{-(c) Implemente a função zerosInPeriod::[Int] que retorne a lista de todos os dias em que as
vendas foram de zero unidades;-}
zerosInPeriod::Int ->[Int]
zerosInPeriod (-1)  = []
zerosInPeriod x
    | vendas x == 0 = x:zerosInPeriod (x-1)
    | otherwise     = zerosInPeriod (x-1)

{-(d) Utilizando listas de inteiros, retorne os dias em que as vendas foram abaixo de um deter-
minado valor passado como parâmetro-}

listHowManyLess::Int->Int->Int->[Int]
listHowManyLess min inicio fim
    | inicio > fim         = [] 
    | vendas inicio >= min = inicio :listHowManyLess min (inicio + 1) fim
    | otherwise            = listHowManyLess min (inicio + 1) fim