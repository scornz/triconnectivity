from dataclasses import dataclass
from typing import cast, List, Dict


@dataclass(frozen=True)
class Edge:
    """An undirected edge, pointing from u --> v"""

    u: int
    v: int

    def __eq__(self, __o: object):
        assert type(__o) is Edge
        obj = cast(Edge, __o)
        return (self.u == obj.u and self.v == obj.v) or (
            self.u == obj.v and self.v == obj.u
        )

    def __contains__(self, u: int) -> bool:
        return u == self.u or u == self.v

    def __hash__(self):
        # hash(custom_object)
        return hash(frozenset([self.u, self.v]))

    def adj(self, u: int) -> int:
        if u == self.u:
            return self.v
        elif u == self.v:
            return self.u
        else:
            raise Exception(f"{u} not found in {self}.")

    def __str__(self):
        return f"{self.u} -- {self.v}"


class Component(frozenset):
    def __repr__(self):
        return "{" + ",".join(str(x) for x in self) + "}"

    def __str__(self):
        return self.__repr__()


def verify_graph(graph: Dict[int, List[int]]):
    """Takes in an undirected graph, and makes sure every edge has its opposite
    in the graph."""

    for u, adj in graph.items():
        for v in adj:
            if u not in graph[v]:
                raise Exception(
                    f"{u} is adjacent to {v}, but {v} is not adjacent to {u}."
                )
