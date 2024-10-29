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
model = scip.Model("Vertex Cover")

# add variables of type 'binary' for each node
vars = { ... }

# add constraints for each edge
# Use graph.edges to iterate over the edges. Each edge is a tuple e = (i,j),
# the end nodes can be accessed with e[0] and e[1].
for e in graph.edges:
    model.addCons( ... )

# add objective function
model.setObjective(scip.quicksum( ... ), sense="minimize")

# compute optimum
model.optimize()

# output result
print(
    f"The model status is '{model.getStatus()}', solved after {model.getSolvingTime()} seconds."
)
print("Solution:")
for i in graph.nodes: # use graph.nodes to iterate over the nodes
    print(f"node {i} -> {model.getVal(vars[i])}")

print(f"The vertex cover consists of the following {model.getObjVal()} nodes:")
print(f"   {[i for i in graph.nodes if model.getVal(vars[i]) == 1]}")

# draw graph with matching
for i in graph.nodes: 
    if model.getVal(vars[i]) == 1:
        graph.nodes[i]["color"] = "orange" # nodes can have attributes with arbitrary names such as "color"
    else:
        graph.nodes[i]["color"] = "gray"

figure = plt.figure()
nx.draw(graph, ax=figure.add_subplot(), with_labels=True, pos=nx.get_node_attributes(graph,'pos'), node_color=nx.get_node_attributes(graph,'color').values())
figure.savefig("graph_vertexcover.png")


# The following is useful for non-integer solutions, uncomment if necessary
# draw graph with nodes in shades of gray according to variable values

#node_color = [model.getVal(vars[i]) for i in graph.nodes]
#figure = plt.figure()
#nx.draw(graph, ax=figure.add_subplot(), with_labels=True, pos=nx.get_node_attributes(graph,'pos'), node_color=node_color, cmap=plt.cm.gray)
#figure.savefig("graph_vertexcover.png")
