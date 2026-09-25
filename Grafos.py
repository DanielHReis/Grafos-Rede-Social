# self.amizades = lista de adjacência para amizades(não-direcionado) aponta para um conjunto de "vizinhos"

# self.seguindo = lista de adjacência(dígrafo)

# self.peso = peso das arestas (força de intereção: numero de mensagens/curtidas)

from collections import deque
import heapq


class RedeSocial:
    def __init__(self):
        self.amizades = {}

        self.seguindo = {}

        self.pesos = {}

    def adicionar_usuario(self, usuario): # (adiciona um vértice)
        self.amizades.setdefault(usuario, set())
        self.seguindo.setdefault(usuario, set())

    def adicionar_amizade(self, u1, u2, peso=1): # (adiciona aresta não-direcionada)
        # """Aresta não-direcionada: amizade é mútua (u1 <-> u2)."""
        self.adicionar_usuario(u1)
        self.adicionar_usuario(u2)
        self.amizades[u1].add(u2)
        self.amizades[u2].add(u1)
        self.pesos[(u1, u2)] = peso
        self.pesos[(u2, u1)] = peso

    def adicionar_seguidor(self, quem_segue, quem_e_seguido): # (adiciona aresta direcionada)
        # """Aresta direcionada: caracteriza o DÍGRAFO (ex: A segue B)."""
        self.adicionar_usuario(quem_segue)
        self.adicionar_usuario(quem_e_seguido)
        self.seguindo[quem_segue].add(quem_e_seguido)

    def mostrar_lista_adjacencia(self):
        print("\nLista de adjacência das amizades:")
        for usuario in self.amizades:
            print(f"   {usuario} -> {self.amizades[usuario]}")

        print("\nLista de adjacência dos seguidores:")
        for usuario in self.seguindo:
            print(f"   {usuario} -> {self.seguindo[usuario]}")

    def grau_de_separacao(self, origem, destino):

        # BFS (breadth-first search), busca o caminho mais curto
        # em arestas entre um vértice de origem e destino.

        if origem not in self.amizades or destino not in self.amizades:
            return None

        visitados = {origem}
        fila = deque([(origem, [origem])])

        while fila:
            atual, caminho = fila.popleft()
            if atual == destino:
                return caminho
            for vizinho in self.amizades[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append((vizinho, caminho + [vizinho]))

        return None  # não existe caminho -> usuários em componentes diferentes


    # DFS (Depth-First Search), a partir de um vértice de origem
    # explora o grafo indo o mais fundo possível ao longo de um ramo
    # antes de retroceder (backtracking)

    # verificação de conexidade

    def _dfs_visita(self, usuario, visitados, componente):
        visitados.add(usuario)
        componente.append(usuario)
        for vizinho in self.amizades[usuario]:
            if vizinho not in visitados:
                self._dfs_visita(vizinho, visitados, componente)

    def componentes_conexos(self):
        visitados = set()
        componentes = []
        for usuario in self.amizades:
            if usuario not in visitados:
                componente = []
                self._dfs_visita(usuario, visitados, componente)
                componentes.append(componente)
        return componentes

    def eh_conexo(self):
        return len(self.componentes_conexos()) == 1


    # DFS (Depth-First Search)
    # Detecção de ciclo no dígrafo de "seguidores"

    def existe_circuito(self):
        BRANCO, CINZA, PRETO = 0, 1, 2
        estado = {u: BRANCO for u in self.seguindo}

        def dfs(u):
            estado[u] = CINZA
            for v in self.seguindo[u]:
                if estado[v] == CINZA:
                    return True  # aresta de retorno -> circuito encontrado
                if estado[v] == BRANCO and dfs(v):
                    return True
            estado[u] = PRETO
            return False

        return any(dfs(u) for u in self.seguindo if estado[u] == BRANCO)


    # DIJKSTRA utilizado para encontrar o caminho mais próximo
    # (menor custo ou distancia total) entre um vértice de origem
    # e todos os demais vértices em um grafo ponderado.
    # Usado para resolver problemas de rotas e navegação
    # quando arestas possuem pesos numéricos.

    def caminho_mais_proximo(self, origem, destino):

        distancias = {u: float('inf') for u in self.amizades}
        anteriores = {u: None for u in self.amizades}
        distancias[origem] = 0
        fila = [(0, origem)]
        visitados = set()

        while fila:
            dist_atual, atual = heapq.heappop(fila)
            if atual in visitados:
                continue
            visitados.add(atual)

            if atual == destino:
                break

            for vizinho in self.amizades[atual]:
                peso = self.pesos.get((atual, vizinho), 1)
                custo = 1 / peso  # interação forte = custo baixo
                nova_dist = dist_atual + custo
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    anteriores[vizinho] = atual
                    heapq.heappush(fila, (nova_dist, vizinho))

        if distancias[destino] == float('inf'):
            return None, None

        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]
        caminho.reverse()
        return caminho, distancias[destino]


    # Descobrir quem é o mais influente

    def usuarios_mais_influentes(self, top_n=3):
        seguidores_count = {u: 0 for u in self.seguindo}
        for u, seguidos in self.seguindo.items():
            for alvo in seguidos:
                seguidores_count[alvo] += 1
        return sorted(seguidores_count.items(), key=lambda x: x[1], reverse=True)[:top_n]


# Demonstração

if __name__ == "__main__":
    rede = RedeSocial()

    rede.adicionar_amizade("Ana", "Bruno", peso=5)
    rede.adicionar_amizade("Bruno", "Carla", peso=2)
    rede.adicionar_amizade("Carla", "Diego", peso=8)
    rede.adicionar_amizade("Diego", "Elis", peso=1)
    rede.adicionar_amizade("Ana", "Carla", peso=1)
    rede.adicionar_amizade("Fabio", "Gina")

    rede.adicionar_seguidor("Ana", "Bruno")
    rede.adicionar_seguidor("Bruno", "Carla")
    rede.adicionar_seguidor("Carla", "Ana")
    rede.adicionar_seguidor("Diego", "Carla")

    print("=" * 60)

    # NOVO: demonstração da lista de adjacência
    print("0) LISTA DE ADJACÊNCIA:")
    rede.mostrar_lista_adjacencia()

    print("\n1) CAMINHO (BFS) - grau de separação entre Ana e Elis:")
    caminho = rede.grau_de_separacao("Ana", "Elis")
    print(f"   {' -> '.join(caminho)}  ({len(caminho)-1} graus de separação)")

    print("\n2) CONEXIDADE (DFS) - componentes conexos da rede:")
    for i, comp in enumerate(rede.componentes_conexos(), 1):
        print(f"   Componente {i}: {comp}")
    print(f"   A rede é totalmente conexa? {rede.eh_conexo()}")

    print("\n3) CIRCUITO (DFS no dígrafo) - existe ciclo em 'seguidores'?")
    print(f"   {rede.existe_circuito()}  (Ana->Bruno->Carla->Ana)")

    print("\n4) DIJKSTRA - caminho de conexão mais forte entre Ana e Elis:")
    caminho2, custo = rede.caminho_mais_proximo("Ana", "Elis")
    print(f"   {' -> '.join(caminho2)}  (custo acumulado: {custo:.2f})")

    print("\n5) Usuários mais influentes (mais seguidores):")
    for usuario, qtd in rede.usuarios_mais_influentes():
        print(f"   {usuario}: {qtd} seguidor(es)")

    print("=" * 60)