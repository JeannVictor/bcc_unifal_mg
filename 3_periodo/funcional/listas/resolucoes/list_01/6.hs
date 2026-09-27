-- 6. Considere a sequência: a_0 = sqrt(6) a_1 = sqrt(6 + sqrt(6)) ... a_n = sqrt(6 + a_(n-1)) com tendência ao +∞. 
-- Faça, em Haskell,uma função para calcular o i−ésimo termo desta sequência, considerando i0 = 6^1/2.

expressao :: Double -> Double
expressao 1 = sqrt (6)
expressao x = sqrt (6 + expressao(x-1))
