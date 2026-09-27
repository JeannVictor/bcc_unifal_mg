{-21. Questão 29 - Lista 1 (Nova proposta): Faça uma solução em Haskell que, dada uma lista de
caracteres maiúsculos, ela retorne uma lista com uma repetição de cada elemento de acordo
com o valor de sua ordem no alfabeto. Faça a solução utilizando list comprehension.
{-exemplo-}
Main> proliferaChar [C,B,D] = "CCCBBDDDD"-}
import Data.Char (chr,ord)
-- Versão Normal 
proliferaChar1:: [Char] -> [Char]
proliferaChar1 [] = []
proliferaChar1 (x:xs) = repete x (ord x - 64)

repete:: Char -> Int -> String
repete _ 0 = []
repete x y =  x : repete x (y-1)

-- Versão com List Comprehension
proliferaChar2:: [Char] -> [Char]
proliferaChar2 xs = concat[replicate (ord x - 64) x|x <- xs]
