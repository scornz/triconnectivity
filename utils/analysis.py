# Internal
from utils import Component

# Typing
from typing import List

# External
import pickle


def load_pickle(data_path: str) -> List[Component]:
    """Load a saved pickle dataset into a list of components"""

    with open(f"data/processed/{data_path}-components.pkl", "rb") as inp:
        return pickle.load(inp)


def print_stats(components: List[Component]):
    """Given a list of components, print out some statistics about them."""
    num = len(components)
    print(f"Number of components: {num}")
    largest_component_size = len(max(components, key=lambda x: len(x)))
    print(f"Largest component size: {largest_component_size}")
    print(f"Average component size: {sum(len(c) for c in components) / num}")
    print(
        f"Average component size (w/o largest component): {sum(len(c) for c in components if len(c) != largest_component_size) / (num - 1)}"
    )
