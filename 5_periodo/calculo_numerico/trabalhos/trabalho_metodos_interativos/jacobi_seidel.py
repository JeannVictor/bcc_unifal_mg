import numpy as np

def jacobi(A, b, x0=None, tol=1e-8, max_iter=500):
    """
    Resolve Ax = b pelo metodo de Gauss-Jacobi.
    Retorna (solucao, num_iteracoes, historico_residuos).
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    
    D_inv = 1.0 / np.diag(A)
    R = A - np.diag(np.diag(A))
    historico = []
    
    for k in range(max_iter):
        x_new = D_inv * (b - R @ x)
        residuo = np.linalg.norm(A @ x_new - b)
        historico.append(residuo)
        diff = np.linalg.norm(x_new - x, np.inf)
        denom = np.linalg.norm(x_new, np.inf)
        if denom > 0 and diff / denom < tol:
            return x_new, k + 1, historico
        x = x_new
    
    return x, max_iter, historico


def gauss_seidel(A, b, x0=None, tol=1e-8, max_iter=500):
    """
    Resolve Ax = b pelo metodo de Gauss-Seidel.
    Retorna (solucao, num_iteracoes, historico_residuos).
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    historico = []
    
    for k in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            soma = (np.dot(A[i, :i], x[:i]) 
                    + np.dot(A[i, i+1:], x_old[i+1:]))
            x[i] = (b[i] - soma) / A[i, i]
        residuo = np.linalg.norm(A @ x - b)
        historico.append(residuo)
        diff = np.linalg.norm(x - x_old, np.inf)
        denom = np.linalg.norm(x, np.inf)
        if denom > 0 and diff / denom < tol:
            return x, k + 1, historico
    
    return x, max_iter, historico

def gauss_seidel_modificado(A, b, x0=None, tol=1e-8, max_iter=500):
    """
    Versão modificada que mostra quais valores são usados (novo vs antigo)
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    historico = []
    
    for k in range(max_iter):
        x_old = x.copy()
        
        print(f"\n{'-'*90}")
        print(f"Iteração {k+1}:")
        print(f"Valores ANTIGOS (início da iteração): x = {x_old}")
        print(f"{'-'*90}")
        
        for i in range(n):
            # Calcula a soma separando termos com valores novos e antigos
            soma_novos = 0
            soma_antigos = 0
            
            # Termos com índices < i (já foram atualizados → NOVOS)
            for j in range(i):
                termo = A[i, j] * x[j]
                soma_novos += termo
            
            # Termos com índices > i (ainda não foram atualizados → ANTIGOS)
            for j in range(i+1, n):
                termo = A[i, j] * x_old[j]
                soma_antigos += termo
            
            x[i] = (b[i] - soma_novos - soma_antigos) / A[i, i]
            
            # Imprime detalhe do cálculo
            print(f"\n  x{i+1} = (b{i+1} - [NOVOS] - [ANTIGOS]) / A{i+1}{i+1}")
            print(f"       = ({b[i]} - ({soma_novos:.4f}) - ({soma_antigos:.4f})) / {A[i,i]}")
            print(f"       = {x[i]:.6f}")
            print(f"       → USOU: ", end="")
            
            for j in range(i):
                print(f"x{j+1}(NOVO={x[j]:.4f}) ", end="")
            for j in range(i+1, n):
                print(f"x{j+1}(ANTIGO={x_old[j]:.4f}) ", end="")
            print()
        
        residuo = np.linalg.norm(A @ x - b)
        historico.append(residuo)
        
        print(f"\nValores NOVOS (fim da iteração): x = {x}")
        print(f"Resíduo: {residuo:.6e}")
        
        diff = np.linalg.norm(x - x_old, np.inf)
        denom = np.linalg.norm(x, np.inf)
        if denom > 0 and diff / denom < tol:
            return x, k + 1, historico
    
    return x, max_iter, historico

def raio_espectral(A, metodo='jacobi'):
    """Calcula rho(T_J) ou rho(T_GS) numericamente."""
    D = np.diag(np.diag(A))
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)
    if metodo == 'jacobi':
        T = np.linalg.inv(D) @ (L + U)
    else:
        T = np.linalg.inv(D - L) @ U
    return np.max(np.abs(np.linalg.eigvals(T))), T