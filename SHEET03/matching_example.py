import pyscipopt as scip

# create the SCIP model
model = scip.Model("Bipartite Matching Example")

# add variables of type 'binary' for each edge

# add constraints for each node

# add objective function

# compute optimum
model.optimize()

# output result
print(f"The model status is '{model.getStatus()}', solved after {model.getSolvingTime()} seconds.")
print(f"The matching consists of {model.getObjVal()} edges.")
print(f"Solution values: x_16 = {model.getVal(x_16)}")
print(f"Solution values: x_17 = {model.getVal(x_17)}")
print(f"Solution values: x_28 = {model.getVal(x_28)}")
print(f"Solution values: x_35 = {model.getVal(x_35)}")
print(f"Solution values: x_36 = {model.getVal(x_36)}")
print(f"Solution values: x_37 = {model.getVal(x_37)}")
print(f"Solution values: x_48 = {model.getVal(x_48)}")