import Data.Char

--faça f1 capaz de somar uma lista de inteiros se um Char for alfanumérico, 
--ou multiplicar os elementos, caso contrário 


'a' [1,2,3,4] == 10  '! ' [1,2,3,4] = 24
-- Minha implementação
f1:: Char -> [Int] -> Int
f1 x y 
    | isAlpha x || isDigit x = sum y
    | otherwise = multiplicar y

multiplicar:: [Int] -> Int
multiplicar [] = 1
multiplicar (x:xs) = x * multiplicar xs

-- Implementação do Eliseu
f1_E::Char->[Int]->Int
f1_E c x
  |isDigit (c)     && x==[]    = 0
  |not (isDigit c) && x==[]    = 1
  |isDigit c                   = a + f1_E c b
  |otherwise                   = a * f1_E c b
    where (a:b) = x
----------------------------------------------------------------------------------
{- reescreva f1 usando casamento de padrão -}

f2::Char->[Int]->Int
f2 c x   = f2_aux (isAlpha x || isDigit x) x

f2_aux::Bool->[Int]->Int
f2_aux True   []   = 0
f2_aux False  []   = 1
f2_aux True  (a:b) = a + f2_aux True b
f2_aux False (a:b) = a * f2_aux False b
----------------------------------------------------------------------------------
-- reescreva f2 fazendo chamadas de funções para somar ou multiplicar 

f3::Char->[Int]-> Int
f3 c x = f3_aux (isDigit c || isAlpha c) x

f3_aux:: Bool->[Int]->Int
f3_aux True  x = somaL x
f3_aux False x = multL x

somaL []    = 0
somaL (a:b) = a + somaL b

multL []    = 1
multL (a:b) = a * multL b
----------------------------------------------------------------------------------
{- Reescreva f3 usando função de alta ordem
   Esta função é didática, pois mostra o uso de função de alta ordem
   Contudo, o booleano não seria necessário se conseguíssemos fazer casamento 
   de padrão com a função parâmetro-}

-- Versão com Casamento de Padrão 
f4_ :: Char -> (Int -> Int -> Int) -> [Int] -> Int
f4_ c _ xs = f4_aux (isDigit c || isAlpha c) xs

f4_aux True  []     = 0
f4_aux True  (x:xs) = x + f4_aux True xs
f4_aux False []     = 1
f4_aux False (x:xs) = x * f4_aux False xs

-- Versão com Foldr
f4_f :: Char -> (Int -> Int -> Int) -> [Int] -> Int
f4_f c _ xs = f4_faux (isDigit c || isAlpha c) xs

f4_faux :: Bool -> [Int] -> Int
f4_faux True  xs = foldr (+) 0 xs
f4_faux False xs = foldr (*) 1 xs

-- Implementação para lista de pelo menos um elemento 
f4::(Int->Int->Int)->[Int]->Int
f4 op [a] = a
f4 op (a:x) = (op) a (f4 op x) 
----------------------------------------------------------------------------------
{- soma ou subtrai elementos de lista com função de alta ordem -}

sumLsubL :: (Int->Int->Int) -> [Int] -> Int
sumLsubL op [] = 0
sumLsubL op (a:x) = (op) a (sumLsubL op x)

----------------------------------------------------------------------------------
{- função que converte caixa baixa para caixa  alta
   usar a função map para aplicar a uma String -}
   
intervalo = ord ('a') - ord ('A')
caixaBaixaAlta c = chr (ord c - intervalo)

func:: (Char -> Char) -> String -> String
func f [] = []
func f (x:xs) = f x : func f xs 

