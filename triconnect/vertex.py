"""NOTE: This script is wildly incomplete, but is left here for the possibility
of future work. It is uncommented and does not work, please ignore it."""


from typing import List, Set, FrozenSet, DefaultDict, Dict
from collections import defaultdict
from utils import Component, Edge
import logging
from bidict import bidict


def traverse(graph: Dict[int, List[int]]):
    time = 0
    # Preordering of graph (order encountered in dfs)
    pre: bidict = bidict()

    # Total number of descendants for a given node
    num_descendants: DefaultDict[int, int] = defaultdict(int)  # Dict[node, n]
    flag: DefaultDict[int, bool] = defaultdict(bool)
    parents: Dict[int, int] = dict()  # Dict[node, parent of node]

    low1: DefaultDict[int, int] = defaultdict(int)
    low2: DefaultDict[int, int] = defaultdict(int)

    equal_children: DefaultDict[int, Set[int]] = defaultdict(set)

    # A list of tree edges: u -- v
    tree: Set[Edge] = set()
    non_tree: Set[Edge] = set()

    def dfs(u: int, p: int = -1):
        nonlocal time
        # Assign pre-order value
        time += 1
        pre[u] = time
        # Assign parent
        parents[u] = p
        num_descendants[u] = 1

        u_out = [v for v in graph[u] if pre[u] > pre[v] and Edge(u, v) not in tree]
        u_in = [v for v in graph[u] if pre[u] < pre[v] and Edge(u, v) not in tree]

        # This should always be the case, since this is undirected
        assert u in graph
        for v in graph[u]:
            # If v has NOT been visited yet
            if v not in pre:
                # Add u -- v as a tree edge
                tree.add(Edge(u, v))
                # Explore v, with u labeled as its parent
                dfs(v, u)

                if low1[v] < low1[u]:
                    low2[u] = min(low1[u], low2[v])
                    low1[u] = low1[v]
                    equal_children[u].add(v)
                elif low1[v] == low1[u]:
                    low2[u] = min(low2[u], low2[v])
                else:
                    low2[u] = min(low2[u], low1[v])

                num_descendants[u] += num_descendants[v]
                parents[v] = u
            elif pre[v] < pre[u] and (
                v != p or flag[u]
            ):  # (dfs(w) < dfs(v)) ∧ (w 6= y ∨ flag(v) = false)
                non_tree.add(Edge(u, v))
                if pre[v] < low1[u]:
                    low2[u] = low1[u]
                    low1[u] = pre[v]
                    equal_children[u].add(v)
                elif pre[v] > low1[u]:
                    low2[u] = min(low2[u], pre[v])
            if u == p:
                flag[u] = True

        x: int = bidict.inverse[  # type:ignore
            low1[u]
        ]  # Let x be the node such that low1(u) = dfs(x);
        if x != p and low2[u] >= pre[p]:
            # {x, y} is a seperation pair! uh oh, not triconnected

            pass

        if num_descendants[u] > 1 and any(
            [low1[u] == low1[q] for q in equal_children[u]]
        ):
            new = len(graph)
            # Out(new) = Out(u) --> outgoing back edge
            pre[new] = pre[u]
            low1[new] = low1[u]
            graph[new] = u_out.copy()
            for v in graph[new]:
                graph[v].append(new)

            reduce_vertex(new)

        # Calculate again just in case
        u_out = [v for v in graph[u] if pre[u] > pre[v] and Edge(u, v) not in tree]
        u_in = [v for v in graph[u] if pre[u] < pre[v] and Edge(u, v) not in tree]

        if len(u_out) + len(u_in) > 1:
            reduce_vertex(u)

    def reduce_vertex(u: int):
        pass

    pass
