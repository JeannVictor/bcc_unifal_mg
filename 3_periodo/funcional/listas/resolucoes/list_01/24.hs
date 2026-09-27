{-24. Faça em Haskell uma solução para, dada uma lista de inteiros, retornar a string contendo as
letras do alfabeto cuja posição é dada pelos elementos da lista.
{-exemplo-}
Main> converte [1,2,6,1,9] = "ABFAI"
Main> converte [ ] = "". -}
import Data.Char (chr)

convert:: [Int] -> [Char]
convert [] = ""
convert (h:t) = [chr(h + 64)] ++ convert (t)

-- A função utiliza a tabela ASCII, onde:
-- - 'A' corresponde ao valor 65
-- - ...
-- - 'Z' corresponde ao 90
-- Portanto, para converter um número n (1-26) para a letra correspondente,
-- basta somar 64 ao valor de n e obter o caractere ASCII correspondente.


