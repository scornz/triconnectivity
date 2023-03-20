from triconnect.edge import get_three_edge_connected_components
from utils import verify_graph

from typing import Dict, List

import logging

from utils.exceptions import ComponentsInconsistentException


def test_consistency(graph: Dict[int, List[int]]):
    """Test the consistency of the algorithm on the given input. For every possible
    root, compare the returned components against one another. NOTE: This does
    not necessarily test for correctness, but consistent responses no matter the
    initialization of the function."""

    # Verify that the graph is undirected
    verify_graph(graph)

    # Get the list of possible roots
    vertices = [k for k in graph]
    # Initial set of components to compare against
    components = set(get_three_edge_connected_components(vertices[0], graph))

    # Run the algorithm for every other set of vertices
    for i in range(1, len(vertices)):
        v = vertices[i]
        test_components = get_three_edge_connected_components(v, graph)
        count = 0

        # Compare returned components against the intial set
        for c in test_components:
            if frozenset(c) not in components:
                raise ComponentsInconsistentException()

            count += 1

        # Make sure the count of components is the exact same
        if count != len(components):
            raise ComponentsInconsistentException()

    # Success! Print out the components that were returned
    logging.info(
        f"Graph was consistent for all root inputs. The components are: {components}"
    )


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
# ---------------------------------------------------------------------------- #

logging.basicConfig(level=logging.INFO)
test_consistency(simple)
test_consistency(simple2)
test_consistency(simple3)
test_consistency(graph)
test_consistency(paper_example)
