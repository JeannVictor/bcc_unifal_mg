import math

# NOTE: Modify the function definition here whenever you want to solve a different equation
# Define the function f(x)
def funcao(x):
    return x**3 -x -2

# Compute the theoretical maximum number of iterations for the bisection method
def cond_parada(ia,ib,erro):
    return math.ceil(math.log2((ib - ia)/erro)- 1)

def bissecao(ia,ib,erro):
    pm = (ia + ib)/2
    sinal_a = math.copysign(1,funcao(ia))
    sinal_b = math.copysign(1,funcao(ib))
    interacao = 1
    parada = cond_parada(ia,ib,erro)

    while (parada > 0):
        print(f"Iteration {interacao:2d} | A={ia:.6f} | B={ib:.6f} | Midpoint={pm:.6f} | f(Midpoint)={funcao(pm):.6f}")
        print("-"* 100)

        if(sinal_a == math.copysign(1,funcao(pm))):
            ia = pm
        elif(sinal_b == math.copysign(1,funcao(pm))):
            ib = pm

        # Update midpoint, iteration counter, and stopping condition
        pm = (ia + ib)/2
        interacao += 1
        parada = parada - 1

print("This program computes an approximate root using the Bisection Method")
ia = float(input("Enter the lower bound of the interval: "))
ib = float(input("Enter the upper bound of the interval: "))
erro = float(input("Enter the desired precision (e.g. 0.0001): "))

# Verify if the interval satisfies Bolzano's Theorem
# A root is guaranteed in the interval if f(a) * f(b) < 0 (sign change)
if (funcao(ia) * funcao(ib)) < 0:
    print("The interval satisfies Bolzano's Theorem. The Bisection Method can proceed.")
    bissecao(ia,ib,erro)
else:
    print("The interval does not satisfy Bolzano's Theorem (no sign change). A root is not guaranteed in this interval.")