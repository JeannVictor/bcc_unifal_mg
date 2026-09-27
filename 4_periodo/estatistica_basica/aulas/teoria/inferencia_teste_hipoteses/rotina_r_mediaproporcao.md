#==========================================================
# USANDO  A Função t.test() para MEDIA populacional
#  Realiza o teste t-Student para uma ou duas amostras.
#==========================================================

# Exemplo secao 8.3.1

amostra=c(6, 7, 7, 3, 4, 5, 4 , 2)
mu0=5
t.test(amostra,mu=mu0,alternative="greater")

# usar alternative="greater", quando H1 tiver sinal de maior (>)
# usar alternative="less", quando H1 tiver sinal de menor (<) 
# usar alternative="two.side", quando H1 tiver sinal de diferente (!=)

#===============================================================================
#               Teste a PROPORÇÃO (PI) de uma população
#                Fazendo o teste MANUALMENTE 
#               USANDO A FUNCAO binom.test - Teste EXATO para PROPORCAO (PI)                            
#================================================================================
# Cuidado: entrada com número de sucessos (ns) e tamanho da amostra (n)

# Exemplo secao 8.4.1

n=200
ns=188 #numero de sucessos
p0= 0.90   ##Valor a ser testado (assumido) para Pi#

binom.test(ns, n, p = p0,alternative="greater")

# usar alternative="greater", quando H1 tiver sinal de maior (>)
# usar alternative="less", quando H1 tiver sinal de menor (<) 
# usar alternative="two.side", quando H1 tiver sinal de diferente (!=)

#=====================================================================
