import pyscipopt as scip
import numpy as np

n = 4 # size of the chessboard

# create the SCIP model
model = scip.Model("Queens Problem")

# add variables of type 'binary', one for each field of the chessboard
var_array = np.zeros((n, n), dtype=object) # dtype object allows arbitrary storage

# row and column constraints: at most one queen per row/column
# TODO

# diagonal constraints: at most one queen on the diagonals (diagonal = row_index ± col_index == constant)
# TODO

# add objective function
# TODO

# compute optimum
model.optimize()

model.writeProblem(filename="queens.lp")

for i in range(n):
    print("-"*(4*n+1))
    for j in range(n):
        if model.getVal(var_array[i,j]) == 1:
            print("| Q ",end="")    
        else:
            print("|   ",end="")
    print("|")
print("-"*(4*n+1))
