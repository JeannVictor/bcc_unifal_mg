--36. Apresentada a base de dados de 10 professores:
base :: Int -> (Int, String, String, Char)
base x
  | x == 0  = (1793, "Pedro Paulo", "MESTRE", 'M')
  | x == 1  = (1797, "Joana Silva Alencar", "MESTRE", 'M')
  | x == 2  = (1534, "João de Medeiros", "DOUTOR", 'F')
  | x == 3  = (1267, "Cláudio César de Sá", "DOUTOR", 'M')
  | x == 4  = (1737, "Paula de Medeiros", "MESTRE", 'F')
  | x == 5  = (1888, "Rita de Matos", "MESTRE", 'F')
  | x == 6  = (1442, "Carlos Henrique", "DOUTOR", 'M')
  | x == 7  = (1655, "Mariana Lima", "MESTRE", 'F')
  | x == 8  = (1589, "Luiz Fernando", "DOUTOR", 'M')
  | x == 9  = (1698, "Tereza Cristina Andrade", "MESTRE", 'F')
  | x == 10 = (1064, "Joaquim Batista Neto", "DOUTOR", 'M')
  | otherwise = (0, "", "", '0')
  
-- Construa funções que retornem:
-- (a) O número de doutores na base.
qtdDoutor:: Int -> Int
qtdDoutor (-1) = 0
qtdDoutor x 
    | (third36 (base x) == "DOUTOR") = 1 + qtdDoutor (x - 1)
    | otherwise                    = qtdDoutor (x - 1) 

--(b) O número de mulheres.
qtdWoman:: Int -> Int
qtdWoman (-1) = 0
qtdWoman x 
    | (fourth36 (base x) == 'F') = 1 + qtdWoman (x - 1)
    | otherwise                  = qtdWoman (x - 1) 

--(c) O número de mestres do sexo masculino.
qtdMasterMan:: Int -> Int
qtdMasterMan (-1) = 0
qtdMasterMan x 
    | (fourth36 (base x) == 'M') && (third36 (base x) == "MESTRE") = 1 + qtdMasterMan (x - 1)
    | otherwise                                                    = qtdMasterMan (x - 1) 

--(d) O nome do professor mais antigo (número de menor matrícula)
oldProf:: Int -> Int -> String -> String
oldProf (-1) _ name = name
oldProf x ra name
    | first36 (base x) < ra = oldProf (x-1) (first36 (base x)) (second36(base x))
    | otherwise             = oldProf (x-1) (ra) (name)

------------------------------------------------------------------------------
-- Funções para acessar os dados da tripla
first36 :: (a, b, c,d) -> a
first36 (a, _, _,_) = a

second36 :: (a, b, c,d) -> b
second36 (_, b, _,_) = b

third36 :: (a, b, c,d) -> c
third36 (_, _, c,_) = c

fourth36 :: (a, b, c,d) -> d
fourth36 (_, _, _,d) = d