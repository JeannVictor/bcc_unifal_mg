class Heuristics:
    def __init__(self, instance_data):
        """
        Initialize the Heuristics class with the instance data.
        """
        self.graph = instance_data
        # A solution is represented as a list of edges, where each edge is an ordered pair of nodes (u, v).
        self.best_solution: list[tuple[int, int]] = []

    def construtiva(self):
        """
        Constructive heuristic.
        """
        print("Executing construtiva algorithm...")

        #Escolha um vértice inicial de forma arbitrária (por exemplo, o de menor grau).
        degrees = dict(self.graph.degree())
        start_vertex = min(degrees, key=degrees.get)

        visited = {start_vertex}
        path = []
        current_vertex = start_vertex

        # Escolha o próximo vértice a ser adicionado ao caminho como aquele que possui o maior grau entre os vértices ainda não visitados.        
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

    def local(self):
        """
        Local search heuristic.
        """
        print("Executing local search algorithm...")
        # Add implementation here
        pass

    def evaluate(self):
        """
        Evaluate the solution.
        """
        cost = 0
        for u, v in self.best_solution:
            cost += self.graph[u][v]['weight']

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
            print(f"ATENÇÃO: reparo terminou, mas a solução ainda é inválida "
                  f"(falha na aresta de índice {indice_falha_final}).")

        
            



