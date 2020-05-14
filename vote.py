import os
import argparse
import sys
import numpy as np
import shutil
import max_kruskal as mk
import matplotlib.pyplot as plt
import networkx as nx
import connection


src = './'

dest = './all'
cluster_num = 1

# move all images to a single folder if checking a different cluster file
while (cluster_num < sys.maxsize):

    source = f"./{cluster_num}/"
    if not os.path.exists(source):
        break

    files = os.listdir(source)

    for f in files:
        shutil.move(source+f, dest)
    cluster_num = cluster_num + 1


cluster_files = []

for file in os.listdir(src):
    if(file.endswith('_vga_sym_XBSym_mod')):
        cluster_files.append(file)

# A Buddyship indicates if a pair of eyes are in the same clique (i.e. cluster)
num_buddys = len(os.listdir(dest))
num_cliques = len(cluster_files)
buddyships = np.zeros((num_cliques, num_buddys, num_buddys))

np.set_printoptions(threshold=sys.maxsize)

for f_index in range(num_cliques):
    clique_file = open(cluster_files[f_index], 'r')
    lines = clique_file.readlines()
    lines.pop(0)

    clique_nums = []

    for line in lines:
        line = line.strip().split('   ')

        clique_val = line[len(line) - 1]

        if(clique_val.isdecimal()):
            clique_nums.append(clique_val)

    for y_buddy in range(num_buddys):
        for x_buddy in range(y_buddy, num_buddys):
            if(clique_nums[y_buddy] == clique_nums[x_buddy]):
                buddyships[f_index][y_buddy][x_buddy] = 1

flat = []

for y in range(len(buddyships[0])):
    temp = np.zeros(len(buddyships[0]))
    for x in range(len(buddyships)):
        temp += buddyships[x][y]
    temp = list(temp)
    flat.append(temp)


graph = {
    'vertices': [x for x in range(num_buddys)],
    'edges': set([])
}

for y in range(num_buddys):
    for x in range(y, num_buddys):
        if(flat[y][x] > 0):
            graph['edges'].add((flat[y][x], y, x))

mst = mk.kruskal(graph)
s_mst = []
for l in range(len(mst)):
    if(l > len(mst)):
        break
    (w, x, y) = mst[l]
    if (w > 5):
        s_mst.append(mst[l])

filename = 's_mst.txt'
if(os.path.exists(filename)):
    f = open(filename, 'r')
else:
    f = open("s_mst.txt", "a")
    for line in s_mst:
        (w, x, y) = line
        f.write(f"{x},{y},{w}\n")

# G = nx.read_edgelist("./s_mst.txt", delimiter=',', data=[('weight', float)])
# G.edges(data=True)

# edge_labels = dict(((u, v), d['weight']) for u, v, d in G.edges(data=True))
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True)
# nx.draw_networkx_edges(G, pos, edge_color='b')

# plt.show()

s_mst.sort(key=lambda y: y[1])

out_pts = []
in_pts = []
for x in range(len(s_mst)):
    _, p_out, p_in = s_mst[x]
    out_pts.append(p_out)
    in_pts.append(p_in)

# for x in range(num_buddys):
#     while out_pts.count(x) > 1:
#         y = out_pts.index(x)
#         in_pts.pop(y)
#         out_pts.remove(x)

clusters = []
# idea: add every point that connects to this point by checking every point connected to it in in and out pts
# make it be a list where each entry is the connection. If the pt exists in any of the lists found then just ignore


G = connection.Graph(num_buddys)
for x in range(len(out_pts)):
    G.addEdge(out_pts[x], in_pts[x])

cc = G.connectedComponents()

for line in cc:
    print(line)

clusters = []
for x in range(num_buddys):
    for y in range(len(cc)):
        if x in cc[y]:
            clusters.append(y)

source = './all/'
files = os.listdir(source)

for file in files:
    cluster_val = clusters.pop(0) + 1
    if not os.path.exists(source):
        os.makedirs(f"{cluster_num}")
    dest = f'./{cluster_val}/'
    shutil.move(source+file, dest)
