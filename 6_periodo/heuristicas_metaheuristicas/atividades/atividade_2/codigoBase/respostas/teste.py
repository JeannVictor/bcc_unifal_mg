#!/usr/bin/env python3
"""
experimento.py

Compara, em instâncias reais (regular e udg, esparsas):
1. construtiva() pura -> tempo e cobertura (sempre válida).
2. construtiva_degenerada() (ignora vértices visitados, gera solução
   inválida de propósito, seguindo a opção (b) sugerida na aula_08.md)
   seguida de repair() -> tempo do reparo e cobertura final.

Também confirma, via check_solution(), que o repair() sempre devolve
uma solução válida.
"""

import os
import time
import json

from main import read_instance
from heuristics import Heuristics

INSTANCIAS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instancias')


def construtiva_degenerada(h):
    """
    Versão degenerada da construtiva: escolhe sempre o vizinho de maior
    grau, mas SEM excluir vértices já visitados -> gera uma solução
    inválida de propósito (opção b do enunciado da aula_08).
    """
    degrees = dict(h.graph.degree())
    start_vertex = min(degrees, key=degrees.get)
    path = []
    current_vertex = start_vertex

    # roda por um número de passos igual ao da construtiva normal,
    # mas sem checar se o vizinho já foi visitado
    for _ in range(len(h.graph) - 1):
        current_neighbors = list(h.graph.neighbors(current_vertex))
        if not current_neighbors:
            break
        next_vertex = max(current_neighbors, key=lambda v: h.graph.degree(v))
        path.append((current_vertex, next_vertex))
        current_vertex = next_vertex

    h.best_solution = path
    return path


def forcar_invalidez_perto_do_fim(solucao_valida):
    """
    Pega uma solução válida e força uma repetição na penúltima aresta,
    apontando para um vértice já visitado bem no início do caminho.
    Simula uma corrupção "tardia": quase tudo deveria ser aproveitável.
    """
    sol = list(solucao_valida)
    if len(sol) < 2:
        return sol
    vertice_ja_visitado = sol[0][0]
    u, _ = sol[-1]
    sol[-1] = (u, vertice_ja_visitado)
    return sol


def testar_instancia(nome_arquivo):
    caminho = os.path.join(INSTANCIAS_DIR, nome_arquivo)
    grafo = read_instance(caminho)
    n_nos = grafo.number_of_nodes()

    # --- 1. construtiva pura ---
    h1 = Heuristics(grafo)
    t0 = time.perf_counter()
    h1.construtiva()
    t_construtiva = time.perf_counter() - t0
    valida_construtiva, _ = h1.check_solution()
    cobertura_construtiva = len(h1.best_solution) / (n_nos - 1) if n_nos > 1 else 0

    # --- 2. degenerada (inválida) + repair ---
    h2 = Heuristics(grafo)
    sol_invalida = construtiva_degenerada(h2)
    valida_antes, indice_falha = h2.check_solution()
    tamanho_antes_reparo = len(sol_invalida)

    t0 = time.perf_counter()
    h2.repair()
    t_repair = time.perf_counter() - t0
    valida_depois, _ = h2.check_solution()
    cobertura_reparada = len(h2.best_solution) / (n_nos - 1) if n_nos > 1 else 0

    # --- 3. corrupção tardia (perto do fim) + repair, a partir da própria construtiva ---
    h3 = Heuristics(grafo)
    h3.construtiva()
    sol_valida_original = list(h3.best_solution)
    sol_corrompida_tarde = forcar_invalidez_perto_do_fim(sol_valida_original)
    h3.best_solution = sol_corrompida_tarde
    _, indice_falha_tarde = h3.check_solution()

    t0 = time.perf_counter()
    h3.repair()
    t_repair_tarde = time.perf_counter() - t0
    valida_depois_tarde, _ = h3.check_solution()
    cobertura_reparada_tarde = len(h3.best_solution) / (n_nos - 1) if n_nos > 1 else 0

    return {
        "instancia": nome_arquivo,
        "nos": n_nos,
        "arestas_grafo": grafo.number_of_edges(),
        "t_construtiva_ms": t_construtiva * 1000,
        "cobertura_construtiva": cobertura_construtiva,
        "construtiva_valida": valida_construtiva,
        "tam_solucao_invalida": tamanho_antes_reparo,
        "indice_falha": indice_falha,
        "t_repair_ms": t_repair * 1000,
        "cobertura_reparada": cobertura_reparada,
        "reparo_valido": valida_depois,
        "indice_falha_tarde": indice_falha_tarde,
        "t_repair_tarde_ms": t_repair_tarde * 1000,
        "cobertura_reparada_tarde": cobertura_reparada_tarde,
        "reparo_tarde_valido": valida_depois_tarde,
    }


def main():
    arquivos = sorted(os.listdir(INSTANCIAS_DIR))
    resultados = []
    for nome in arquivos:
        print(f"Rodando: {nome} ...", flush=True)
        try:
            resultados.append(testar_instancia(nome))
        except Exception as e:
            print(f"  ERRO em {nome}: {type(e).__name__}: {e}")

    with open("resultados.json", "w") as f:
        json.dump(resultados, f, indent=2)

    print()
    print("== Cenário A: corrupção cedo (construtiva_degenerada) ==")
    header = f"{'instancia':<16}{'nos':>6}{'t_constr(ms)':>14}{'cob_constr':>11}{'idx_falha':>10}{'t_repair(ms)':>14}{'cob_rep':>9}{'ok':>6}"
    print(header)
    print("-" * len(header))
    for r in resultados:
        print(
            f"{r['instancia']:<16}{r['nos']:>6}{r['t_construtiva_ms']:>14.4f}"
            f"{r['cobertura_construtiva']:>11.2%}{str(r['indice_falha']):>10}"
            f"{r['t_repair_ms']:>14.4f}{r['cobertura_reparada']:>9.2%}"
            f"{str(r['reparo_valido']):>6}"
        )

    print()
    print("== Cenário B: corrupção tardia (perto do fim do caminho) ==")
    header2 = f"{'instancia':<16}{'nos':>6}{'idx_falha':>10}{'t_repair(ms)':>14}{'cob_rep':>9}{'ok':>6}"
    print(header2)
    print("-" * len(header2))
    for r in resultados:
        print(
            f"{r['instancia']:<16}{r['nos']:>6}{str(r['indice_falha_tarde']):>10}"
            f"{r['t_repair_tarde_ms']:>14.4f}{r['cobertura_reparada_tarde']:>9.2%}"
            f"{str(r['reparo_tarde_valido']):>6}"
        )


if __name__ == "__main__":
    main()