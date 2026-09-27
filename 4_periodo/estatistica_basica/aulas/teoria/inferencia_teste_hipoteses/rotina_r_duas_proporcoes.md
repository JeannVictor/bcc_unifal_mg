################################################################################
#               Teste a comparação proporções (P11 e Pi2) de duas populações        ################################################################################

#Afirmação : pi_p - pi_m < 0


# H0: pi_p - pi_m >= 0
# H1: pi_p - pi_m < 0

#pi_p - pi_m < 0

#=============================================================================
#     Fazendo com a função prop.test (aproxima por uma Qui-quadrado)
#=============================================================================
n1=160
ns1=150 # número de sucesso na amostra da pop_1

n2=140
ns2=118 # número de sucesso na amostra da pop_2


prop.test(c(ns2,ns1),c(n2,n1),alternative="less")

#CUIDADO COM A ORDEM ns2 e ns1/ n2,n1, dever na mesma da hipótese

#===============================================================
#Pode ser feiro também com # H1: pi_m - pi_p > 0
# Então usa greater, com oredem n1 e n2

prop.test(c(ns1,ns2),c(n1,n2),alternative="greater")

## Ficar atento com H1.
# usar alternative="two.side", quando H1 tiver sinal de diferente (!=)
# usar alternative="greater", quando H1 tiver sinal de maior (>)
# usar alternative="less", quando H1 tiver sinal de menor (<) 

