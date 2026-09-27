{-29. Faça uma solução em Haskell que, dada uma lista de caracteres maiúsculos, ela retorne uma
lista com uma repetição de cada elemento de acordo com o valor de sua ordem no alfabeto.
{-exemplo-}
Main> proliferaChar [C,B,D] = "CCCBBDDDD"-}
import Data.Char (ord, chr)

whatNumber:: Char -> Int
whatNumber x = (ord x - 64)

repeat3:: Char -> Int -> String
repeat3 x 0 = []
repeat3 x y = x:repeat3 x (y-1)

proliferaChar:: [Char] -> [Char]
proliferaChar [] = []
proliferaChar (x:xs) = (repeat3 x (whatNumber x)) ++ proliferaChar xs
