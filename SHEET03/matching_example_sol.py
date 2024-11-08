import pyscipopt as scip

# create the SCIP model
model = scip.Model("Bipartite Matching Example")

# add variables of type 'binary' for each edge
x_16 = model.addVar(vtype="B", name='x16')
x_17 = model.addVar(vtype="B", name='x17')
x_28 = model.addVar(vtype="B", name='x28')
x_35 = model.addVar(vtype="B", name='x35')
x_36 = model.addVar(vtype="B", name='x36')
x_37 = model.addVar(vtype="B", name='x37')
x_48 = model.addVar(vtype="B", name='x48')

# add constraints for each node
model.addCons(x_16 + x_17 <= 1, name="vertex 1")
model.addCons(x_28 <= 1, name="vertex 2")
model.addCons(x_35 + x_36 + x_37 <= 1, name="vertex 3")
model.addCons(x_48 <= 1, name="vertex 4")
model.addCons(x_35 <= 1, name="vertex 5")
model.addCons(x_16 + x_36 <= 1, name="vertex 6")
model.addCons(x_17 + x_37 <= 1, name="vertex 7")
model.addCons(x_28 + x_48 <= 1, name="vertex 8")

# add objective function
model.setObjective( x_16 + x_17 + x_28 + x_35 + x_36 + x_37 + x_48, sense="maximize")

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