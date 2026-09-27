{-18. Defina uma função charToNum::Char->Int que converte um dígito numérico do tipo Char
(como ´3´) para o valor que ele representa em Int, (3). Se o caractere de entrada não representa
um dígito numérico, a função deve retornar -1. Como dica, veja as funções isDigit, chr e ord
do módulo Data.Char.-}

import Data.Char (ord, chr)

charToNum :: Char -> Int
charToNum x
    | (x >= '0' && x <= '9') = ord x - ord '0'
    | otherwise              = (-1)
