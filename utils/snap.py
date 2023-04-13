from collections import defaultdict
from typing import DefaultDict, List


def load_snap_dataset(file: str, node_limit=None):
    graph: DefaultDict[int, List[int]] = defaultdict(list)

    with open(file, "r") as f:
        processed = 0
        for line in f.readlines():
            if line[0] == "#":
                continue

            edge = line.strip().split("\t")
            from_vertex = int(edge[0])
            to_vertex = int(edge[1])

            if node_limit and (from_vertex >= node_limit or to_vertex >= node_limit):
                continue

            graph[from_vertex].append(to_vertex)
            processed += 1

    return graph
