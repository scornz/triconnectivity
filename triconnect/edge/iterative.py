from .base import ThreeEdgeConnectBase
from typing import List, Set, Dict
from utils import MutableEdge, print_progress_bar
import logging


class ThreeEdgeConnectIterative(ThreeEdgeConnectBase):
    def __init__(self, root: int, g: Dict[int, List[int]], progress_bar=False):
        # Whether or not to show progress bar
        self.progress_bar = progress_bar
        # Init main graph
        super().__init__(root, g)

    def _absorb(self, u: int, v: int, eject: bool = False):
        """Absorb v into u."""
        assert u != v
        self.edge_graph[u].update(self.edge_graph[v])

        # time1 = datetime.utcnow()
        remove: Set[MutableEdge] = set()
        for edge in self.edge_graph[v]:
            # Redirect all of the edges
            edge.redirect(v, u)
            if edge.v == edge.u:
                remove.add(edge)

        # Remove immediate self-loops
        # self.graph[u] = [x for x in self.graph[u] if x != u]
        self.edge_graph[u].difference_update(remove)
        if not eject:
            self.edge_graph.pop(v)
            self.components[u].update(self.components[v])
            # Get rid of this item, since it has been absorbed by u
            self.components.pop(v)
        else:
            # Degree should be 2 if we are ejecting
            assert len(self.edge_graph[v]) == 2
            # Nothing should be pointed to v at this point,
            # likewise, v should not be connected to anything either
            # self.graph[v].clear()
            self.edge_graph[v].clear()

    def _explore(self, u: int):
        stack = [u]

        processed = 0
        length = len(self.graph)
        # Print out a progress bar with how many vertices have been post-visited
        if self.progress_bar:
            print_progress_bar(
                processed, length, prefix="Progress:", suffix="Complete", length=50
            )

        prev = 0
        while stack:
            u = stack[-1]
            if u not in self.pre:
                # This is the first time we are visiting this node
                self.pre[u] = self.time
                self.time += 1

                # Initialize low values and w-path
                # Assign pre-order value
                self.low[u] = self.pre[u]
                self.paths[u] = [u]
            else:
                v = prev
                # We are post visiting u from some node, v!
                # If the degree of v is two
                if len(self.edge_graph[v]) == 2:
                    # Connect u to all of v's edges, and EJECT v
                    self._absorb(u, v, eject=True)
                    self.paths[v].remove(v)

                if self.low[u] <= self.low[v]:
                    self._absorb_path([u] + self.paths[v])
                else:
                    self.low[u] = self.low[v]
                    self._absorb_path(self.paths[u])
                    self.paths[u] = [u] + self.paths[v]

            one = False
            for edge in self.edge_graph[u].copy():
                # Skip self-loops
                if edge.u == edge.v:
                    continue

                # Get the other end of the edge u --v
                v = edge.adj(u)

                if v not in self.pre:
                    # v is unvisited
                    stack.append(v)
                    edge.mark()
                    one = True
                    break
                elif not edge.tree:
                    if self.pre[u] > self.pre[v]:
                        # Outgoing back-edge of u
                        if self.pre[v] < self.low[u]:
                            self._absorb_path(self.paths[u])
                            self.low[u] = self.pre[v]
                            self.paths[u] = [u]
                    elif self.pre[u] < self.pre[v]:
                        # Incoming back-edge of u
                        if v in self.paths[u]:
                            index = self.paths[u].index(v)
                            self._absorb_path(self.paths[u][: index + 1])
                            self.paths[u] = [u] + self.paths[u][index + 1 :]
                        else:
                            logging.error(
                                f"INCOMING BACK-EDGE PARTIAL ABSORB: Could not find {v} in paths[u]"
                            )
                    else:
                        raise Exception("pre[u] == pre[v], bad.")

            if not one:
                stack.pop()
                processed += 1
                if self.progress_bar:
                    print_progress_bar(
                        processed,
                        length,
                        prefix="Progress:",
                        suffix="Complete",
                        length=50,
                    )

                prev = u
