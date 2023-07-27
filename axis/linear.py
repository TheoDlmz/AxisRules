import numpy as np
from gurobipy import Model, GRB
from axis.miscellaneous import compute_weighted_matrix


################ LINEAR PROGRAM #########################



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


def ballot_completion_lp(m, matrix_votes, in_vars, n_candidates):
    # We compute the positions

    positions = []
    for i in range(n_candidates):
        pos_i = m.addVar(vtype=GRB.INTEGER, ub=n_candidates-1, lb=0)
        m.addConstr(pos_i == sum(in_vars[i][j] for j in range(n_candidates)))
        positions.append(pos_i)

    tab_scores = []
    for ballot in matrix_votes:
        count = ballot[n_candidates+1]
        app_count = ballot[n_candidates]
        approvals = [i for i in range(n_candidates) if ballot[i] == 1]
        x_M = m.addVar(vtype=GRB.INTEGER)
        x_m = m.addVar(vtype=GRB.INTEGER)
        m.addGenConstrMax(x_M, [positions[i] for i in approvals])
        m.addGenConstrMin(x_m, [positions[i] for i in approvals])

        score = (x_M - x_m - app_count + 1)*count

        tab_scores.append(score)

    m.setObjective(sum(tab_scores), GRB.MINIMIZE)

def voter_deletion_lp(m, matrix_votes, in_vars, n_candidates):
    tab_scores = []
    for ballot in matrix_votes:
        count = ballot[n_candidates+1]
        app_count = int(ballot[n_candidates])
        approvals = [i for i in range(n_candidates) if ballot[i] == 1]
        disapprovals = [i for i in range(n_candidates) if ballot[i] == 0]

        is_consistent = m.addVar(vtype=GRB.BINARY) # Is the ballot consistent with the axis
        for i in range(app_count):
            for j in range(app_count):
                if i == j:
                    continue
                for k in range(len(disapprovals)):
                    m.addConstr(in_vars[approvals[i]][disapprovals[k]] + in_vars[disapprovals[k]][approvals[j]] <= 2 - is_consistent)

        score = (1-is_consistent)*count

        tab_scores.append(score)

    m.setObjective(sum(tab_scores), GRB.MINIMIZE)


def solve_lp(votes, rule, weights=None):
    votes = np.array(votes)

    n_candidates = votes.shape[1] # Number of candidates

    matrix_votes = compute_weighted_matrix(votes, n_candidates, weights)
    m, in_vars = init_model(n_candidates)
    #rule_large(m, matrix_votes, in_vars, n_candidates)
    rule(m, matrix_votes, in_vars, n_candidates)
    # optimize with no verbose
    m.setParam('OutputFlag', 0)
    m.optimize( )

    # print("Optimal value:", m.objVal)
    ranking = [0 for i in range(n_candidates)]

    matrix = np.zeros((n_candidates, n_candidates))
    for i in range(n_candidates):
        for j in range(n_candidates):
            if np.round(in_vars[i][j].x) == 1:
                matrix[i][j] = 1
    
    positions = [np.sum(matrix[i]) for i in range(n_candidates)]
    for i in range(n_candidates):
        ranking[int(positions[i])] = i

    return ranking