from .base import ThreeEdgeConnectBase
from typing import List, Set, DefaultDict, Dict, Tuple
from collections import defaultdict
from utils import Edge, print_progress_bar
import logging

from utils.disjoint import Disjoint


class ThreeEdgeConnectIterative(ThreeEdgeConnectBase):
    def _explore(self, u: int):
        stack = [u]
        explored_back = set()

        processed = 0
        length = len(self.graph)
        # Print out a progress bar with how many vertices have been post-visited
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
                v = self.embodiments.get(Edge(u, prev)).adj(u)
                # We are post visiting u from some node, v!
                logging.debug(f"POST-VISITING: {v} (from {u})")
                # If the degree of v is two
                if len(self.graph[v]) == 2:
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
            for edge in self.edge_graph[u]:
                # Get the embodiment of the edge u -- v
                v = edge.adj(u)
                # Skip self-loops
                v = self.embodiments.get(Edge(u, v)).adj(u)

                if u == v:
                    continue

                if v not in self.graph[u]:
                    logging.error(
                        f"v ({v}) was not found in graph[u] ({self.graph[u]}), the graph was constructed incorrectly."
                    )

                if v not in self.pre:
                    # v is unvisited
                    stack.append(v)
                    edge.mark()
                    one = True
                    break
                elif not edge.tree:
                    if (edge.uid, u) in explored_back:
                        logging.debug(f"SKIPPING BACK-EDGE: {u} -- {v}")
                        continue

                    explored_back.add((edge.uid, u))
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

            if not one:
                stack.pop()
                processed += 1
                print_progress_bar(
                    processed, length, prefix="Progress:", suffix="Complete", length=50
                )

                prev = u
