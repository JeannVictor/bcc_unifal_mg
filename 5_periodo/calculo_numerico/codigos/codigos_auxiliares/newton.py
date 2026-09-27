import sympy as sp

# variável simbólica
x = sp.symbols('x')

# função simbólica (edite aqui quando quiser mudar a equação)
f_expr = 3*x**4 - 2*sp.exp(-x**2)

# derivada simbólica
df_expr = sp.diff(f_expr, x)

# transformar em funções numéricas
f = sp.lambdify(x, f_expr)
df = sp.lambdify(x, df_expr)


def newton_raphson(x0, eps):

    iteration = 1
    xk = x0

    while True:

        fx = f(xk)
        dfx = df(xk)

        x_next = xk - fx/dfx

        print(f"Iteration {iteration:2d} | xk={xk:.8f} | f(xk)={fx:.8f} | f'(xk)={dfx:.8f} | |xk-xk-1|={abs(x_next-xk):.8f}")
        print("-"*90)

        if abs(fx) < eps or abs(x_next - xk) < eps:
            print("\nStopping criterion satisfied.")
            print(f"Approximate root: {x_next:.8f}")
            return x_next

        xk = x_next
        iteration += 1


print("This program computes an approximate root using the Newton-Raphson Method")

x0 = float(input("Enter the initial guess (x0): "))
eps = float(input("Enter epsilon (tolerance): "))

print("\nStarting Newton-Raphson iterations...\n")

newton_raphson(x0, eps)