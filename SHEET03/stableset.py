import pyscipopt as scip
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# create Graph and read input
adjacency_matrix = np.loadtxt("bayg29_adjacency.txt")
coordinates = np.loadtxt("bayg29_coordinates.txt")
n = adjacency_matrix.shape[0]

graph = nx.Graph()
for i in range(n):  # store nodes with coordinates
    graph.add_node(i, pos=(coordinates[i, 1], coordinates[i, 2]))

for i in range(n):
    for j in range(i + 1, n):
        if adjacency_matrix[i, j] == 1:
            print(f"Add edge {i} -> {j}")
            graph.add_edge(i, j)

# create the SCIP model
model = scip.Model("Stable Set")

# add variables of type 'binary' for each node

# add constraints for each edge

# add objective function

# compute optimum
model.optimize()

# output result
print(
    f"The model status is '{model.getStatus()}', solved after {model.getSolvingTime()} seconds."
)
print("Solution:")
# TODO

print(f"The stable set consists of the following {model.getObjVal()} nodes:")
# TODO

# draw graph with matching
node_color = [model.getVal(vars[i]) for i in graph.nodes]

figure = plt.figure()
nx.draw(graph, ax=figure.add_subplot(), with_labels=True, pos=nx.get_node_attributes(graph,'pos'), node_color=node_color, cmap=plt.cm.gray)
figure.savefig("graph_stableset.png")
