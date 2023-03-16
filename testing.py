from triedgeconnect import traverse

simple = {
    1: [2, 3],
    2: [1, 3],
    3: [1, 2]
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
print(traverse(1, simple))