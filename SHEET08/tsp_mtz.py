import pyscipopt as scip
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import tsplib95

# load TSP instance
problem = tsplib95.load(
    "/Users/ritter/Documents/TEACHING/COURSES/DO-GitHub/SHEET08/tsp-problems/ulysses16.tsp"
)


def tsp_solve(problem: tsplib95.models.Problem) -> (float,list):
    # create the SCIP model
    model = scip.Model("TSP: Miller, Tucker, Zemlin")
    graph = problem.get_graph()
    n = len(graph.nodes)
    first_node = min(graph.nodes)

    x = {
        (i, j): model.addVar(vtype="B", name=f"x_({i},{j})")
        for i in graph.nodes
        for j in graph.nodes
        if graph.has_edge(i, j)
    }
    y = {i: model.addVar(vtype="C", ub=n, name=f"y_{i}") for i in graph.nodes}

    for i in graph.nodes:
        if i == first_node:
            model.addCons(y[i] == 1)
        else:
            model.addCons(y[i] >= 2)
    for i in graph.nodes:
        # outgoing edges
        model.addCons(
            scip.quicksum(x[(i, j)] for j in graph.nodes if graph.has_edge(i, j)) == 1
        )
        # incoming edges
        model.addCons(
            scip.quicksum(x[(j, i)] for j in graph.nodes if graph.has_edge(j, i)) == 1
        )

    for i in graph.nodes:
        for j in graph.nodes:
            if (i != first_node) and (j != first_node) and graph.has_edge(i, j):
                model.addCons(y[i] - y[j] + (n - 1) * x[(i, j)] <= n - 2)

    model.setObjective(
        scip.quicksum(
            x[(i, j)] * graph.edges[i, j]["weight"]
            for i in graph.nodes
            for j in graph.nodes
            if graph.has_edge(i, j)
        ),
        sense="minimize",
    )

    model.optimize()
    print(
        f"The model status is '{model.getStatus()}', solved after {model.getSolvingTime()} seconds."
    )
    solution = [None]*n # prepare empty list
    for i in graph.nodes:
        solution[int(model.getVal(y[i]))-1] = i
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

    # n = nv(tsp_graph)
    # first_node = 1

    # @objective(model, Min, sum(x[i,j] * tsp.weights[i,j] for i=1:n, j=1:n if has_edge(tsp_graph,i,j)))

    # optimize!(model)

    # if termination_status(model) == MOI.OPTIMAL  # if model was solved to optimality
    #     # compare optimal objective value with TSPLIB benchmark
    #     println("Optimal solution with objective value $(objective_value(model)) found (should be $(tsp.optimal)).")
    #     tsp_solution = [
    #         (i,j) for i=1:n, j=1:n
    #         if has_edge(tsp_graph, i,j) && value(x[i,j]) ≈ 1  # short for: isapprox(value(x[i,j]), 1)
    #     ]
    # else  # no solution
    #     println(raw_status(model))
    #     tsp_solution = []
#     # end
#     return tsp_solution
# end
