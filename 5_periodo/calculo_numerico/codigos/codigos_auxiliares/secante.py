import math

# NOTE: Modify the function definition here whenever you want to solve a different equation
# Define the function f(x)
def f(x):
    return x**3 - x -2

def secante(a, b, eps1):

    xk = (b - (f(b) * (b - a)) / (f(b) - f(a)))

    iteration = 1

    while True:

        print(f"Iteration {iteration:2d} | xk={xk:.8f} | f(xk)={f(xk):.8f} | |xk - xk-1|={abs(b-a):.8f}")
        print("-"*80)

        if abs(f(xk)) < eps1 or abs(xk - b) < eps1:
            print("\nStopping criterion satisfied.")
            print(f"Approximate root: {xk:.8f}")
            return xk
        
        a = b
        b = xk
        xk = (b - (f(b) * (b - a)) / (f(b) - f(a)))

        iteration += 1


print("This program computes an approximate root using the Secant Method")

a = float(input("Enter the first initial approximation (x0): "))
b = float(input("Enter the second initial approximation (x1): "))

eps1 = float(input("Enter epsilon (tolerance): "))

print("Starting Secant Method iterations...\n")

secante(a, b, eps1)