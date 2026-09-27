{-30. Defina uma função que retorne uma tupla-3(tripla) contendo o caractere fornecido como en-
trada, o mesmo caratere em letras minúsculo ou maiúsculas, e o seu número da tabela ASCII.
{-exemplo-}
Main> converte ’b’ = (b, B, 98)-}
import Data.Char (chr,ord)

convertUpper:: Char -> Char
convertUpper x = chr(ord x - 32)

convertLower:: Char -> Char
convertLower x = chr(ord x + 32)

convertInt:: Char -> Int
convertInt x
    | ( ord x >= 65 && ord x <= 90 ) =  ord x - 64  -- Maiuscula
    | ( ord x >= 97 && ord x <= 122 ) = ord x - 96  -- Minuscula

convert:: Char -> (Char,Char,Int)
convert x 
    | ( ord x >= 65 && ord x <= 90 )  = (convertLower x,x,ord x)
    | ( ord x >= 97 && ord x <= 122 ) = (x,convertUpper x,ord x)
