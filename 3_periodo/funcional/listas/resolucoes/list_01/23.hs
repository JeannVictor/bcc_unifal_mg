{-23. Faça em Haskell uma solução para, dada uma lista de inteiros, retornar uma dupla de listas de
inteiros onde a primeira conterá os elementos ímpares e a segunda os elementos pares passados
como parâmetro.
{-exemplo-}
Main> separa [1,4,3,4,6,7,9,10] = ([1,3,7,9],[4,4,6,10])-}

par:: [Int] -> [Int]
par [] = []
par (head:tail)
    | (mod head 2 == 0) = [head] ++ par tail  
    | otherwise         = par tail

impar:: [Int] -> [Int]
impar [] = []
impar (head:tail)
    | (mod head 2 /= 0) = [head] ++ impar tail  
    | otherwise         = impar tail

separa:: [Int] -> ([Int],[Int])
separa (head:tail) = (impar (head:tail),par (head:tail))

{-Não creio que seja a melhor versão desse algoritmo,haja vista que é necessario
  rodar 2 vezes a mesma lista para separar  os impares dos pares-}