import pyscipopt as scip
import numpy as np

n = 4 # size of the chessboard

# create the SCIP model
model = scip.Model("Queens Problem")

# add variables of type 'binary', one for each field of the chessboard
var_array = np.zeros((n, n), dtype=object) # dtype object allows arbitrary storage
for i in range(n):
    for j in range(n):
        var_array[i,j] = model.addVar(vtype='B', name=f"x_{i}_{j}")

# row and column constraints: at most one queen per row/column
for i in range(n) :
    model.addCons(scip.quicksum(var_array[i,:]) <= 1, name=f"ctr_row_{i}")
    model.addCons(scip.quicksum(var_array[:,i]) <= 1, name=f"ctr_col_{i}")
# diagonal constraints: at most one queen on the diagonals (diagonal = row_index ± col_index == constant)
for k in range(-n+1,n):
    model.addCons(scip.quicksum(var_array[i,j] for i in range(n) for j in range(n) if i-j==k) <= 1, name=f"ctr_diag_{k}")
for k in range(0,2*n-1):
    model.addCons(scip.quicksum(var_array[i,j] for i in range(n) for j in range(n) if i+j==k) <= 1, name=f"ctr_antidiag_{k}")

# add objective function
model.setObjective(scip.quicksum(var_array.flat), sense="maximize")

# compute optimum
model.optimize()

model.writeProblem(filename="queens.lp")

for i in range(n):
    print("-"*(4*n+1))
    for j in range(n):
        if model.getVal(var_array[i,j]) > 0.9:
            print("| Q ",end="")    
        else:
            print("|   ",end="")
    print("|")
print("-"*(4*n+1))
