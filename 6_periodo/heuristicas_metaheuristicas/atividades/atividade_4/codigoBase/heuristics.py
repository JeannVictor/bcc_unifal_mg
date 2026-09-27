import time


class Heuristics:
    def __init__(self, instance_data):
        """
        Initialize the Heuristics class with the instance data.
        """
        self.graph = instance_data

        # A solution is represented as a list of edges,
        # where each edge is an ordered pair of nodes (u, v).
        self.best_solution: list[tuple[int, int]] = []

    def construtiva(self):
        """
        Constructive heuristic.
        """
        print("Executing construtiva algorithm...")

        # Escolha um vértice inicial de forma arbitrária
        # (por exemplo, o de menor grau).
        degrees = dict(self.graph.degree())
        start_vertex = min(degrees, key=degrees.get)

        visited = {start_vertex}
        path = []
        current_vertex = start_vertex

        # Escolha o próximo vértice a ser adicionado ao caminho
        # como aquele que possui o maior grau entre os vértices
        # ainda não visitados.
        # Repita o passo 2 até que todos os vértices tenham sido visitados.
        while len(visited) < len(self.graph):
            current_neighbors = list(self.graph.neighbors(current_vertex))
            max_degree = -1
            next_vertex = None

            for neighbor in current_neighbors:
                if neighbor not in visited:
                    if self.graph.degree(neighbor) > max_degree:
                        max_degree = self.graph.degree(neighbor)
                        next_vertex = neighbor

            if next_vertex is not None:
                path.append((current_vertex, next_vertex))
                visited.add(next_vertex)
                current_vertex = next_vertex
            else:
                break

        self.best_solution = path

    def evaluate(self):
        """
        Evaluate the solution.
        """
        cost = 0

        for u, v in self.best_solution:
            cost += self.graph[u][v]["weight"]

        return cost

    def check_solution(self):
        visited = set()

        for i, (u, v) in enumerate(self.best_solution):
            visited.add(u)

            if v not in visited:
                visited.add(v)
            else:
                return False, i

        return True, None

    def repair(self):
        """
        Repair the solution to make it valid.
        """
        valido, indice_falha = self.check_solution()

        if valido:
            print("Solução já é válida, não precisa de reparo.")
            return

        print("Solução é inválida, precisa de reparo.")

        path = self.best_solution[:indice_falha]

        visited = set()

        for u, v in path:
            visited.add(u)
            visited.add(v)

        current_vertex = path[-1][1]

        while len(visited) < len(self.graph):
            current_neighbors = list(self.graph.neighbors(current_vertex))
            max_degree = -1
            next_vertex = None

            for neighbor in current_neighbors:
                if neighbor not in visited:
                    if self.graph.degree(neighbor) > max_degree:
                        max_degree = self.graph.degree(neighbor)
                        next_vertex = neighbor

            if next_vertex is not None:
                path.append((current_vertex, next_vertex))
                visited.add(next_vertex)
                current_vertex = next_vertex
            else:
                break

        self.best_solution = path

        valido_final, indice_falha_final = self.check_solution()

        if valido_final:
            print("Reparo concluído: solução final é válida.")
        else:
            print(
                f"ATENÇÃO: reparo terminou, mas a solução ainda é inválida "
                f"(falha na aresta de índice {indice_falha_final})."
            )


    def local(self):
        """
        Local search heuristic.
        """
        print("Executing local search algorithm...")

        valido, _ = self.check_solution()

        if not valido:
            self.repair()

        valido, _ = self.check_solution()

        if not valido:
            print("Não foi possível obter uma solução válida.")
            return

        melhorou = True

        while melhorou:
            melhorou = False

            peso_antigo = self.evaluate()
            partial_solution = self.best_solution.copy()

            if not partial_solution:
                break

            ultima_aresta = partial_solution.pop()

            # Descobre o vértice final do caminho restante.
            if partial_solution:
                current_vertex = partial_solution[-1][1]
            else:
                current_vertex = ultima_aresta[0]

            visited = set()

            for u, v in partial_solution:
                visited.add(u)
                visited.add(v)

            visited.add(current_vertex)

            # Na primeira escolha, evita reconstruir imediatamente
            # a mesma aresta que acabou de ser removida.
            primeiro_movimento = True

            # Reconstrói o final do caminho.
            while len(visited) < len(self.graph):
                current_neighbors = list(
                    self.graph.neighbors(current_vertex)
                )

                max_weight = float("-inf")
                next_vertex = None

                for neighbor in current_neighbors:
                    if neighbor in visited:
                        continue

                    if (
                        primeiro_movimento
                        and neighbor == ultima_aresta[1]
                    ):
                        continue

                    weight = self.graph[current_vertex][neighbor]["weight"]

                    if weight > max_weight:
                        max_weight = weight
                        next_vertex = neighbor

                if next_vertex is None:
                    break

                partial_solution.append(
                    (current_vertex, next_vertex)
                )

                visited.add(next_vertex)
                current_vertex = next_vertex
                primeiro_movimento = False

            # Calcula o peso do caminho completamente reconstruído.
            peso_novo = 0

            for u, v in partial_solution:
                peso_novo += self.graph[u][v]["weight"]

            # Só substitui a solução quando existe melhoria estrita.
            if peso_novo > peso_antigo:
                self.best_solution = partial_solution
                melhorou = True

                print(
                    f"Melhoria encontrada: "
                    f"{peso_antigo} -> {peso_novo}"
                )

        print(
            f"Busca local finalizada. "
            f"Peso final: {self.evaluate()}"
        )

    def vizinhanca(self, quantidade_arestas, tempo_final):
        """
        Gera um vizinho removendo arestas do final do caminho e
        reconstruindo essa parte de forma gulosa.
        """
        if quantidade_arestas > len(self.best_solution):
            return None

        partial_solution = self.best_solution.copy()
        arestas_removidas = []

        for _ in range(quantidade_arestas):
            arestas_removidas.insert(0, partial_solution.pop())

        if partial_solution:
            current_vertex = partial_solution[-1][1]
        else:
            current_vertex = arestas_removidas[0][0]

        visited = set()

        for u, v in partial_solution:
            visited.add(u)
            visited.add(v)

        visited.add(current_vertex)
        primeiro_movimento = True
        antigo_proximo_vertice = arestas_removidas[0][1]

        while len(visited) < len(self.graph):
            if time.perf_counter() >= tempo_final:
                return None

            current_neighbors = list(
                self.graph.neighbors(current_vertex)
            )

            max_weight = float("-inf")
            next_vertex = None

            for neighbor in current_neighbors:
                if neighbor in visited:
                    continue

                if (
                    primeiro_movimento
                    and neighbor == antigo_proximo_vertice
                ):
                    continue

                weight = self.graph[current_vertex][neighbor]["weight"]

                if weight > max_weight:
                    max_weight = weight
                    next_vertex = neighbor

            if next_vertex is None:
                break

            partial_solution.append(
                (current_vertex, next_vertex)
            )

            visited.add(next_vertex)
            current_vertex = next_vertex
            primeiro_movimento = False

        return partial_solution

    def vnd(self, tempo_maximo=30):
        """
        Variable Neighborhood Descent (VND).
        """
        print("Executing VND algorithm...")

        inicio = time.perf_counter()
        tempo_final = inicio + tempo_maximo

        if not self.best_solution:
            self.construtiva()

        valido, _ = self.check_solution()

        if not valido:
            self.repair()

        estruturas_vizinhanca = [1, 2, 3]
        k = 0

        while (
            k < len(estruturas_vizinhanca)
            and time.perf_counter() < tempo_final
        ):
            peso_antigo = self.evaluate()
            quantidade_arestas = estruturas_vizinhanca[k]

            nova_solucao = self.vizinhanca(
                quantidade_arestas,
                tempo_final,
            )

            if nova_solucao is None:
                break

            peso_novo = 0

            for u, v in nova_solucao:
                peso_novo += self.graph[u][v]["weight"]

            if peso_novo > peso_antigo:
                self.best_solution = nova_solucao
                k = 0

                print(
                    f"Melhoria encontrada: "
                    f"{peso_antigo} -> {peso_novo}"
                )
            else:
                k += 1

        tempo_execucao = time.perf_counter() - inicio

        print(
            f"VND finalizado. "
            f"Peso final: {self.evaluate()}. "
            f"Tempo: {tempo_execucao:.4f} segundos"
        )

        
        


        
            
