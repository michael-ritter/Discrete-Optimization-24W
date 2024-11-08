import pyscipopt as scip

a = 13
b = 2

# create the SCIP model
model = scip.Model("Greatest Common Divisor")

# add variables x and y of type 'integer' with no upper and lower bound
x = model.addVar(vtype="I", lb=None, ub=None, name="x")
y = model.addVar(vtype="I", lb=None, ub=None, name="y")

# add constraint
constraint = model.addCons(a*x + b*y >= 1, name="Constraint 1")

# add objective function
model.setObjective(a*x + b*y, sense="minimize")

# compute optimum
model.optimize()

# output result
print(f"The model status is '{model.getStatus()}', solved after {model.getSolvingTime()} seconds.")
print(f"The gcd of {a} and {b} is {model.getObjVal()}.")
print(f"It can be represented as gcd({a}, {b}) = {model.getObjVal()} = {a} * {model.getVal(x)} + {b} * {model.getVal(y)}.")
