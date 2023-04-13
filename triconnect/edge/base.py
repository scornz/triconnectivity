from typing import List, Set, FrozenSet, DefaultDict, Dict
from collections import defaultdict
from utils import Component, Edge
import logging

from utils.disjoint import Disjoint


class ThreeEdgeConnectBase:
    # Graph to modify (key is vertex, value is list of adjacent vertices)
    graph: Dict[int, List[int]]
    # Make an edge graph, where the key is a vertex, and the value is a set of
    # edges that are objects and have unique identifiers
    edge_graph: Dict[int, List[Edge]]
    # A disjoint-set-union object where the key is an edge in edges, and the value
    # is the embodiment of that edge
    # An embodiment is simply the representation of an edge after some merges
    # happen to its incident vertices
    embodiments: Disjoint[Edge]
    # Initialize each component to be 1 vertex (itself)
    components: Dict[int, Set[int]]

    def __init__(self, root: int, g: Dict[int, List[int]]):
        # Temporary graph solely for constructing edge_graph
        temp: Dict[int, List[int]] = dict()

        self.graph = dict()
        # Set of all edges in the entire graph
        edges: Set[Edge] = set()
        for u, connected in g.items():
            # Copy over all vertices
            temp[u] = connected.copy()
            self.graph[u] = connected.copy()
            # Add an edge to the set of edges for each
            for v in connected:
                edges.add(Edge(u, v))

        # Make an edge graph, where the key is a vertex, and the value is a set of
        # edges that are objects and have unique identifiers
        self.edge_graph = defaultdict(list)
        for i, (u, adj) in enumerate(temp.items()):
            for v in adj:
                edge = Edge(u, v, i)
                self.edge_graph[u].append(edge)
                self.edge_graph[v].append(edge)
                temp[v].remove(u)

        # A disjoint-set-union object where the key is an edge in edges, and the value
        # is the embodiment of that edge
        # An embodiment is simply the representation of an edge after some merges
        # happen to its incident vertices
        self.embodiments = Disjoint(list(edges))

        # Initialize each component to be 1 vertex (itself)
        self.components = dict()
        for u in self.edge_graph:
            self.components[u] = set([u])

        self.time = 1
        # Preordering of edge_graph (order encountered in dfs)
        self.pre = defaultdict(int)
        # Key is a vertex, value is lowest pre-order value reachable via tree-edges and one back-edge
        self.low = dict()
        # Key is a vertex, and the value is the "w-path" as defined in the paper
        self.paths = dict()

        self._explore(root)

    def get(self):
        # Convert to components
        res: List[Component] = []
        for c in self.components.values():
            res.append(Component(c))

        return res

    time: int
    # Preordering of edge_graph (order encountered in dfs)
    pre: DefaultDict[int, int]
    # Key is a vertex, value is lowest pre-order value reachable via tree-edges and one back-edge
    low: Dict[int, int]
    # Key is a vertex, and the value is the "w-path" as defined in the paper
    paths: Dict[int, List[int]]

    def _explore(self, u: int):
        raise NotImplementedError()

    def _absorb(self, u: int, v: int, eject: bool = False):
        """Absorb v into u."""
        assert u != v

        self.graph[u].extend(self.graph[v])
        for x in self.graph[v]:
            # Let u -- x embody v -- x
            self.embodiments.union(Edge(u, x), Edge(v, x))

            # Replace all mentions of v, with u!
            for _ in range(self.graph[x].count(v)):
                self.graph[x].remove(v)
                self.graph[x].append(u)

        # Remove immediate self-loops
        self.graph[u] = [x for x in self.graph[u] if x != u]

        if not eject:
            self.graph.pop(v)
            self.components[u].update(self.components[v])
            # Get rid of this item, since it has been absorbed by u
            self.components.pop(v)
        else:
            # Degree should be 2 if we are ejecting
            assert len(self.graph[v]) == 2
            # Nothing should be pointed to v at this point,
            # likewise, v should not be connected to anything either
            self.graph[v].clear()

    def _absorb_path(self, p: List[int]):
        """Absorb a path of n vertices into p[0]. Take all edges incident to
        the path p and connect them to p[0], remove self-loops (back-edges from
        vertices in p connecting back to p[0]). In this example, a list of integers,
        means that there are edges connecting p[0] to p[1], p[1] to [2], etc."""
        # If p is the null path, just skip this
        # Must contain one edge
        if not p or len(p) < 2:
            return

        origin = p[0]
        for v in p[1:]:
            # Absorb edge u -- v
            self._absorb(origin, v, eject=False)
