""" A modified disjoint set algorithm with path compression, that maintains a 
specific value in the parent upon return from get(). The structure of the tree
is exactly the same as another algorithm, except that union(x,y) sets a special
value on the parent of the newly joined set to be equal to x. This value gets
returned upon a call to get() (whilst _find() returns just the parent()). This
makes it appear that x is the parent of the new set (when it really is not).

Heavily modified from:
https://www.geeksforgeeks.org/union-by-rank-and-path-compression-in-union-find-algorithm/"""

from typing import TypeVar, Generic, Hashable, List, Dict

T = TypeVar("T", bound=Hashable)


class DisjoinSetItem(Generic[T]):
    def __init__(self, value: T, parent: T):
        self.value = value
        self.rank = 0
        self.parent = parent


class Disjoint(Generic[T]):
    def __init__(self, values: List[T]):
        self.items: Dict[T, DisjoinSetItem[T]] = {
            v: DisjoinSetItem(value=v, parent=v) for v in values
        }

    def get(self, item: T) -> T:
        """Get the value that item is represented by (its embodied parent)"""
        return self.items[self._find(item)].value

    def _find(self, item: T) -> T:
        # If we are not the parent
        if self.items[item].parent != item:
            self.items[item].parent = self._find(self.items[item].parent)
        return self.items[item].parent

    def add(self, value: T):
        """Add a new value to the data structure"""

        if value not in self.items:
            self.items[value] = DisjoinSetItem(value=value, parent=value)

    def union(self, u: T, v: T):
        """Union the two sets by u and v. Set the value of the parent of this
        new set to be equal to u (making it look like u is the parent of the
        new set)"""

        self.add(u)
        self.add(v)

        u_p = self._find(u)
        v_p = self._find(v)

        # The owner of the new set
        owner: T
        if self.items[u_p].rank > self.items[v_p].rank:
            self.items[v_p].parent = u_p
            owner = u_p
        elif self.items[v_p].rank > self.items[u_p].rank:
            self.items[u_p].parent = v_p
            owner = v_p
        else:
            # Increment rank
            self.items[u_p].rank += 1
            # Always set u_p to be the parent in this case
            self.items[v_p].parent = u_p
            owner = u_p

        # Make it seem like u is the parent of the new set
        # NOTE: .value of the parent is only valid at any given time
        self.items[owner].value = u

    def __str__(self):
        items: Dict[T, T] = dict()
        for item in self.items:
            items[item] = self.get(item)

        return str(items)
