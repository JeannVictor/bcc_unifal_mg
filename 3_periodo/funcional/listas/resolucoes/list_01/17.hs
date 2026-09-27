{-17. Implemente uma função que converte uma letra minúsculas como entrada para seu equivalente
em maiúsculo. Caso a entrada não seja uma letra minúscula, retorne o próprio caractere
de entrada. Como dica, veja a função predefinida isLower::Char->Bool. Para verificar outras
funções pré-definidas para o tipo Char, consulte a biblioteca padrão no endereço http://zvon.
org/other/haskell/Outputglobal/index.html-}
import Data.Char (ord, chr)

isLowerMy:: Char -> Bool
isLowerMy crc
    | crc >= 'a' && crc <= 'z' = True
    | otherwise = False -- Desnecessario

lowerToUpper:: Char -> Char
lowerToUpper crc
    | (isLowerMy crc == True) = chr(ord crc - 32)
    | otherwise           = crc 