from triedgeconnect import traverse

# Not tri-connected, at all, three different components
simple = {
    1: [2, 3],
    2: [1, 3],
    3: [1, 2]
}

# Tri-connected, should be single component
simple2 = {
    1: [2, 3, 4],
    2: [1, 3, 4],
    3: [1, 2, 4],
    4: [1, 2, 3]
}

# Same as simple2, except now there's a 5th node that is only biconnected
simple3 = {
    1: [2, 3, 4, 5],
    2: [1, 3, 4],
    3: [1, 2, 4],
    4: [1, 2, 3, 5],
    5: [1, 4]
}

graph = {
    1: [2, 3, 4, 6],
    2: [1, 4, 3],
    3: [2, 1, 4],
    4: [1, 2, 3, 5],
    5: [4, 6, 7, 8],
    6: [1, 5, 7, 8],
    7: [6, 5, 8],
    8: [5, 6, 7]
}
print(traverse(4, graph))