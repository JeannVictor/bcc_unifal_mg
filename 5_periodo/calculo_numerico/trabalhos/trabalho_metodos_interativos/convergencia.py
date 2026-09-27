import numpy as np

def criterio_linhas(A):
    """
    Verifica diagonal dominancia estrita por linhas.
    Retorna (satisfaz, alfas) onde alfas[i] = soma_j != i |a_ij| / |a_ii|.
    """
    n = A.shape[0]
    alfas = np.array([
        sum(abs(A[i, j]) for j in range(n) if j != i) / abs(A[i, i])
        for i in range(n)
    ])
    return np.all(alfas < 1), alfas


def criterio_sassenfeld(A):
    """
    Criterio de Sassenfeld para Gauss-Seidel.
    Retorna (satisfaz, betas).
    """
    n = A.shape[0]
    betas = np.zeros(n)
    betas[0] = sum(abs(A[0, j]) for j in range(1, n)) / abs(A[0, 0])
    for i in range(1, n):
        soma = sum(abs(A[i, s]) * betas[s] for s in range(i))
        soma += sum(abs(A[i, s]) for s in range(i + 1, n))
        betas[i] = soma / abs(A[i, i])
    return np.max(betas) < 1, betas


def diagnostico(A, nome="A"):
    """Imprime diagnostico completo de convergencia para a matriz A."""
    print(f"\n=== Diagnostico: {nome} ===")
    ok_lin, alfas = criterio_linhas(A)
    ok_sas, betas = criterio_sassenfeld(A)
    print(f"Criterio das linhas (Jacobi/GS): {'OK' if ok_lin else 'FALHA'}"
          f" | alpha = {np.max(alfas):.4f}")
    print(f"Criterio de Sassenfeld (GS): {'OK' if ok_sas else 'FALHA'}"
          f" | beta = {np.max(betas):.4f}")
    from jacobi_seidel import raio_espectral
    rho_j, _ = raio_espectral(A, 'jacobi')
    rho_gs, _ = raio_espectral(A, 'seidel')
    print(f"Raio espectral Jacobi: rho_J = {rho_j:.6f}")
    print(f"Raio espectral GS: rho_GS = {rho_gs:.6f}")
    print(f"Convergencia garantida: J={'Sim' if rho_j < 1 else 'NAO'}"
          f" | GS={'Sim' if rho_gs < 1 else 'NAO'}")