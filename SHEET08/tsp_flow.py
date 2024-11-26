import pyscipopt as scip
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import tsplib95

# load TSP instance
problem = tsplib95.load("SHEET08/tsp-problems/ulysses16.tsp")


def tsp_solve(
    problem: tsplib95.models.Problem,
) -> tuple[float, list]:  # objective, list of nodes in order
    # create the SCIP model
    model = scip.Model("TSP: Flow Formulation")
    graph = problem.get_graph()
    first_node = min(graph.nodes)

    x = {
        (i, j): model.addVar(vtype="B", name=f"x_{i},{j}")
        for i in graph.nodes
        for j in graph.nodes
        if graph.has_edge(i, j) and i < j
    }
    goods = list(graph.nodes)
    goods.remove(first_node)
    y = {
        (i, j, k): model.addVar(vtype="C", name=f"y_{i},{j},{k}")
        for i in graph.nodes
        for j in graph.nodes
        for k in goods
        if graph.has_edge(i, j)
    }

    # degree constraints
    for i in graph.nodes:
        model.addCons(
            scip.quicksum(
                x[(min(i, j), max(i, j))] for j in graph.neighbors(i) if i != j
            )
            == 2
        )
    # flow conservation constraints
    for k in goods:
        for i in graph.nodes:
            if i == first_node:  # in- and outflow constraints for first node
                model.addCons(
                    scip.quicksum(
                        y[(j, i, k)] for j in graph.nodes if graph.has_edge(i, j)
                    )
                    == 0
                )
                model.addCons(
                    scip.quicksum(
                        y[(i, j, k)] for j in graph.nodes if graph.has_edge(i, j)
                    )
                    == 2
                )
            elif (
                i != k
            ):  # flow conservation constraints for all other nodes except for node k
                model.addCons(
                    scip.quicksum(
                        y[(j, i, k)] for j in graph.nodes if graph.has_edge(i, j)
                    )
                    - scip.quicksum(
                        y[(i, j, k)] for j in graph.nodes if graph.has_edge(i, j)
                    )
                    == 0
                )
    # capacity constraints
    for k in goods:
        for i in graph.nodes:
            for j in graph.nodes:
                if (i < j) and (graph.has_edge(i, j)):
                    model.addCons(y[(i, j, k)] <= x[(i, j)])
                    model.addCons(y[(j, i, k)] <= x[(i, j)])

    model.setObjective(
        scip.quicksum(
            x[(i, j)] * graph.edges[i, j]["weight"]
            for i in graph.nodes
            for j in graph.nodes
            if (i < j) and (graph.has_edge(i, j))
        ),
        sense="minimize",
    )

    model.writeProblem("tsp_flow.lp")
    model.optimize()
    print(
        f"The model status is '{model.getStatus()}', solved after {model.getSolvingTime()} seconds."
    )
    solution = [
        first_node,
    ]
    previous_node = first_node
    current_node = first_node
    next_node = None
    while True:
        next_node = int(
            min(
                i
                for i in graph.neighbors(current_node)
                if i != current_node
                and i != previous_node
                and model.getVal(x[(min(current_node, i), max(current_node, i))]) > 0.9
            )
        )
        if next_node != first_node:
            solution.append(next_node)
            previous_node = current_node
            current_node = next_node
        else:
            break

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
    solution_edges = []
    first_node = None
    for i, v in enumerate(solution):
        if i == 0:
            from_node = v
            first_node = v
        else:
            solution_edges.append((from_node, v))
            from_node = v
    solution_edges.append((from_node, first_node))

    figure = plt.figure()
    nx.draw(
        graph.edge_subgraph(solution_edges), ax=figure.add_subplot(), with_labels=True
    )
    figure.savefig("tsp_solution.png")
else:
    print(f"Problem instance '{problem.name}' is not depictable.")
