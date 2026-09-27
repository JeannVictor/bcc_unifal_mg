#!/usr/bin/env python3
"""Executa e compara os cenarios das heuristicas em varias instancias."""

import argparse
import contextlib
import fnmatch
import io
import json
import os
import time

from heuristics import Heuristics
from main import read_instance


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCIAS_DIR = os.path.join(BASE_DIR, "instancias")
ALGORITMOS = ("construtiva", "reparo", "local", "local_reparo")


def construtiva_degenerada(heuristica):
    """Gera propositalmente uma solucao com repeticao de vertices."""
    if len(heuristica.graph) == 0:
        heuristica.best_solution = []
        return

    degrees = dict(heuristica.graph.degree())
    current_vertex = min(degrees, key=degrees.get)
    path = []

    for _ in range(max(0, len(heuristica.graph) - 1)):
        neighbors = list(heuristica.graph.neighbors(current_vertex))
        if not neighbors:
            break

        next_vertex = max(
            neighbors,
            key=lambda vertex: heuristica.graph.degree(vertex),
        )
        path.append((current_vertex, next_vertex))
        current_vertex = next_vertex

    heuristica.best_solution = path


def peso_da_solucao(heuristica, solucao):
    """Calcula o peso de uma lista de arestas."""
    return sum(
        heuristica.graph[u][v]["weight"]
        for u, v in solucao
    )


def quantidade_vertices(solucao):
    """Conta os vertices distintos presentes em uma lista de arestas."""
    vertices = set()
    for u, v in solucao:
        vertices.add(u)
        vertices.add(v)
    return len(vertices)


def executar_algoritmo(grafo, algoritmo):
    """Prepara e executa um dos quatro cenarios inteiramente no teste."""
    heuristica = Heuristics(grafo)

    inicio_preparacao = time.perf_counter()

    if algoritmo == "reparo":
        construtiva_degenerada(heuristica)
    elif algoritmo == "local":
        heuristica.construtiva()
    elif algoritmo == "local_reparo":
        construtiva_degenerada(heuristica)

    tempo_preparacao = time.perf_counter() - inicio_preparacao

    solucao_inicial = heuristica.best_solution.copy()
    valida_inicial, indice_falha = heuristica.check_solution()
    peso_inicial = peso_da_solucao(heuristica, solucao_inicial)
    peso_antes_busca_local = None

    inicio_algoritmo = time.perf_counter()

    if algoritmo == "construtiva":
        heuristica.construtiva()
    elif algoritmo == "reparo":
        heuristica.repair()
    elif algoritmo == "local":
        peso_antes_busca_local = peso_inicial
        heuristica.local()
    elif algoritmo == "local_reparo":
        heuristica.repair()
        peso_antes_busca_local = heuristica.evaluate()
        heuristica.local()

    tempo_algoritmo = time.perf_counter() - inicio_algoritmo

    valida_final, indice_falha_final = heuristica.check_solution()
    peso_final = heuristica.evaluate()
    numero_vertices = quantidade_vertices(heuristica.best_solution)
    cobertura = numero_vertices / len(grafo) if len(grafo) else 0.0

    return {
        "algoritmo": algoritmo,
        "valida_inicial": valida_inicial,
        "indice_falha_inicial": indice_falha,
        "valida_final": valida_final,
        "indice_falha_final": indice_falha_final,
        "peso_inicial": peso_inicial,
        "peso_final": peso_final,
        "melhoria": peso_final - peso_inicial,
        "peso_antes_busca_local": peso_antes_busca_local,
        "melhoria_local": (
            peso_final - peso_antes_busca_local
            if peso_antes_busca_local is not None
            else None
        ),
        "arestas_solucao": len(heuristica.best_solution),
        "vertices_solucao": numero_vertices,
        "cobertura": cobertura,
        "tempo_preparacao_ms": tempo_preparacao * 1000,
        "tempo_algoritmo_ms": tempo_algoritmo * 1000,
    }


def selecionar_instancias(nome=None, padrao=None):
    """Seleciona uma instancia, um padrao ou todos os arquivos da pasta."""
    arquivos = sorted(
        arquivo
        for arquivo in os.listdir(INSTANCIAS_DIR)
        if os.path.isfile(os.path.join(INSTANCIAS_DIR, arquivo))
    )

    if nome:
        if nome not in arquivos:
            raise FileNotFoundError(f"Instancia nao encontrada: {nome}")
        return [nome]

    if padrao:
        arquivos = [arquivo for arquivo in arquivos if fnmatch.fnmatch(arquivo, padrao)]
        if not arquivos:
            raise FileNotFoundError(f"Nenhuma instancia corresponde a: {padrao}")

    return arquivos


