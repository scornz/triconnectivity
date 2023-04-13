from dataclasses import dataclass
from typing import cast, List, Dict


@dataclass(frozen=True)
class Edge:
    """An immutable undirected edge, containing u and v. Can be a self-loop
    (as in, u and v are the same vertex)."""

    u: int
    v: int
    uid: int = 0

    def __eq__(self, __o: object):
        assert type(__o) is Edge
        obj = cast(Edge, __o)
        return (self.u == obj.u and self.v == obj.v) or (
            self.u == obj.v and self.v == obj.u
        )

    def __contains__(self, u: int) -> bool:
        return u == self.u or u == self.v

    def __hash__(self):
        """Simply return the hash of a frozen set"""
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


import sys


class TailRecurseException(Exception):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_call_optimized(g):
    """
    This function decorates a function with tail call
    optimization. It does this by throwing an exception
    if it is it's own grandparent, and catching such
    exceptions to fake the tail call optimization.

    This function fails if the decorated
    function recurses in a non-tail context.
    """

    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs

    func.__doc__ = g.__doc__
    return func
