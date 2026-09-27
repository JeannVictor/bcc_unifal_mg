{-19. Questão 24 - Lista 1 (Nova proposta): Faça em Haskell uma solução para, dada uma lista de
inteiros, retornar a string contendo as letras do alfabeto cuja posição é dada pelos elementos
da lista. Utilize list comprehension e, caso necessário, funções de alta ordem.
{-exemplos-}
Main> converte [1,2,6,1,9] = "ABFAI"
Main> converte [ ] = "".-}
import Data.Char (chr)

-- Versão Normal
converte1 :: [Int] -> String
converte1 [] = ""
converte1 (x:xs) = chr(x + 64) : converte1 (xs)

-- Versão com List Comprehension
converte2 :: [Int] -> String
converte2 xs = [chr(x + 64)| x <- xs]

-- Versão com Funções de Alta Ordem
converte3 :: [Int] -> String
converte3 xs = map (\x -> chr(x + 64)) xs
-- A função Map basciamente aplica alguma operação a todo elemento de uma lista,
-- logo eu apliquei a todo x  de xs,a operação chr(x + 64).
-- converte3 [1,2,6,1,9] = "ABFAI"