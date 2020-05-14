parent = dict()
rank = dict()


def make_set(vertex):
    parent[vertex] = vertex
    rank[vertex] = 0


def find(vertex):
    if (parent[vertex] != vertex):
        parent[vertex] = find(parent[vertex])
    return parent[vertex]


def union(vertex_1, vertex_2):
    root_1 = find(vertex_1)
    root_2 = find(vertex_2)

    if root_1 != root_2:
        if rank[root_1] > rank[root_2]:
            parent[root_2] = root_1
        else:
            parent[root_1] = root_2
        if rank[root_1] == rank[root_2]:
            rank[root_2] += 1


def kruskal(graph):
    for vertex in graph['vertices']:
        make_set(vertex)
        max_spanning_tree = set()
        edges = list(graph['edges'])
        edges.sort(reverse=True)
    for edge in edges:
        weight, vertex_1, vertex_2 = edge
        if find(vertex_1) != find(vertex_2):
            union(vertex_1, vertex_2)
            max_spanning_tree.add(edge)

    return sorted(max_spanning_tree, reverse=True)
