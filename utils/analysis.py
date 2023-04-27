# Internal
from utils import Component

# Typing
from typing import List

# External
import pickle
from collections import Counter
import numpy as np


def load_pickle(data_path: str) -> List[Component]:
    """Load a saved pickle dataset into a list of components"""

    with open(f"data/processed/{data_path}-components.pkl", "rb") as inp:
        return pickle.load(inp)


def print_stats(components: List[Component]):
    """Given a list of components, print out some statistics about them."""
    num = len(components)
    num_vertices = sum([len(c) for c in components])

    print(f"Number of components: {num}")
    largest_component_size = len(max(components, key=lambda x: len(x)))
    print(f"Largest component size: {largest_component_size}")
    print(f"Average component size: {sum(len(c) for c in components) / num}")
    print(
        f"Average component size (w/o largest component): {sum(len(c) for c in components if len(c) != largest_component_size) / (num - 1)}"
    )

    components_excluding_small = [c for c in components if len(c) > 1]
    print(
        f"Number of components (greater than size 1): {len(components_excluding_small)}"
    )

    print(f"Proportion: {largest_component_size / num_vertices}")
    print(
        f"Proportion (core): {largest_component_size / sum([len(c) for c in components_excluding_small])}"
    )

    # fig, ax = plt.subplots()

    # # plt.plot(x1, y1)

    # all_component_sizes = [len(c) for c in components]
    # counted_sizes = np.array(list(Counter(all_component_sizes).items()))

    # # Sort such that component size is increasing
    # counted_sizes = counted_sizes[counted_sizes[:, 0].argsort()]
    # counted_sizes = counted_sizes[counted_sizes[:, 1] > 1, :]
    # print(counted_sizes[:, 0])
    # ax.set_yscale("log")
    # ax.plot(counted_sizes[:, 0], counted_sizes[:, 1], color="orange")
    # ax.set_ylabel("# of components")
    # ax.set_xlabel("Component size (# of vertices)")
    # fig.show()
    # fig.show()
    # plt.show()
    # sorted_counted_sizes = sorted(counted_sizes.items())
    # plt.bar(counted_sizes.keys(), counted_sizes.values())
    # plt.show()
