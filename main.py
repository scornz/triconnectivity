import logging
from triconnect.edge.iterative import ThreeEdgeConnectIterative
from triconnect.edge.recursive import ThreeEdgeConnectRecursive
from utils.snap import run_and_save
from utils.analysis import load_pickle, print_stats

from utils.testing import test_consistency


# --- EXAMPLES --------------------------------------------------------------- #

# Not tri-connected, at all, three different components
simple = {1: [2, 3], 2: [1, 3], 3: [1, 2]}

# Tri-connected, should be single component
simple2 = {1: [2, 3, 4], 2: [1, 3, 4], 3: [1, 2, 4], 4: [1, 2, 3]}

# Same as simple2, except now there's a 5th node that is only biconnected
simple3 = {1: [2, 3, 4, 5], 2: [1, 3, 4], 3: [1, 2, 4], 4: [1, 2, 3, 5], 5: [1, 4]}

graph = {
    1: [2, 3, 4, 6],
    2: [1, 4, 3],
    3: [2, 1, 4],
    4: [1, 2, 3, 5],
    5: [4, 6, 7, 8],
    6: [1, 5, 7, 8],
    7: [6, 5, 8],
    8: [5, 6, 7],
}

paper_example = {
    1: [2, 10, 10],
    2: [8, 3, 1],
    3: [2, 4, 5],
    4: [3, 6, 6],
    5: [3, 6, 7, 6],
    6: [5, 5, 4, 4],
    7: [12, 8, 17, 11, 17, 5],
    8: [9, 7, 2],
    9: [10, 8],
    10: [1, 9, 1],
    11: [17, 7, 12],
    12: [11, 7, 13, 16],
    13: [16, 12, 15, 14],
    14: [16, 13, 15],
    15: [14, 16, 13],
    16: [12, 15, 14, 13],
    17: [7, 11, 7],
}

nsfnet = {
    1: [2, 3, 6],
    2: [1, 3, 4],
    3: [1, 2, 9],
    4: [2, 5, 7, 14],
    5: [4, 10],
    6: [1, 7, 11],
    7: [4, 6, 8],
    8: [7, 9],
    9: [3, 8, 10],
    10: [5, 9, 12, 13],
    11: [6, 12, 13],
    12: [10, 11, 14],
    13: [11, 10, 14],
    14: [4, 12, 13],
}

gbn = {
    0: [8, 2],
    1: [2, 3, 4],
    2: [0, 1, 4],
    3: [9, 4, 1],
    4: [1, 2, 3, 8, 9, 10],
    5: [6, 8],
    6: [5, 7],
    7: [8, 6, 10],
    8: [4, 0, 5, 7],
    9: [4, 3, 12, 10],
    10: [4, 7, 9, 11, 12],
    11: [10, 13],
    12: [9, 10, 14, 16],
    13: [14, 11],
    14: [12, 15, 13],
    15: [14, 16],
    16: [15, 12],
}

geant2 = {
    0: [1, 2],
    1: [3, 0, 9, 6],
    2: [0, 3, 4],
    3: [2, 1, 6, 5],
    4: [2, 7],
    5: [3, 8],
    6: [3, 1, 9, 8],
    7: [4, 8, 11],
    8: [20, 11, 7, 5, 6, 12, 18, 17],
    9: [6, 1, 10, 13, 12],
    10: [9, 13],
    11: [7, 8, 20, 14],
    12: [9, 13, 19, 21, 8],
    13: [10, 9, 12],
    14: [11, 15],
    15: [14, 16],
    16: [15, 17],
    17: [16, 8, 18],
    18: [17, 8, 21],
    19: [12, 23],
    20: [11, 8],
    21: [18, 12, 22],
    22: [21, 23],
    23: [19, 22],
}


def test_examples():
    """Run test_consistency on all examples"""
    test_consistency(simple)
    test_consistency(simple2)
    test_consistency(simple3)
    test_consistency(graph)
    test_consistency(paper_example)
    test_consistency(nsfnet)
    test_consistency(gbn)
    test_consistency(geant2)


# ---------------------------------------------------------------------------- #

logging.basicConfig(level=logging.INFO)
run_and_save("as-skitter.txt", directed=True)
# print_stats(load_pickle("roadNet-PA.txt"))

# test_examples()
# print(ThreeEdgeConnectIterative(5, simple3).get())
