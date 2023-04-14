# Internal
from utils import Component

# Typing
from typing import List

# External
import pickle


def load_pickle(data_path: str) -> List[Component]:
    """Load a saved pickle dataset into a list of components"""

    with open(f"{data_path}.pkl", "rb") as inp:
        return pickle.load(inp)


def print_stats(components: List[Component]):
    """Given a list of components, print out some statistics about them."""
    print(f"Number of components: {len(components)}")
