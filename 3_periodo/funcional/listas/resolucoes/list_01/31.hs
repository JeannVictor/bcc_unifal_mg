-- 31. Seja o cadastro de pessoas dado pela função a seguir:
-- Construa funções que retornem os seguintes dados:

pessoa :: Int -> (String, Int, Char)
pessoa rg
    | rg == 1 = ("João Silva", 22, 'm')
    | rg == 2 = ("Maria Oliveira", 30, 'f')
    | rg == 3 = ("Carlos Souza", 19, 'm')
    | rg == 4 = ("Ana Paula", 25, 'f')
    | rg == 5 = ("Pedro Martins", 33, 'm')
    | rg == 6 = ("Juliana Rocha", 27, 'f')
    | rg == 7 = ("Lucas Ferreira", 21, 'm')
    | rg == 8 = ("Fernanda Lima", 29, 'f')
    | rg == 9 = ("Rafael Duarte", 24, 'm')
    | rg == 10 = ("Camila Ribeiro", 26, 'f')
    | rg == 11 = ("Marcelo Nunes", 31, 'm')
    | rg == 12 = ("Bianca Melo", 20, 'f')
    | rg == 13 = ("André Costa", 28, 'm')
    | rg == 14 = ("Patrícia Pires", 23, 'f')
    | rg == 15 = ("Bruno Cardoso", 34, 'm')
    | rg == 16 = ("Natália Sales", 22, 'f')
    | rg == 17 = ("Thiago Rocha", 27, 'm')
    | rg == 18 = ("Larissa Alves", 25, 'f')
    | rg == 19 = ("Eduardo Pinto", 32, 'm')
    | rg == 20 = ("Gabriela Teixeira", 21, 'f')
    | rg == 21 = ("Diego Castro", 26, 'm')
    | rg == 22 = ("Vanessa Lopes", 28, 'f')
    | rg == 23 = ("Rodrigo Moura", 29, 'm')
    | rg == 24 = ("Isabela Martins", 24, 'f')
    | rg == 25 = ("Henrique Vieira", 30, 'm')
    | rg == 26 = ("Tainá Costa", 23, 'f')
    | rg == 27 = ("Leandro Silva", 27, 'm')
    | rg == 28 = ("Juliane Torres", 26, 'f')
    | rg == 29 = ("Vinícius Almeida", 22, 'm')
    | rg == 30 = ("Débora Carvalho", 25, 'f')
    | rg == 31 = ("Gustavo Moreira", 31, 'm')
    | rg == 32 = ("Sabrina Gonçalves", 29, 'f')
    | rg == 33 = ("Fábio Rezende", 24, 'm')
    | rg == 34 = ("Aline Fernandes", 28, 'f')
    | rg == 35 = ("César Prado", 26, 'm')
    | rg == 36 = ("Tatiane Lopes", 30, 'f')
    | rg == 37 = ("Rogério Silva", 33, 'm')
    | rg == 38 = ("Elaine Duarte", 27, 'f')
    | rg == 39 = ("Otávio Ramos", 22, 'm')
    | rg == 40 = ("Renata Souza", 24, 'f')
    | rg == 41 = ("Danilo Peixoto", 29, 'm')
    | rg == 42 = ("Amanda Ferreira", 23, 'f')
    | rg == 43 = ("Igor Barros", 25, 'm')
    | rg == 44 = ("Jéssica Lima", 28, 'f')
    | rg == 45 = ("Alex Costa", 21, 'm')
    | rg == 46 = ("Luciana Braga", 30, 'f')
    | rg == 47 = ("Fernando Tavares", 26, 'm')
    | rg == 48 = ("Priscila Gomes", 27, 'f')
    | rg == 49 = ("Cauê Almeida", 23, 'm')
    | rg == 50 = ("Jocileide Strauss", 21, 'f')
    | otherwise = ("Não há ninguém mais", 9999, 'x')

-- Funções auxiliares para acessar os elementos da tupla (Nome, Idade, Sexo)
first :: (a,b,c) -> a
first (a,_,_) = a

second :: (a,b,c) -> b
second (_,b,_) = b

third :: (a,b,c) -> c
third (_,_,c) = c

-----------------------------------------------------
-- (a) Nome da pessoa com a menor idade até certo RG
-- Parâmetros:
-- 1º: Último RG a considerar
-- 2º: Idade mínima inicial (ex: 200)
-- 3º: Nome inicial qualquer
-----------------------------------------------------
younger:: Int -> Int -> String -> String
younger 0 _ name = name
younger rg min name
    | second (pessoa rg) < min = younger (rg -1) (second(pessoa rg)) (first(pessoa rg))
    | otherwise                = younger (rg -1) (min) (name)
-----------------------------------------------------
-- (b) Idade média das pessoas até certo RG
-- Função auxiliar que soma as idades
-----------------------------------------------------
somaAge:: Int->Int
somaAge 0 = 0
somaAge age = second(pessoa age) + somaAge(age -1)

mediaP:: Int -> Int
mediaP x = (somaAge x) `div` x
-----------------------------------------------------
-- (c) Quantidade de pessoas do sexo masculino até certo RG
-----------------------------------------------------
qtdMan:: Int -> Int
qtdMan 0 = 0
qtdMan xx
    | third (pessoa xx) == 'm' = 1 + qtdMan(xx-1)
    | otherwise =  qtdMan(xx-1)
-----------------------------------------------------
-- (d) RG da pessoa com a maior idade até certo RG
-- Parâmetros:
-- 1º: Último RG a considerar
-- 2º: Idade máxima inicial (ex: 0)
-- 3º: RG inicial (ex: mesmo valor do 1º parâmetro)
-----------------------------------------------------
older:: Int -> Int -> Int -> Int
older 0 _ rg2 = rg2
older rg max rg2
    | second (pessoa rg) > max = older (rg -1) (second(pessoa rg)) (rg)
    | otherwise                = older (rg -1) (max) (rg2)



