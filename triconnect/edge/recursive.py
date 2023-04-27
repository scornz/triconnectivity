from utils import Edge
from .base import ThreeEdgeConnectBase
import logging


class ThreeEdgeConnectRecursive(ThreeEdgeConnectBase):
    """A direct, recursive implementation based on Tsin's simple 3-edge-connectivity
    algorithm. Includes significantly more debugging lines compared to its iterative
    counterpart, as performance is not much of a concern in this implementation since
    it's already so limited by the size of the recursive stack."""

    def _absorb(self, u: int, v: int, eject: bool = False):
        """Absorb v into u."""
        assert u != v

        self.graph[u].extend(self.graph[v])
        for x in set(self.graph[v]):
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

    def _explore(self, u: int):
        logging.debug(f"VISITING: {u}")
        # Assign pre-order value
        self.pre[u] = self.time
        self.time += 1

        # Initialize low values and w-path
        self.low[u] = self.pre[u]
        self.paths[u] = [u]

        for edge in self.edge_graph[u]:
            v = edge.adj(u)
            # Get the embodiment of the edge u -- v
            v = self.embodiments.get(edge.freeze()).adj(u)

            # Skip self-loops
            if u == v:
                continue

            if v not in self.graph[u]:
                logging.error(
                    f"v ({v}) was not found in edge_graph[u] ({self.graph[u]}), the edge_graph was constructed incorrectly."
                )

            if v not in self.pre:
                edge.mark()
                # v is unvisited
                self._explore(v)
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
                    logging.debug(f"INCOMING BACK-EDGE: {u} -- {v} ({self.paths[u]})")
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
