import math

# Define the function f(x) = e^x - 3x
def f(x):
    return math.exp(x) - 3*x

def false_position(a, b, eps1, eps2):

    xk = (a * f(b) - b * f(a)) / (f(b) - f(a))

    iteration = 1

    while True:

        print(f"Iteration {iteration:2d} | a={a:.6f} | f(a)={f(a):.6f} | b={b:.6f} | f(b)={f(b):.6f} | xk={xk:.6f} | f(xk)={f(xk):.6f} | |b-a|={abs(b-a):.6f}")
        print("-"*100)

        # Update the interval based on the sign of f(xk)
        if f(a) * f(xk) < 0:
            b = xk
        else:
            a = xk

        # Check stopping criteria
        if abs(b - a) < eps1 or abs(f(xk)) < eps2:
            print("\nStopping criterion satisfied.")
            print(f"Approximate root: {xk:.6f}")
            return xk

        # Calculate new xk
        xk = (a * f(b) - b * f(a)) / (f(b) - f(a))

        iteration += 1


print("This program computes an approximate root using the False Position Method")

a = float(input("Enter the lower bound of the interval: "))
b = float(input("Enter the upper bound of the interval: "))

eps1 = float(input("Enter epsilon1 (interval tolerance): "))
eps2 = float(input("Enter epsilon2 (function tolerance): "))

# Verify if the interval satisfies Bolzano's Theorem
if f(a) * f(b) < 0:
    print("The interval satisfies Bolzano's Theorem. The False Position Method can proceed.")
    false_position(a, b, eps1, eps2)
else:
    print("The interval does not satisfy Bolzano's Theorem (no sign change). A root is not guaranteed in this interval.")