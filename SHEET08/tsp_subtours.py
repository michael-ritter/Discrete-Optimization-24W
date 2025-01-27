import pyscipopt as scip
import networkx as nx
import matplotlib.pyplot as plt
import tsplib95

# load TSP instance
problem = tsplib95.load("SHEET08/tsp-problems/ts225.tsp")

# subtour elimination constraint handler
class SubtourEliminationConstraintHandler(scip.Conshdlr):

    # method for creating a constraint of this constraint handler type
    def createCons(self, name, variables):
        constr = self.model.createCons(self, name)

        # data relevant for the constraint
        # Here we need to access the variables to find subtours
        # constr is a dict that contains all relevant data
        # for the separation subroutines
        constr.data = {}
        constr.data['variables'] = variables
        return constr


    # find subtours in the graph induced by the edges {i,j} 
    # for which x[(i,j]) is positive at the given solution
    def find_subtours(self, constr, solution = None):
        graph = nx.Graph()
        x = constr.data['variables']

        for i,j in x.keys():
            if self.model.getSolVal(solution, x[(i,j)]) > 0.9: #getVal can only be used once the model is solved, must use getSolVal for intermediate solution
                graph.add_edge(i, j)

        components = list(nx.connected_components(graph))

        if len(components) == 1:
            return []
        else:
            return components

    # checks whether solution is feasible
    # returns either SCIP_RESULT.INFEASIBLE or SCIP_RESULT.FEASIBLE
    # as "result" in a dictionary
    def conscheck(self, constraints, solution, check_integrality,
                  check_lp_rows, print_reason, completely, **results):

        # check if there is a violated subtour elimination constraint
        # and return SCIP_RESULT.INFEASIBLE if any is found
        for ctr in constraints:
            if self.find_subtours(ctr, solution):
                return {"result": scip.SCIP_RESULT.INFEASIBLE}

        # no violated constraint found, return SCIP_RESULT.FEASIBLE
        return {"result": scip.SCIP_RESULT.FEASIBLE}


    # enforces the LP solution: 
    # search for subtours in the solution 
    # and add constraints forbidding every subtour discovered
    def consenfolp(self, constraints, n_useful_conss, sol_infeasible):
        constraint_added = False

        for ctr in constraints:
            subtours = self.find_subtours(ctr)

            # if there are subtours
            if subtours:
                x = ctr.data['variables']

                # add subtour elimination constraint for each subtour
                for S in subtours:
                    print(f"SEC added for subtour {S}")
                    self.model.addCons(scip.quicksum(x[(i,j)] for i in S for j in S if (i,j) in x.keys()) <= len(S)-1)
                    constraint_added = True

        if constraint_added:
            return {"result": scip.SCIP_RESULT.CONSADDED}
        else:
            return {"result": scip.SCIP_RESULT.FEASIBLE}


    # this is a technical detail and not relevant for the exercise
    def conslock(self, constraint, locktype, nlockspos, nlocksneg):
        pass
        

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

    # degree constraints
    for i in graph.nodes:
        model.addCons(
            scip.quicksum(
                x[(min(i, j), max(i, j))] for j in graph.neighbors(i) if i != j
            )
            == 2
        )

    model.setObjective(
        scip.quicksum(
            x[(i, j)] * graph.edges[i, j]["weight"]
            for i in graph.nodes
            for j in graph.nodes
            if (i < j) and (graph.has_edge(i, j))
        ),
        sense="minimize",
    )
    
    # create the constraint handler and add it to SCIP. 
    # Set negative priority (prio = when is the handler invoked), so that the handler is invoked
    # only when an integer feasible solution is available (integrality handler has prio 0)
    # Priority is separate by "check feasibility" and "enforce constraint"
    constraint_handler = SubtourEliminationConstraintHandler()
    model.includeConshdlr(constraint_handler, "TSP", "TSP subtour elimination constraint", chckpriority = -10, enfopriority = -10)

    # create a subtour elimination constraint, pass x as relevant variables
    sec_constraints = constraint_handler.createCons("Subtour Elimination Constraints", x)

    # add constraint to the model
    model.addPyCons(sec_constraints)

    model.writeProblem("tsp_subtours.lp")
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
