from .base import ThreeEdgeConnectBase
from typing import List, Set, Dict
from utils import MutableEdge, print_progress_bar


class ThreeEdgeConnectIterative(ThreeEdgeConnectBase):
    """A fully iterative implementation into Tsin's simple 3-edge-connectivity
    algorithm. It introduces some necessary modifications in order to support
    large datasets."""

    def __init__(self, root: int, g: Dict[int, List[int]], progress_bar=False):
        # Whether or not to show progress bar
        self.progress_bar = progress_bar
        # Init main graph
        super().__init__(root, g)

    def _absorb(self, u: int, v: int, eject: bool = False):
        """Absorb v into u."""
        assert u != v
        self.edge_graph[u].update(self.edge_graph[v])

        # A list of edges that were changed to become self-loops
        self_loops: Set[MutableEdge] = set()
        for edge in self.edge_graph[v]:
            # Redirect all of the edges
            edge.redirect(v, u)
            if edge.v == edge.u:
                self_loops.add(edge)

        # Remove immediate self-loops from
        self.edge_graph[u].difference_update(self_loops)
        if not eject:
            # (v) is absorbed into (u), so it is no longer needed in the edge_graph
            self.edge_graph.pop(v)
            # Absorb components of original vertex into this one
            self.components[u].update(self.components[v])
            # Get rid of this item, since it has been absorbed by u
            self.components.pop(v)
        else:
            # Degree should be 2 if we are ejecting
            assert len(self.edge_graph[v]) == 2
            # Nothing should be pointed to v at this point,
            # likewise, v should not be connected to anything either
            self.edge_graph[v].clear()

    def _explore(self, u: int):
        # Initialize the stack with the root
        stack = [u]

        # --- USED FOR PROGRESS BAR (if selected) ---------------------------- #
        processed = 0
        length = len(self.graph)
        # Print out a progress bar with how many vertices have been post-visited
        if self.progress_bar:
            print_progress_bar(
                processed, length, prefix="Progress:", suffix="Complete", length=50
            )
        # --------------------------------------- ---------------------------- #

        # The previously visited vertex, the last vertex that was popped on top of u
        prev: int = 0
        while stack:
            # Get the top of the stack
            u = stack[-1]

            # If u has not been visited
            if u not in self.pre:
                # This is the first time we are visiting this vertex
                self.pre[u] = self.time
                self.time += 1

                # Initialize low values and u-path
                # Assign pre-order value
                self.low[u] = self.pre[u]
                self.paths[u] = [u]
            else:
                # We are post visiting u from some vertex, v!
                # (prev) is the item that was just popped, thus the last vertex visited

                v = prev

                # Absorb-eject if the degree of v is only two
                if len(self.edge_graph[v]) == 2:
                    # Connect u to all of v's edges, and EJECT v
                    self._absorb(u, v, eject=True)
                    self.paths[v].remove(v)

                # u is connected to some item earlier in the tree than v
                if self.low[u] <= self.low[v]:
                    # Absorb v-path, prepended by u
                    self._absorb_path([u] + self.paths[v])
                else:
                    # v is connected to some item earlier in the tree that u
                    self.low[u] = self.low[v]
                    # Completely absorb u-path
                    self._absorb_path(self.paths[u])
                    self.paths[u] = [u] + self.paths[v]

            # Was there one edge connected from u to another unexplored vertex, v?
            explored: bool = False
            for edge in self.edge_graph[u].copy():
                # Skip self-loops
                if edge.u == edge.v:
                    continue

                # Get the other end of the edge u --v
                v = edge.adj(u)

                # If this edge points to another vertex that has NOT been visited yet
                if v not in self.pre:
                    # v is unvisited
                    stack.append(v)
                    # Mark this edge as a tree-edge
                    edge.mark()
                    # One has been found, do not push any more vertices to stack
                    explored = True
                    break
                # Only continue if we are looking on a BACK-EDGE
                elif not edge.tree:
                    # u was visited later than v
                    if self.pre[u] > self.pre[v]:
                        # Outgoing back-edge of u
                        if self.pre[v] < self.low[u]:
                            self._absorb_path(self.paths[u])
                            self.low[u] = self.pre[v]
                            self.paths[u] = [u]
                    # u was visited earlier than v
                    elif self.pre[u] < self.pre[v]:
                        # Incoming back-edge of u
                        if v in self.paths[u]:
                            index = self.paths[u].index(v)
                            self._absorb_path(self.paths[u][: index + 1])
                            self.paths[u] = [u] + self.paths[u][index + 1 :]
                        else:
                            raise Exception(f"Could not find {v} in paths[{u}]")
                    else:
                        raise Exception("pre[u] == pre[v], bad.")

            # If u was only connected to already visited vertices
            if not explored:
                # Pop it from the stack, where it will never be pushed again
                stack.pop()

                # Update progress bar metrics
                processed += 1
                if self.progress_bar:
                    print_progress_bar(
                        processed,
                        length,
                        prefix="Progress:",
                        suffix="Complete",
                        length=50,
                    )

                # Update prev to indicate this was the last visited vertex
                prev = u
