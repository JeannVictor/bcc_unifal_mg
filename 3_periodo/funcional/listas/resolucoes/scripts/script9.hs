import Data.Char

{- 01 qual é o resultado da computação desta implementação? -}

f1 :: [(Int,Char)]   
f1 = [ (a,b) | a <-[1..26], b<-['a'..'z']]
-- O resultado é uma lista com tuplas de (1,'a'),(1,'b')...(26,'z')
----------------------------------------------------------------------------------
{- 02 Considere uma tupla (x, y) que aparece na lista gerada por f1. 
Faça uma função que remova toda ocorrência subsequentes de tuplas (x, _), mantendo apenas a primeira 
exemplo: f2 [(1,'a'),(1,'b'),(1,'c'),(2,'d'),(2,'e'),(2,'f'),(2,'g')] retorna [(1,'a'),(2,'d')] 
Observação: você não deve considerar o Char da tupla em sua computação-}
-- Apenas Funciona para Listas Ordenadas
-- Entretanto o custo de apenas ordenar provavelmente é menor que fazer 
-- de alguma maneira que não precise de ordem.
f2:: [(Int,Char)] -> [(Int,Char)]
f2 [] = []
f2 [a] = [a]
f2 ((x1,c1):(x2,c2):xs) 
    | x1 /= x2  = (x1,c1) : f2 ((x2,c2):xs)
    | otherwise = f2 ((x1,c1):xs) 

{- 03 Desafio: considere as repetições das tuplas (x,_) geradas por f1. Então, faça um filtro parecido com f2,
contudo, para o primeiro Int, a primeira tupla com a ocorrência será mantida na solução. 
Por conseguinte, para o segundo Int, a segunda tupla será mantida, e assim por diante. Vejam o exemplo:
f3 [(1,'a'),(1,'b'),(1,'c'),(1,'d'),(2,'a'),(2,'b'),(2,'c'),(2,'d'),(3,'a'),(3,'b'),(3,'c'),(3,'d'),(4,'a'),(4,'b'),(4,'c'),(4,'d')] 
retorna [(1,'a'),(2,'b'),(3,'c'),(4,'d')]
Observação: você não deve considerar o Char da tupla em sua computação -}

f3:: [(Int,Char)] -> [(Int,Char)]
f3 [] = []
f3 ((x,y):xs) = f3_aux ((x,y):xs) 1 1

f3_aux :: [(Int,Char)] -> Int -> Int -> [(Int,Char)]
f3_aux [] _ _ = []
f3_aux ((a,b):xs) pos obj
    | a == obj && pos == obj = (a,b) : f3_aux xs 1 (obj+1)
    | a == obj = f3_aux xs (pos+1) obj
    | a > obj = f3_aux ((a,b):xs) 1 (obj+1)  
    | otherwise = f3_aux xs pos obj       


{- 04 Considere a função f4Fold como definida a seguir -}

f4Fold::(t->u->u)->[t]->u->u
f4Fold _ [] z    = z
f4Fold f (a:b) z = f a (f4Fold f b z)
 
{- implemente um exemplo de computação em que t diferente de u para a computação de f4Fold -}

{- sugestão Eliseu -}
temPar::Int->Bool->Bool
temPar x b = (mod x 2 == 0) || b

todosPar::Int->Bool->Bool
todosPar x b = (mod x 2 == 0) && b
 
generalizaPar:: (Bool->Bool->Bool)->Int->Bool->Bool
generalizaPar f x b = f (mod x 2 == 0) b

{- solução do Davi -}
f_d :: Char->Char->Bool->Bool
f_d     c1 c2 b = c1 == c2 || b

f_p :: [Char] -> Char -> Bool
f_p      l  c = f4Fold (f_d c) l False