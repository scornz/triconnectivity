class ComponentsInconsistentException(Exception):
    """
    The returned tri-connected components of a graph were inconsistent given
    varying roots of DFS.
    """

    def __init__(self):
        message = f"The returned tri-connected components of a graph were inconsistent given varying roots of DFS."
        super().__init__(message)
