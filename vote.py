"""
This program will create a Maximum Spanning Tree connecting each of the eyes based on the clusterings given.
It then prunes the weakest connections until the eyes are all in their final calculated clusters.
The eyes are moved into folders with arbitrary numbers that represent that cluster.
"""
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
# Gather each of the clusterings provided
for file in os.listdir(src):
    if(file.endswith('_vga_sym_XBSym_mod')):
        cluster_files.append(file)

# A Buddyship indicates if a pair of eyes are in the same clique (i.e. cluster)
num_buddys = len(os.listdir(dest))
num_cliques = len(cluster_files)

# 3D boolean table
buddyships = np.zeros((num_cliques, num_buddys, num_buddys))

np.set_printoptions(threshold=sys.maxsize)

# Read each of the cluster files and place them into cliques. A clique is one of the clusters in the clustering group.

for f_index in range(num_cliques):
    clique_file = open(cluster_files[f_index], 'r')
    lines = clique_file.readlines()
    lines.pop(0)

    clique_nums = []
    
    # Find out which clique this eye is in and place it in a list
    for line in lines:
        line = line.strip().split('   ')

        clique_val = line[len(line) - 1]

        if(clique_val.isdecimal()):
            clique_nums.append(clique_val)

    # Buddyships will contain a 1 if the two eyes being compared are in a clique together and 0 otherwise
    for y_buddy in range(num_buddys):
        for x_buddy in range(y_buddy, num_buddys):
            if(clique_nums[y_buddy] == clique_nums[x_buddy]):
                buddyships[f_index][y_buddy][x_buddy] = 1

flat = []

# Flatten the 3D matrix into a 2D one by summing up the z-entries
for y in range(len(buddyships[0])):
    temp = np.zeros(len(buddyships[0]))
    for x in range(len(buddyships)):
        temp += buddyships[x][y]
    temp = list(temp)
    flat.append(temp)


# Make a graph showing all the points in space

graph = {
    'vertices': [x for x in range(num_buddys)],
    'edges': set([])
}

for y in range(num_buddys):
    for x in range(y, num_buddys):
        if(flat[y][x] > 0):
            graph['edges'].add((flat[y][x], y, x))

# Apply Kruskal's algorithm for a Max Spanning Tree
mst = mk.kruskal(graph)

# Do k-pruning
s_mst = []
for l in range(len(mst)):
    if(l > len(mst)):
        break
    (w, x, y) = mst[l]
    
    # weight is being hard coded but this gives the desired output for now.
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

# # This code when uncommented will show the graph formed

# G = nx.read_edgelist("./s_mst.txt", delimiter=',', data=[('weight', float)])
# G.edges(data=True)

# edge_labels = dict(((u, v), d['weight']) for u, v, d in G.edges(data=True))
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True)
# nx.draw_networkx_edges(G, pos, edge_color='b')

# plt.show()


# Sort the points by their parent in the edge-graph
s_mst.sort(key=lambda y: y[1])

out_pts = []
in_pts = []
for x in range(len(s_mst)):
    _, p_out, p_in = s_mst[x]
    out_pts.append(p_out)
    in_pts.append(p_in)

G = connection.Graph(num_buddys)
for x in range(len(out_pts)):
    G.addEdge(out_pts[x], in_pts[x])

# Get all points that are connected to each other    
cc = G.connectedComponents()

clusters = []
for x in range(num_buddys):
    for y in range(len(cc)):
        if x in cc[y]:
            clusters.append(y)

# Move files to their final cluster
source = './all/'
files = os.listdir(source)

for file in files:
    cluster_val = clusters.pop(0) + 1
    if not os.path.exists(source):
        os.makedirs(f"{cluster_num}")
    dest = f'./{cluster_val}/'
    shutil.move(source+file, dest)
