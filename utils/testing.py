from datetime import datetime
from triconnect.edge.recursive import ThreeEdgeConnectRecursive
from triconnect.edge.iterative import ThreeEdgeConnectIterative

from typing import Dict, List

import logging

# Exceptions
from .exceptions import ComponentsInconsistentException


def test_consistency(graph: Dict[int, List[int]]):
    """Test the consistency of the algorithm on the given input. For every possible
    root, compare the returned components against one another. NOTE: This does
    not necessarily test for correctness, but consistent responses no matter the
    initialization of the function."""

    # Verify that the graph is undirected
    verify_graph(graph)

    # Get the list of possible roots
    vertices = [k for k in graph]
    # Initial set of components to compare against (for recursive and iterative)
    iterative_components = set(ThreeEdgeConnectIterative(vertices[0], graph).get())
    recursive_components = set(ThreeEdgeConnectRecursive(vertices[0], graph).get())
    # Both must have the same amount of components
    if len(iterative_components) != len(recursive_components):
        raise ComponentsInconsistentException()

    count = len(iterative_components)
    # Run the algorithm for every other set of vertices
    for i in range(1, len(vertices)):
        v = vertices[i]
        iterative_test_components = ThreeEdgeConnectIterative(v, graph).get()
        recursive_test_components = ThreeEdgeConnectRecursive(v, graph).get()

        # Compare returned components against the intial set
        for c in iterative_test_components:
            if (
                frozenset(c) not in iterative_components
                or frozenset(c) not in recursive_components
            ):
                raise ComponentsInconsistentException()

        # Compare recursive as well
        for c in recursive_test_components:
            if (
                frozenset(c) not in iterative_components
                or frozenset(c) not in recursive_components
            ):
                raise ComponentsInconsistentException()

        # Make sure the count of components is the exact same
        if (
            len(iterative_test_components) != count
            or len(recursive_test_components) != count
        ):
            raise ComponentsInconsistentException()

    # Success! Print out the components that were returned
    logging.info(
        f"Graph was consistent for all root inputs. The components are: {iterative_components}"
    )


def verify_graph(graph: Dict[int, List[int]]):
    """Takes in an undirected graph, and makes sure every edge has its opposite
    in the graph."""

    for u, adj in graph.items():
        for v in adj:
            if u not in graph[v]:
                raise Exception(
                    f"{u} is adjacent to {v}, but {v} is not adjacent to {u}."
                )
