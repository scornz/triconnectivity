from typing import List, Set, FrozenSet, DefaultDict, Dict
from collections import defaultdict
from utils import Component, Edge
import logging


def traverse(root: int, g: Dict[int, List[int]]) -> List[Component]:
    graph: Dict[int, List[int]] = dict()
    # Embodiments of all edges
    embodiments: Dict[Edge, Edge] = dict()

    # Make a defensive copy of the original graph
    for u, connected in g.items():
        graph[u] = connected.copy()
        for v in connected:
            embodiments[Edge(u, v)] = Edge(u, v)

    # Initialize each component to be 1 vertex (itself)
    components: Dict[int, Set[int]] = dict()
    for u in graph:
        components[u] = set([u])

    time = 1
    # Preordering of graph (order encountered in dfs)
    pre: DefaultDict[int, int] = defaultdict(int)  # Dict[vertex, preorder num]
    parents: Dict[int, int] = dict()  # Dict[vertex, parent]
    low: Dict[int, int] = dict()
    paths: Dict[int, List[int]] = dict()
    tree: Set[Edge] = set()

    def degree(u: int) -> int:
        connected = graph[u]
        actual = set()
        for v in connected:
            actual.add(embodiments[Edge(u, v)].adj(u))

        if u in actual:
            actual.remove(u)
        return len(actual)

    def dfs(u: int, p: int = -1):
        logging.debug(f"VISITING: {u}")
        nonlocal time
        # Assign pre-order value
        pre[u] = time
        time += 1
        # Assign parent
        parents[u] = p

        # Initialize low values and w-path
        low[u] = pre[u]
        paths[u] = [u]

        for v in graph[u].copy():
            v = embodiments[Edge(u, v)].adj(u)
            if u == v:
                continue

            if v not in graph[u]:
                logging.error("The graph was constructed incorrectly.")

            edge = Edge(u, v)

            if v not in pre:
                tree.add(edge)
                # v is unvisited
                dfs(v, u)
                logging.debug(f"POST-VISITING: {v} (from {u})")
                # If the degree of v is two
                # print(degree())
                if len(graph[v]) == 2:
                    # Connect u to all of v's edges, and EJECT v
                    absorb(u, v, eject=True)
                    paths[v].remove(v)

                if low[u] <= low[v]:
                    logging.debug(f"LOW[U] <= LOW[V]: {[u]} + {paths[v]}")
                    absorb_path([u] + paths[v])
                else:
                    logging.debug(f"LOW[U] > LOW[V]")
                    low[u] = low[v]
                    absorb_path(paths[u])
                    paths[u] = [u] + paths[v]
            else:
                if pre[u] > pre[v]:
                    # Outgoing back-edge of u
                    logging.debug(f"OUTGOING BACK-EDGE: {u} -- {v}")
                    if pre[v] < low[u]:
                        logging.debug(f"OUTGOING BACK-EDGE ABSORB: {paths[u]}")
                        absorb_path(paths[u])
                        low[u] = pre[v]
                        paths[u] = [u]
                elif pre[u] < pre[v]:
                    # Incoming back-edge of u
                    logging.debug(f"INCOMING BACK-EDGE: {u} -- {v} ({paths[u]})")
                    if v in paths[u]:
                        index = paths[u].index(v)
                        absorb_path(paths[u][: index + 1])
                        paths[u] = [u] + paths[u][index + 1 :]
                    else:
                        logging.error(
                            f"INCOMING BACK-EDGE PARTIAL ABSORB: Could not find {v} in paths[u]"
                        )
                else:
                    raise Exception("pre[u] == pre[v], bad.")

    def absorb(u: int, v: int, eject: bool = False):
        """Absorb u into v."""
        assert u != v
        logging.debug(f"ABSORB EDGE: {u} -- {v} (eject: {eject})")
        logging.debug(f"ABSORB EDGE ADD: {graph[u]} + {graph[v]} (eject: {eject})")

        graph[u].extend(graph[v])

        # for edge in embodiments:
        #     if v in edge:
        #         print(f"yes {edge} (adj: {edge.adj(v)}) --> {Edge(edge.adj(v), u)}")
        #         embodiments[edge] = Edge(edge.adj(v), u)

        for x in graph[v]:
            embodiments[Edge(v, x)] = Edge(u, x)

            for uv, xy in embodiments.items():
                if xy == Edge(v, x):
                    embodiments[uv] = Edge(u, x)

            # Replace all mentions of v, with u!
            for _ in range(graph[x].count(v)):
                # embodiments[Edge(x,v)] =
                graph[x].remove(v)
                graph[x].append(u)

        # Remove self-loops
        graph[u] = [x for x in graph[u] if x != u]
        # graph[u].remove(v)
        # print(f"trying to remove {v}")
        # graph[u].remove(v)

        if not eject:
            # print(graph.pop(v))
            components[u].update(components[v])
            # Get rid of this item, since it has been absorbed by u
            components.pop(v)
        else:
            # Degree should be 2 if we are ejecting
            assert len(graph[v]) == 2
            # Nothing should be pointed to v at this point,
            # likewise, v should not be connected to anything either
            graph[v].clear()

        # print(embodiments)

    def absorb_path(p: List[int]):
        """Absorb a path of n vertices into p[0]. Take all edges incident to
        the path p and connect them to p[0], remove self-loops (back-edges from
        vertices in p connecting back to p[0]). In this example, a list of integers,
        means that there are edges connecting p[0] to p[1], p[1] to [2], etc."""
        logging.debug(f"ABSORB PATH: {p}")
        # If p is the null path, just skip this
        # Must contain one edge
        if not p or len(p) < 2:
            return

        origin = p[0]
        for v in p[1:]:
            # Absorb edge u -- v
            absorb(origin, v, eject=False)

    dfs(root, -1)

    res: List[Component] = []
    for c in components.values():
        res.append(Component(c))

    return res
