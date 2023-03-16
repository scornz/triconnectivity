from typing import List, Set, FrozenSet, DefaultDict, Dict
from collections import defaultdict
import logging

logging.basicConfig(level=logging.DEBUG)

def traverse(root: int, g: Dict[int, List[int]]):
    graph:  Dict[int, Set[int]] = dict()
    # Make a defensive copy of the original graph
    for u, connected in g.items():
        graph[u] = set(connected)

    # Initialize each component to be 1 vertex (itself)
    components: Dict[int, Set[int]] = dict()
    for u in graph:
        components[u] = set([u])

    time = 1
    # Preordering of graph (order encountered in dfs)
    pre: DefaultDict[int, int] = defaultdict(int) # Dict[vertex, preorder num]
    parents: Dict[int, int] = dict() # Dict[vertex, parent]
    low: Dict[int, int] = dict()
    paths: Dict[int, List[int]] = dict()
    tree: Set[FrozenSet[int]] = set()

    def dfs(u: int, p: int = -1):
        logging.debug(f"PRE-VISITING: {u}")
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
            if v not in graph[u]:
                continue

            edge = frozenset([u,v])

            if v not in pre:
                tree.add(edge)
                # v is unvisited
                dfs(v, u)
                logging.debug(f"POST-VISITING: {u}")
                # If the degree of v is two
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
            elif edge not in tree:
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
                    logging.debug(f"INCOMING BACK-EDGE: {u} -- {v}")
                    index = paths[u].index(v)
                    absorb_path(paths[u][:index+1])
                    paths[u] = [u] + paths[u][index+1:]
                else:
                    raise Exception("pre[u] == pre[v], bad.")
    

    def absorb(u: int, v: int, eject: bool = False):
        """Absorb u into v."""
        assert u != v
        logging.debug(f"ABSORB EDGE: {u} -- {v} (eject: {eject})")

        graph[u].update(graph[v])
        for x in graph[v]:
            # Replace all mentions of v, with u!
            graph[x].remove(v)
            graph[x].add(u)

        # Remove self-loops
        graph[u].remove(u)
            # graph[u].remove(v)
        # print(f"trying to remove {v}")
        # graph[u].remove(v)

        if not eject:
            graph.pop(v)
            components[u].update(components[v])
            # Get rid of this item, since it has been absorbed by u
            components.pop(v)
        else:
            # Degree should be 2 if we are ejecting
            assert len(graph[v]) == 2
            # Nothing should be pointed to v at this point, 
            # likewise, v should not be connected to anything either
            graph[v].clear()

        print(graph)

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
    return components