# Implementations
from triconnect.edge.iterative import ThreeEdgeConnectIterative

# External
import logging
import pickle
from collections import defaultdict
from datetime import datetime

# Internal functions
from .analysis import print_stats
from .testing import verify_graph

# Typing
from typing import DefaultDict, List


def load_snap_dataset(file: str, directed=False, vertex_limit=None):
    """Given a file path, load the given file into a dictionary. If node_limit
    is filled in, then do not consider edges with a vertex number higher than
    this."""

    graph: DefaultDict[int, List[int]] = defaultdict(list)

    # Open file and load into undirected graph
    with open(f"data/{file}", "r") as f:
        for line in f.readlines():
            # Ignore lines that are commented out
            if line[0] == "#":
                continue

            edge = line.strip().split("\t")
            from_vertex = int(edge[0])
            to_vertex = int(edge[1])
            # print(f"{from_vertex} -- {to_vertex}")

            # Check for vertex limit if it is necessary
            if vertex_limit and (
                from_vertex >= vertex_limit or to_vertex >= vertex_limit
            ):
                continue

            # Append this to the graph
            graph[from_vertex].append(to_vertex)

    # If it is a directed graph
    if directed:
        for u in graph.copy().keys():
            connected = graph[u]
            for v in connected:
                if u not in graph[v]:
                    graph[v].append(u)

    verify_graph(graph)
    return graph


def run_and_save(data_path: str, directed: bool = False):
    """Using a SNAP file, run the iterative version of the algorithm, and save
    the results to a .pkl file for later use."""

    # Load dataset from SNAP format
    logging.info(f"Loading {data_path} into dictionary.")
    snap = load_snap_dataset(data_path, directed)
    logging.info(f"Finished loading {data_path} into dictionary.")

    # Just let the root be the first vertex listed
    root = list(snap.keys())[0]

    # Run the algorithm
    logging.info(
        f"Conducting iterative triconnectivity algorithm on {data_path} with {len(snap)} vertices."
    )
    start_time = datetime.utcnow()
    components = ThreeEdgeConnectIterative(root, snap).get()
    end_time = datetime.utcnow()
    logging.info(
        f"Finished in {end_time - start_time}. Saving results to {data_path}.pkl."
    )

    # Open file to save results to
    with open(f"data/processed/{data_path}-components.pkl", "wb") as outp:
        # Dump to file
        pickle.dump(components, outp, pickle.HIGHEST_PROTOCOL)

    logging.info(f"Saved and complete. Displaying stats.")
    print_stats(components)
