import pyscipopt as scip
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# create Graph and read input
filename = "./MATCHING/adj-4.txt"
adjacency_matrix = np.loadtxt(filename)
n = adjacency_matrix.shape[0]

graph = nx.Graph()
for i in range(n):
    for j in range(i + 1, n):
        if adjacency_matrix[i, j] == 1:
            print(f"Add edge {i} -> {j}")
            graph.add_edge(i, j)

# create the SCIP model
model = scip.Model("General Matching")

# add variables of type 'binary' for each edge
vars = {
    tuple(sorted(e)): model.addVar(vtype="B", name=f"x_{tuple(sorted(e))}")
    for e in graph.edges
}
print(vars)

# add constraints for each node
for v in graph.nodes:
    model.addCons(
        scip.quicksum(vars[tuple(sorted(e))] for e in graph.edges(v)) <= 1,
        name=f"constraint for node {v}",
    )

# add objective function
model.setObjective(
    scip.quicksum(vars[tuple(sorted(e))] for e in graph.edges), sense="maximize"
)

# compute optimum
model.optimize()

# output result
print(
    f"The model status is '{model.getStatus()}', solved after {model.getSolvingTime()} seconds."
)
print(f"The matching consists of {model.getObjVal()} edges.")
print("The matching consists of the following edges:")
print(f"   {[e for e in graph.edges if model.getVal(vars[tuple(sorted(e))]) > 0.9]}")

# draw graph with matching
edge_color_list = ["gray"] * len(graph.edges)
for i, e in enumerate(graph.edges):
    if model.getVal(vars[tuple(sorted(e))]) > 0.9:
        edge_color_list[i] = "orange"

figure = plt.figure()
nx.draw(graph, ax=figure.add_subplot(), with_labels=True, edge_color=edge_color_list)
figure.savefig("graph_matching.png")
