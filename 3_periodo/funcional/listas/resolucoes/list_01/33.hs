{-33. Dadas duas datas (d1 , m1 , a1 ) e (d2 , m2 , a2 ), tal que data1 ≤ data2 , construa uma função que
retorne quantos dias existem entre estas duas datas , onde di define o dia do mês mj no ano ak .-}

--------------------------------------------------------------------------------
first :: (a,b,c) -> a
first (a,_,_) = a

second :: (a,b,c) -> b
second (_,b,_) = b

third :: (a,b,c) -> c
third (_,_,c) = c
--------------------------------------------------------------------------------

yeartomonth :: (Int, Int, Int) -> (Int, Int, Int) -> Int
yeartomonth d1 d2
    | third d1 >= third d2 = (third d1 - third d2) * 12
    | otherwise            = (third d2 - third d1) * 12

monthtoday :: (Int, Int, Int) -> (Int, Int, Int) -> Int
monthtoday d1 d2
    | second d1 >= second d2 = second d1 - second d2
    | otherwise              = second d2 - second d1

daysm :: Int -> Int
daysm x = x * 30

diasEntreDatas :: (Int, Int, Int) -> (Int, Int, Int) -> Int
diasEntreDatas d1 d2 = (daysm (yeartomonth d1 d2 + monthtoday d1 d2)) + (abs (first d2 - first d1))




