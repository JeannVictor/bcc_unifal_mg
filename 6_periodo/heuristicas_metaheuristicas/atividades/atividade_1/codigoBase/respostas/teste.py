#!/usr/bin/env python3

import os
import time

from main import read_instance
from heuristics import Heuristics

INSTANCIAS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instancias')


def testar_instancia(nome_arquivo):
    caminho = os.path.join(INSTANCIAS_DIR, nome_arquivo)
    grafo = read_instance(caminho)

    inicio = time.perf_counter()
    heur = Heuristics(grafo)
    heur.construtiva()
    custo = heur.evaluate()
    duracao = time.perf_counter() - inicio

    n_nos = grafo.number_of_nodes()
    n_arestas_caminho = len(heur.best_solution)
    cobertura = n_arestas_caminho / (n_nos - 1) if n_nos > 1 else 0

    return {
        "instancia": nome_arquivo,
        "nos": n_nos,
        "arestas_grafo": grafo.number_of_edges(),
        "arestas_caminho": n_arestas_caminho,
        "cobertura": cobertura,
        "custo": custo,
        "tempo_s": duracao,
    }


def main():
    if not os.path.isdir(INSTANCIAS_DIR):
        print(f"Pasta de instancias nao encontrada: {INSTANCIAS_DIR}")
        return

    arquivos = sorted(os.listdir(INSTANCIAS_DIR))
    resultados = []

    for nome in arquivos:
        print(f"Rodando: {nome} ...", flush=True)
        try:
            resultados.append(testar_instancia(nome))
        except Exception as e:
            print(f"  ERRO em {nome}: {e}")

    print()
    print(f"{'instancia':<20}{'nos':>8}{'arestas_g':>12}{'arestas_c':>12}{'cobertura':>11}{'custo':>14}{'tempo(s)':>10}")
    print("-" * 87)
    for r in resultados:
        print(
            f"{r['instancia']:<20}{r['nos']:>8}{r['arestas_grafo']:>12}"
            f"{r['arestas_caminho']:>12}{r['cobertura']:>11.2%}"
            f"{r['custo']:>14.2f}{r['tempo_s']:>10.3f}"
        )


if __name__ == "__main__":
    main()