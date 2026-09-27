{-37. Para a solução dos próximos itens, sempre use uma função implementada no ítem anterior para
auxiliar nas novas implementações, se possível. Também, use sempre o underscore quando um
parâmetro não for necessário. Considere, para os itens que se seguem, as funções e tipos:-}

-- Definição dos tipos
type Acervo = [(Isbn, Titulo, Reserva, Volumes)]
type Emprestimo = [(Matricula, Isbn)]
type Isbn = Int        -- Isbn de um livro
type Volumes = Int     -- quantidade no acervo
type Titulo = String   -- título do livro
type Matricula = String -- matrícula do discente
type Reserva = Bool    -- deve permanecer na biblioteca?

-- Dados de teste para o acervo
acervo :: Acervo
acervo = [
    (1001, "Introduction to Haskell", False, 3),
    (1002, "Functional Programming Paradigms", True, 2),  -- Este é reservado (não pode ser emprestado)
    (1003, "Data Structures and Algorithms", False, 5),
    (1004, "Computer Science Fundamentals", True, 1),    -- Este é reservado
    (1005, "Programming Language Theory", False, 4),
    (1006, "Advanced Functional Programming", False, 2)
  ]

-- Dados de teste para empréstimos
emprestimo :: Emprestimo
emprestimo = [
    ("2021001", 1001),  -- Estudante 2021001 emprestou o livro 1001
    ("2021002", 1001),  -- Estudante 2021002 emprestou o livro 1001
    ("2021003", 1003),  -- Estudante 2021003 emprestou o livro 1003
    ("2021004", 1003),  -- Estudante 2021004 emprestou o livro 1003
    ("2021005", 1003),  -- Estudante 2021005 emprestou o livro 1003
    ("2021006", 1005),  -- Estudante 2021006 emprestou o livro 1005
    ("2021007", 1006)   -- Estudante 2021007 emprestou o livro 1006
  ]

{-(a) O campo Reserva, de acervo, é True quando o livro é reservado ao uso exclusivo na
biblioteca. Então, um livro só pode ser emprestado caso esse campo seja False. Sabendo
disso, faça uma solução em Haskell, chamada por func_1, que receba um Isbn e o acervo
e, em seguida, informe se o livro para tal Isbn pode ser emprestado (True) ou não (False).-}

func_1 :: Isbn -> Acervo -> Bool
func_1 _ [] = False
func_1 isbn ((isbnL,_, reserva,_):xs)
    | (isbn == isbnL) && (reserva == False) = True
    | otherwise                             = func_1 isbn xs

{-(b) Faça uma solução em Haskell chamada func_2 que receba um Isbn e informe quantos
volumes daquele livro estão emprestados.-}
func_2 :: Isbn -> Emprestimo -> Int
func_2 _ [] = 0
func_2 isbn ((_,isbnL):xs)
    | (isbn == isbnL) = 1 + func_2 isbn xs
    | otherwise       = func_2 isbn xs    

{-(c) Faça uma solução em Haskell, chamada func_3 que receba um Isbn e retorne quantos
livros há no acervo.-}
func_3 :: Isbn -> Acervo -> Int
func_3 _ [] = 0
func_3 isbn ((isbnL,_,_,volumes):xs)
    | (isbn == isbnL) = volumes + func_3 isbn xs
    | otherwise       = func_3 isbn xs

{-(d) Faça uma solução em Haskell, chamada func_4 que receba um Isbn e retorne a quantidade
de livros disponível para empréstimo. Para tanto, deve-se observar os três pontos: a)
quantos livros você tem no acervo; b) quantos estão emprestados; c) se Reserva, retorne
zero.-}
func_4 :: Isbn -> Int
func_4 isbn 
    | func_1 isbn acervo == True = (func_3 isbn acervo ) -(func_2 isbn emprestimo)
    | otherwise                  = 0

{-(e) Faça uma solução em Haskell, chamada func_5 que receba uma matrícula e um Isbn e, em
seguida, retorne a lista de empréstimo atualizada. Caso o livro não possa ser emprestado
(reservado ou sem disponibilidade), deve retornar a lista de empréstimo sem alterações.-}
func_5 :: Matricula -> Isbn -> Emprestimo
func_5 ra isbn 
    | func_4 isbn == 0 = emprestimo
    | otherwise        = (ra,isbn) : emprestimo