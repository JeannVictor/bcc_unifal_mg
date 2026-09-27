import math

def g2(x):
    """Função de iteração g2(x) = sqrt(x + 6)"""
    return math.sqrt(x + 6)

def fixed_point_iteration(x0, num_iterations, x_star):
    """Método do ponto fixo para encontrar a raiz"""
    
    print("=" * 80)
    print("n     xn           xn+1         EA = |xn+1 - 3|    ER = EA/3      |f(xn+1)|")
    print("=" * 80)
    
    xn = x0
    
    for n in range(num_iterations + 1):
        # Calcular xn+1
        xn1 = g2(xn)
        
        # Calcular erros
        EA = abs(xn1 - x_star)
        ER = EA / x_star
        
        # Calcular f(xn+1) para verificar o erro da função
        f_value = abs(xn1**2 - xn1 - 6)  # f(x) = x² - x - 6 = 0
        
        # Exibir resultados formatados com 4 casas decimais
        if n == 0:
            print(f"{n:2d}   {xn:8.4f}   {xn1:8.4f}   {EA:12.4f}   {ER:12.4f}   {f_value:10.4f}")
        else:
            print(f"{n:2d}   {xn:8.4f}   {xn1:8.4f}   {EA:12.4f}   {ER:12.4f}   {f_value:10.4f}")
        
        # Atualizar xn para próxima iteração
        xn = xn1
    
    return xn

# Parâmetros do problema
x0 = 2.0  # Chute inicial
x_star = 3.0  # Raiz verdadeira
num_iterations = 4  # Número de iterações

print("Método do Ponto Fixo com g2(x) = sqrt(x + 6)")
print(f"Valor inicial x0 = {x0}")
print(f"Raiz verdadeira x* = {x_star}")
print()

# Executar o método do ponto fixo
result = fixed_point_iteration(x0, num_iterations, x_star)

print()
print("=" * 80)
print(f"Após {num_iterations} iterações: x ≈ {result:.4f}")
print(f"Erro absoluto final: |{result:.4f} - {x_star}| = {abs(result - x_star):.4f}")