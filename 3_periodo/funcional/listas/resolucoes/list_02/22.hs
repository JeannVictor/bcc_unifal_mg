{-22. Compare as seguintes implementações de uma função que verifica a existência de um elemento
na lista e responda:-}


procuraElemento :: Int -> [Int] -> Bool
procuraElemento n (x:xs) = n == x || procuraElemento n xs

procuraElemento2 :: Int -> [Int] -> Bool
procuraElemento2 n (x:xs) = procuraElemento n xs || n == x



--(a) Ambas as implementações estão corretas para o problema em questão? Se sim, qual a
--diferença existente na computação das duas funções?

--(b) Qual implementação é mais eficiente?
Basicamente, no melhor caso possivel, que é quando o primeiro elemento já satifaz
a função , a implementação da A é melhor. Haja vista, que ela logo de cara, já da o resultado

Enquanto a implementação da A irá verificar primeiro a lista para depois verificar a cabeça,
portanto na a implementação da A é mais eficiente...

