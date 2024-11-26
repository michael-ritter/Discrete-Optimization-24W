from itertools import pairwise
import pyscipopt as scip
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import tsplib95

# load TSP instance
problem = tsplib95.load(
    "SHEET08/tsp-problems/ulysses16.tsp"
)


def tsp_solve(problem: tsplib95.models.Problem) -> tuple[float,list]: #objective, list of nodes in order
    # create the SCIP model
    model = scip.Model("TSP")
    graph = problem.get_graph()
    n = len(graph.nodes)
    
    # …

    model.optimize()
    print(
        f"The model status is '{model.getStatus()}', solved after {model.getSolvingTime()} seconds."
    )
    solution = [None]*n # prepare empty list
    # fill list …
    return model.getObjVal(), solution

objective, solution = tsp_solve(problem)

print(f"Solution with total weight {objective}:")
for i, v in enumerate(solution):
    if i == 0:
        print(v, end="")
    else:
        print(f" -> {v}", end="")
print(f" -> {solution[0]}")

if problem.is_depictable():
    graph = problem.get_graph()
    solution_edges = [e for e in pairwise(solution)]
    cycle_edge = (solution_edges[-1][1], solution_edges[0][0])
    solution_edges.append(cycle_edge)

    figure = plt.figure()
    nx.draw(
        graph.edge_subgraph(solution_edges), ax=figure.add_subplot(), with_labels=True
    )
    figure.savefig("tsp_solution.png")
else:
    print(f"Problem instance '{problem.name}' is not depictable.")