def executar_teste(nome_instancia, metodo, repeticao, mostrar_execucao=False):
    """Executa um cenario e devolve apenas dados serializaveis."""
    caminho = os.path.join(INSTANCIAS_DIR, nome_instancia)
    grafo = read_instance(caminho)

    if grafo is None:
        raise ValueError("instancia vazia ou invalida")

    if mostrar_execucao:
        resultado = executar_algoritmo(grafo, metodo)
    else:
        with contextlib.redirect_stdout(io.StringIO()):
            resultado = executar_algoritmo(grafo, metodo)

    return {
        "instancia": nome_instancia,
        "repeticao": repeticao,
        "metodo": resultado["algoritmo"],
        "nos_grafo": grafo.number_of_nodes(),
        "arestas_grafo": grafo.number_of_edges(),
        "valida_inicial": resultado["valida_inicial"],
        "indice_falha_inicial": resultado["indice_falha_inicial"],
        "valida_final": resultado["valida_final"],
        "indice_falha_final": resultado["indice_falha_final"],
        "peso_inicial": resultado["peso_inicial"],
        "peso_final": resultado["peso_final"],
        "melhoria": resultado["melhoria"],
        "peso_antes_busca_local": resultado["peso_antes_busca_local"],
        "melhoria_local": resultado["melhoria_local"],
        "arestas_solucao": resultado["arestas_solucao"],
        "vertices_solucao": resultado["vertices_solucao"],
        "cobertura": resultado["cobertura"],
        "tempo_preparacao_ms": resultado["tempo_preparacao_ms"],
        "tempo_metodo_ms": resultado["tempo_algoritmo_ms"],
    }


def imprimir_tabela(resultados):
    """Imprime os resultados em uma tabela compacta."""
    print()
    print("Resultados")
    cabecalho = (
        f"{'instancia':<18} {'metodo':<14} {'rep':>3} "
        f"{'val.in':>7} {'val.fim':>7} {'peso.in':>11} "
        f"{'peso.fim':>11} {'ganho':>10} {'cobert.':>8} {'tempo(ms)':>11}"
    )
    print(cabecalho)
    print("-" * len(cabecalho))

    for resultado in resultados:
        ganho = (
            resultado["melhoria_local"]
            if resultado["melhoria_local"] is not None
            else resultado["melhoria"]
        )
        print(
            f"{resultado['instancia']:<18} "
            f"{resultado['metodo']:<14} "
            f"{resultado['repeticao']:>3} "
            f"{str(resultado['valida_inicial']):>7} "
            f"{str(resultado['valida_final']):>7} "
            f"{resultado['peso_inicial']:>11.2f} "
            f"{resultado['peso_final']:>11.2f} "
            f"{ganho:>+10.2f} "
            f"{resultado['cobertura']:>8.2%} "
            f"{resultado['tempo_metodo_ms']:>11.4f}"
        )


def imprimir_validacoes(resultados):
    """Destaca falhas de validade e o efeito da busca local."""
    finais_invalidos = [resultado for resultado in resultados if not resultado["valida_final"]]
    locais = [
        resultado
        for resultado in resultados
        if resultado["metodo"] in ("local", "local_reparo")
    ]
    locais_melhores = [
        resultado
        for resultado in locais
        if resultado["melhoria_local"] is not None
        and resultado["melhoria_local"] > 0
    ]

    print()
    print("Validacoes")
    print(f"- Execucoes realizadas: {len(resultados)}")
    print(f"- Solucoes finais validas: {len(resultados) - len(finais_invalidos)}/{len(resultados)}")
    print(f"- Buscas locais que aumentaram o peso: {len(locais_melhores)}/{len(locais)}")

    if finais_invalidos:
        print("- ATENCAO: houve solucoes finais invalidas:")
        for resultado in finais_invalidos:
            print(
                f"  {resultado['instancia']} / {resultado['metodo']} "
                f"(falha={resultado['indice_falha_final']})"
            )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Testa construtiva, reparo, busca local sem reparo e "
            "busca local com reparo."
        )
    )
    parser.add_argument(
        "--metodo",
        choices=("todos",) + ALGORITMOS,
        default="todos",
        help="Cenario a executar (padrao: todos).",
    )
    grupo_instancia = parser.add_mutually_exclusive_group()
    grupo_instancia.add_argument(
        "--instancia",
        help="Executa somente o arquivo informado.",
    )
    grupo_instancia.add_argument(
        "--padrao",
        help='Executa arquivos que correspondem ao padrao, por exemplo "regular-1000-*".',
    )
    parser.add_argument(
        "--repeticoes",
        type=int,
        default=1,
        help="Quantidade de repeticoes de cada cenario (padrao: 1).",
    )
    parser.add_argument(
        "--mostrar-execucao",
        action="store_true",
        help="Mostra tambem as mensagens internas das heuristicas.",
    )
    parser.add_argument(
        "--saida",
        default=os.path.join(BASE_DIR, "resultados_testes.json"),
        help="Arquivo JSON no qual os resultados serao gravados.",
    )
    args = parser.parse_args()

    if args.repeticoes < 1:
        parser.error("--repeticoes deve ser pelo menos 1")

    try:
        instancias = selecionar_instancias(args.instancia, args.padrao)
    except FileNotFoundError as error:
        parser.error(str(error))

    metodos = ALGORITMOS if args.metodo == "todos" else (args.metodo,)
    resultados = []

    for nome_instancia in instancias:
        for metodo in metodos:
            for repeticao in range(1, args.repeticoes + 1):
                print(
                    f"Testando {nome_instancia} / {metodo} "
                    f"(repeticao {repeticao})...",
                    flush=True,
                )
                try:
                    resultados.append(
                        executar_teste(
                            nome_instancia,
                            metodo,
                            repeticao,
                            args.mostrar_execucao,
                        )
                    )
                except Exception as error:
                    print(f"  ERRO: {type(error).__name__}: {error}")

    with open(args.saida, "w", encoding="utf-8") as arquivo:
        json.dump(resultados, arquivo, indent=2, ensure_ascii=False)

    imprimir_tabela(resultados)
    imprimir_validacoes(resultados)
    print(f"\nResultados completos salvos em: {args.saida}")


if __name__ == "__main__":
    main()
