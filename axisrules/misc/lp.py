import numpy as np
from gurobipy import Model, GRB

def init_model(n_candidates):
    # We build our model
    m = Model()
    in_vars = []
    for i in range(n_candidates):
        vars_i = []
        for j in range(n_candidates):
            vars_i.append(m.addVar(vtype=GRB.BINARY))
        in_vars.append(vars_i)

    # All variable are 0 or 1

    for i in range(n_candidates):
        m.addConstr(in_vars[i][i] == 0)
        for j in range(n_candidates):
            if i > j:
                m.addConstr(in_vars[i][j] + in_vars[j][i] == 1)

    m.addConstr(in_vars[1][0] == 1)


    # transitivity

    for i in range(n_candidates):
        for j in range(n_candidates):
            for k in range(n_candidates):
                m.addConstr(in_vars[i][j] + in_vars[j][k] + in_vars[k][i] <=  2)



    return  m, in_vars
