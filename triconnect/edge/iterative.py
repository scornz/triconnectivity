from .base import ThreeEdgeConnectBase
from typing import List, Set, DefaultDict, Dict, Tuple
from collections import defaultdict
from utils import Edge, print_progress_bar
import logging
from datetime import datetime

from utils.disjoint import Disjoint


class ThreeEdgeConnectIterative(ThreeEdgeConnectBase):
    def __init__(self, root: int, g: Dict[int, List[int]], progress_bar=False):
        # Whether or not to show progress bar
        self.progress_bar = progress_bar
        # Init main graph
        super().__init__(root, g)

    def _absorb(self, u: int, v: int, eject: bool = False):
        """Absorb v into u."""
        assert u != v
        existing = set([edge.uid for edge in self.edge_graph[u]])

        # self.graph[u].extend(self.graph[v])
        self.edge_graph[u].extend(
            [edge for edge in self.edge_graph[v] if edge.uid not in existing]
        )

        for edge in self.edge_graph[v]:
            # Redirect all of the edges
            edge.redirect(v, u)

        # Remove immediate self-loops
        # self.graph[u] = [x for x in self.graph[u] if x != u]
        self.edge_graph[u] = [edge for edge in self.edge_graph[u] if edge.u != edge.v]

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
            logging.debug(f"VISITING: {u}")

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
                logging.debug(f"POST-VISITING: {v} (from {u})")
                # If the degree of v is two
                if len(self.edge_graph[v]) == 2:
                    # Connect u to all of v's edges, and EJECT v
                    self._absorb(u, v, eject=True)
                    self.paths[v].remove(v)

                if self.low[u] <= self.low[v]:
                    logging.debug(f"LOW[U] <= LOW[V]: {[u]} + {self.paths[v]}")
                    self._absorb_path([u] + self.paths[v])
                else:
                    logging.debug(f"LOW[U] > LOW[V]")
                    self.low[u] = self.low[v]
                    self._absorb_path(self.paths[u])
                    self.paths[u] = [u] + self.paths[v]

            one = False
            # time1 = datetime.utcnow()
            # explored = set()
            for edge in self.edge_graph[u]:
                # Get the embodiment of the edge u -- v
                v = edge.adj(u)
                # Skip self-loops
                # v = self.embodiments.get(Edge(u, v)).adj(u)

                if u == v:
                    continue

                # if v not in self.graph[u]:
                #     logging.error(
                #         f"v ({v}) was not found in graph[{u}] ({self.graph[u]}), the graph was constructed incorrectly."
                #     )

                if v not in self.pre:
                    # v is unvisited
                    stack.append(v)
                    edge.mark()
                    one = True
                    break
                elif not edge.tree:
                    if self.pre[u] > self.pre[v]:
                        # Outgoing back-edge of u
                        logging.debug(f"OUTGOING BACK-EDGE: {u} -- {v}")
                        if self.pre[v] < self.low[u]:
                            logging.debug(f"OUTGOING BACK-EDGE ABSORB: {self.paths[u]}")
                            self._absorb_path(self.paths[u])
                            self.low[u] = self.pre[v]
                            self.paths[u] = [u]
                    elif self.pre[u] < self.pre[v]:
                        # Incoming back-edge of u
                        logging.debug(
                            f"INCOMING BACK-EDGE: {u} -- {v} ({self.paths[u]})"
                        )
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

            # time2 = datetime.utcnow()
            # print(f"{time2 - time1} + {len(explored)} + {len(self.edge_graph[u])}")

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
