from dataclasses import dataclass
from typing import cast, List, Dict


@dataclass(frozen=True)
class Edge:
    """An immutable undirected edge, containing u and v. Can be a self-loop
    (as in, u and v are the same vertex)."""

    u: int
    v: int

    # An identifier for the edge itself, used for seperating parallel edges
    uid: int = -1
    # Is this edge a tree edge
    tree: bool = False

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


class MutableEdge:
    """A mutable directed edge."""

    u: int
    v: int

    # An identifier for the edge itself, used for seperating parallel edges
    uid: int = -1
    # Is this edge a tree edge
    tree: bool = False

    def __init__(self, u: int, v: int, uid: int):
        self.u = u
        self.v = v
        self.uid = uid

    def __eq__(self, __o: object):
        assert type(__o) is Edge
        obj = cast(Edge, __o)
        return (self.u == obj.u and self.v == obj.v) or (
            self.u == obj.v and self.v == obj.u
        )

    def __contains__(self, u: int) -> bool:
        return u == self.u or u == self.v

    def adj(self, u: int) -> int:
        if u == self.u:
            return self.v
        elif u == self.v:
            return self.u
        else:
            raise Exception(f"{u} not found in {self}.")

    def __str__(self):
        return f"{self.u} -- {self.v}"

    def mark(self):
        self.tree = True

    def redirect(self, x: int, y: int):
        """Take the x end of this edge and redirect it to y."""
        if x == self.u:
            self.u = y
        elif x == self.v:
            self.v = y
        else:
            raise Exception(f"{x} not found in {self}.")

    def freeze(self):
        return Edge(self.u, self.v, self.uid, self.tree)


class Component(frozenset):
    def __repr__(self):
        return "{" + ",".join(str(x) for x in self) + "}"

    def __str__(self):
        return self.__repr__()


def print_progress_bar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
