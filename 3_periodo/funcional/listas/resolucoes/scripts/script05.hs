import Data.Char

{- 
  Faça a função f1 que receba uma String S e retorne uma String R.
  R deve ser igual a S, com exceção de que todo caracter alfanumérico x encontrado em S
  que esteja seguido de um caracter y não alfanumérico determinará que y será repetido x vezes em R.

  Exemplo: f1 "ab42c570sd3f" retorna "ab42cc570d3fff"
-}

--------------------------------------------------------------------------------

repete :: Char -> Int -> String
repete _ 0 = []
repete c x = c : repete c (x-1)

charToInt :: Char -> Int
charToInt c = ord c - ord '0'

f1 :: [Char] -> [Char]
f1 [] = []
f1 (a:[]) = [a]
f1 (a:b:xs)
  | isDigit a && not (isDigit b) = a : repete b (charToInt a) ++ f1 xs
  | otherwise                    = a : f1 (b:xs)

--------------------------------------------------------------------------------

{- 
  Não faz parte desta questão: transforma string em número
-}

strToInt :: String -> Int
strToInt [] = 0
strToInt (a:x) = charToInt a + (strToInt x) * 10

--------------------------------------------------------------------------------

{- 
  Faça f11, outra versão de f1, que retorne R do tipo [(Char, Bool, Int)] 
  De modo que, para cada caractere de S, informe se ele será repetido ou não
  e a quantidade de vezes.

  Exemplo: f11 "ab42c570sd3f" retorna 
  [('a',False,1),('b',False,1),('4',False,1),('2',False,1),
   ('c',True,2),('5',False,1),('7',False,1),('0',False,1),
   ('s',True,0),('d',False,1),('3',False,1),('f',True,3)]
-}

f11 :: String -> [(Char, Bool, Int)]
f11 [] = []
f11 (a:[]) = [(a, False, 1)]
f11 (a:b:xs)
  | isDigit a && not (isDigit b) = (a, False, 1) : (b, True, charToInt a) : f11 xs
  | otherwise                    = (a, False, 1) : f11 (b:xs)

--------------------------------------------------------------------------------

{- 
  Agora, implemente a função f111 que receba [(Char, Bool, Int)] 
  e gere uma String com os caracteres repetidos ou não (como R em f1).
  Use o Bool da tripla.
-}

fst1 :: (a, b, c) -> a
fst1 (a, _, _) = a

snd1 :: (a, b, c) -> b
snd1 (_, b, _) = b

thd1 :: (a, b, c) -> c
thd1 (_, _, c) = c

f111 :: [(Char, Bool, Int)] -> String
f111 [] = []
f111 (x:xs) 
  | snd1 x == False = fst1 x : f111 xs
  | otherwise       = repete (fst1 x) (thd1 x) ++ f111 xs

--------------------------------------------------------------------------------

{- 
  Faça a função f2 que receba uma lista de Strings 
  e aplique a todas as strings a computação da função f1.
-}

f2 :: [String] -> [String]
f2 [] = []
f2 (x:xs) = f1 x : f2 xs

--------------------------------------------------------------------------------

{- 
  Faça a função f3 que receba uma String S e retorne uma dupla de Bool e String.
  A string de saída deve ter o caracter da ordem alfabética das letras minúsculas
  por substituição a cada caracter numérico (1..9) que aparece em S.
  O Bool deve informar se a entrada foi ou não alterada.

  Exemplo: f3 "a2c4x" retorna ("abcdx", True)
-}

intToAlfa :: Char -> Char
intToAlfa x = chr (ord x + 48)

change :: String -> String
change [] = []
change (x:xs)
  | x >= '1' && x <= '9' = intToAlfa x : change xs
  | otherwise            = x : change xs

compara :: String -> String -> Bool
compara [] [] = False
compara (x:xs) (y:ys)
  | x /= y    = True
  | otherwise = compara xs ys

f3 :: String -> (String, Bool)
f3 [] = ([], False)
f3 x  = (change x, compara x (change x))




