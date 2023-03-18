from typing import List, Set, FrozenSet, DefaultDict, Dict
from collections import defaultdict
import logging

class Edge(tuple):
    def __new__(cls, u: int, v: int):
        return super(Edge, cls).__new__(cls, [u, v])
    
    def __init__(self, u: int, v: int):
        self.u = u
        self.v = v
        pass

    def adj(self, u: int) -> int:
        if u == self.u:
            return self.v
        elif u == self.v:
            return self.u
        else:
            raise Exception(f"{u} not found in {self}.")

    def __str__(self):
        return f"{self.u} -> {self.v}"