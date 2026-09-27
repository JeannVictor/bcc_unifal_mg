import numpy as np

def sor(A, b, omega, x0=None, tol=1e-8, max_iter=500):
    """
    Resolve Ax = b pelo metodo SOR.
    omega = 1.0 -> Gauss-Seidel puro.
    Retorna (solucao, num_iteracoes, historico_residuos).
    """
    if not (0 < omega <= 2.1):
        raise ValueError("omega deve estar em (0, 2)")
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
            x_gs = (b[i] - soma) / A[i, i]
            x[i] = (1 - omega) * x_old[i] + omega * x_gs
        residuo = np.linalg.norm(A @ x - b)
        historico.append(residuo)
        diff = np.linalg.norm(x - x_old, np.inf)
        denom = np.linalg.norm(x, np.inf)
        if denom > 0 and diff / denom < tol:
            return x, k + 1, historico
    
    return x, max_iter, historico


def omega_young(A):
    """
    Calcula omega_opt pela formula de Young (valida para Property A).
    Retorna (omega_opt, rho_J, rho_SOR).
    """
    D_inv = np.diag(1.0 / np.diag(A))
    R = A - np.diag(np.diag(A))
    T_J = D_inv @ R
    rho_J = np.max(np.abs(np.linalg.eigvals(T_J)))
    omega_opt = 2.0 / (1 + np.sqrt(1 - rho_J ** 2))
    rho_SOR = omega_opt - 1
    return omega_opt, rho_J, rho_SOR


def varredura_omega(A, b, omegas, tol=1e-8, max_iter=500):
    """Executa SOR para cada omega e retorna lista de iteracoes."""
    resultados = []
    for w in omegas:
        try:
            _, iters, _ = sor(A, b, w, tol=tol, max_iter=max_iter)
        except Exception:
            iters = max_iter
        resultados.append(iters)
    return resultados

def sor_com_historico_x(A, b, omega, x0=None, tol=1e-8, max_iter=500):
    """Versão que guarda histórico de x[0] (primeira componente)"""
    if not (0 < omega < 2):
        raise ValueError("omega deve estar em (0, 2)")
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float)
    historico_residuos = []
    historico_x1 = []  # Guarda x[0] (primeira componente)
    
    for k in range(max_iter):
        x_old = x.copy()
        historico_x1.append(x[0])  # Salva x1 ANTES de atualizar
        
        for i in range(n):
            soma = (np.dot(A[i, :i], x[:i])
                    + np.dot(A[i, i+1:], x_old[i+1:]))
            x_gs = (b[i] - soma) / A[i, i]
            x[i] = (1 - omega) * x_old[i] + omega * x_gs
        
        residuo = np.linalg.norm(A @ x - b)
        historico_residuos.append(residuo)
        
        diff = np.linalg.norm(x - x_old, np.inf)
        denom = np.linalg.norm(x, np.inf)
        if denom > 0 and diff / denom < tol:
            return x, k + 1, historico_residuos, historico_x1
    
    return x, max_iter, historico_residuos, historico_x1

def raio_espectral_sor(A, omega):
    """
    Calcula o raio espectral da matriz de iteração do SOR.
    """
    D = np.diag(np.diag(A))
    L = -np.tril(A, -1)  # parte triangular inferior (sem diagonal)
    U = -np.triu(A, 1)   # parte triangular superior (sem diagonal)
    
    # Matriz de iteração do SOR: M_ω = (D - ωL)⁻¹[(1-ω)D + ωU]
    M_sor = np.linalg.solve(D - omega * L, (1 - omega) * D + omega * U)
    
    # Raio espectral = maior autovalor em módulo
    rho = np.max(np.abs(np.linalg.eigvals(M_sor)))
    
    return rho