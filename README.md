# Rede Social como Grafo

Projeto acadêmico que modela uma **rede social** utilizando **grafos** como estrutura de dados, aplicando os principais conceitos de Teoria dos Grafos vistos em sala: dígrafos, conexidade, caminho e circuito.

## Sumário

- [Contexto e Motivação](#contexto-e-motivação)
- [Modelagem do Problema](#modelagem-do-problema)
- [Estrutura de Dados Utilizada](#estrutura-de-dados-utilizada)
- [Conceitos de Grafos Aplicados](#conceitos-de-grafos-aplicados)
- [Algoritmos Implementados](#algoritmos-implementados)
- [Como Executar](#como-executar)
- [Exemplo de Uso](#exemplo-de-uso)
- [Referências](#referências)

## Contexto e Motivação

Redes sociais reais (Facebook, Instagram, Twitter/X, LinkedIn) armazenam suas conexões entre usuários literalmente como grafos, muitas vezes em bancos de dados orientados a grafos (ex: Neo4j) ou em listas de adjacência distribuídas entre servidores.

Este projeto modela uma versão simplificada dessa infraestrutura, contemplando dois tipos de relacionamento que coexistem em plataformas reais:

- **Amizade**: relação mútua e simétrica (ex: Facebook, LinkedIn).
- **Seguir**: relação assimétrica, que define o fluxo de distribuição de conteúdo (ex: Instagram, Twitter/X). É a base real de infraestruturas de recomendação e de construção de feed.

## Modelagem do Problema

O sistema é representado por dois grafos sobre o mesmo conjunto de vértices (usuários):

| Grafo | Tipo | Representa |
|---|---|---|
| `amizades` | Não-direcionado, ponderado | Vínculo mútuo entre usuários, com peso = força da interação (nº de mensagens/curtidas) |
| `seguindo` | Direcionado (dígrafo) | Relação assimétrica "A segue B", que não implica "B segue A" |

**Vértices**: usuários da rede.
**Arestas de amizade**: pares `(u1, u2)` com peso numérico.
**Arestas de seguidor**: pares ordenados `(quem_segue, quem_é_seguido)`.

## Estrutura de Dados Utilizada

O projeto utiliza **Lista de Adjacência**, implementada em Python como um dicionário (`dict`) onde cada usuário aponta para um **conjunto (`set`)** de vizinhos:

```python
self.amizades = {}   # grafo não-direcionado
self.seguindo  = {}   # dígrafo
self.pesos     = {}   # peso das arestas de amizade
```

Essa escolha foi feita porque:
- Consulta e inserção de vizinhos em O(1) médio (graças ao `set`).
- Uso eficiente de memória para grafos esparsos (poucos relacionamentos por usuário), como é o caso real de redes sociais.
- Representação natural tanto para grafos direcionados quanto não-direcionados, bastando popular a aresta em um ou dois sentidos.

## Conceitos de Grafos Aplicados

| Conceito | Onde aparece no código |
|---|---|
| **Dígrafo** | `self.seguindo`, populado por `adicionar_seguidor()` |
| **Grafo não-direcionado** | `self.amizades`, populado por `adicionar_amizade()` (aresta adicionada nos dois sentidos) |
| **Caminho** | `grau_de_separacao()` (BFS) e `caminho_mais_proximo()` (Dijkstra) |
| **Conexidade** | `componentes_conexos()` e `eh_conexo()` |
| **Circuito (ciclo)** | `existe_circuito()`, detectado no dígrafo de seguidores |
| **Grau de entrada (in-degree)** | `usuarios_mais_influentes()` |

## Algoritmos Implementados

### 1. BFS — Busca em Largura (`grau_de_separacao`)
Encontra o **caminho mais curto em número de arestas** entre dois usuários, explorando o grafo "camada por camada" com auxílio de uma fila (`deque`). Aplicação real: cálculo de graus de separação, como no antigo recurso do LinkedIn/Facebook.

### 2. DFS — Busca em Profundidade
Utilizada em duas situações distintas:

- **Componentes conexos** (`_dfs_visita`, `componentes_conexos`, `eh_conexo`): percorre o grafo o mais fundo possível a partir de um vértice, marcando tudo que é alcançável. Repetindo esse processo para vértices ainda não visitados, identifica-se cada "ilha" isolada da rede (comunidades desconectadas).
- **Detecção de circuito no dígrafo** (`existe_circuito`): usa a técnica de coloração de vértices (BRANCO/CINZA/PRETO). Se durante a recursão um vértice **CINZA** é revisitado, significa que ele ainda está na pilha de recursão atual, caracterizando uma aresta de retorno — ou seja, um ciclo.

### 3. Dijkstra (`caminho_mais_proximo`)
Encontra o caminho de **menor custo acumulado** entre dois usuários em um grafo ponderado, usando fila de prioridade (`heapq`).

Detalhe de modelagem: o custo de cada aresta é `1 / peso`, invertendo a lógica do peso bruto — quanto **maior** a força de interação entre dois usuários, **menor** o custo da aresta. Isso faz o algoritmo priorizar caminhos que passam por conexões mais fortes, simulando um "caminho de maior afinidade" em vez de menor distância física.

### 4. Contagem de grau de entrada (`usuarios_mais_influentes`)
Não é um algoritmo de busca em grafo propriamente dito, mas uma métrica derivada diretamente da estrutura do dígrafo: conta quantas vezes cada usuário aparece como "seguido", equivalente ao **grau de entrada (in-degree)** de cada vértice. Serve de base para métricas reais de influência, como as usadas em algoritmos de ranking do Twitter/X e LinkedIn.

## Como Executar

Requisitos: Python 3 (nenhuma dependência externa).

```bash
python nome_do_arquivo.py
```

A execução roda uma demonstração completa (`if __name__ == "__main__":`) que:
1. Constrói o grafo de amizades e o dígrafo de seguidores.
2. Imprime a lista de adjacência de ambos.
3. Executa BFS, DFS (conexidade e circuito) e Dijkstra sobre os dados de exemplo.
4. Lista os usuários mais influentes.

## Exemplo de Uso

```python
rede = RedeSocial()

rede.adicionar_amizade("Ana", "Bruno", peso=5)
rede.adicionar_amizade("Bruno", "Carla", peso=2)
rede.adicionar_seguidor("Ana", "Bruno")

caminho = rede.grau_de_separacao("Ana", "Carla")
# ['Ana', 'Bruno', 'Carla']

print(rede.eh_conexo())
# True ou False, dependendo do restante do grafo

print(rede.existe_circuito())
# True se houver ciclo no dígrafo de seguidores
```

## Referências

- **Grafo social do Facebook (Facebook Graph)**: usado internamente pela plataforma para recomendação de amigos, moderação e análise de comunidades.
- **Grafo de seguidores do Twitter/X**: dígrafo assimétrico que define a construção da timeline de cada usuário — mesma lógica implementada em `self.seguindo`.
- **Algoritmos de influência (PageRank e variantes)**: usados por LinkedIn e Twitter/X, baseados em grau de entrada do dígrafo, como em `usuarios_mais_influentes()`.
- **Bancos de dados orientados a grafos** (ex: Neo4j): usam lista de adjacência (ou estruturas equivalentes) para armazenar relações sociais em escala.

---

**Trabalho acadêmico** — Teoria dos Grafos.
Estrutura de dados: Lista de Adjacência.
Conceitos: Dígrafo, Conexidade, Caminho, Circuito.
Algoritmos: BFS, DFS, Dijkstra.
