from axisrules.rules import ScoringRule
from axisrules.misc import find_min, find_max
from gurobipy import GRB


class BallotCompletion(ScoringRule):
    """
    The Ballot Completion rule compute the axis which minimize the total number of candidates to add to voters' ballots
    for the profile to be linear.
    """

    name = "Ballot Completion"
    
    def get_ballot_score(self, axis, votes, n_app):
        min_v = find_min(axis, votes)
        max_v = find_max(axis, votes)
        if not self.abstention:
            return max_v-min_v+1-n_app
        else:
            return len([x for x in range(min_v+1, max_v) if votes[axis[x]] == -1])
    
    def _lp_solve(self, model, matrix, vars, n_candidates):
        # We compute the positions

        positions = []
        for i in range(n_candidates):
            pos_i = model.addVar(vtype=GRB.INTEGER, ub=n_candidates-1, lb=0)
            model.addConstr(pos_i == sum(vars[i][j] for j in range(n_candidates)))
            positions.append(pos_i)

        tab_scores = []
        for ballot in matrix:
            count = ballot[n_candidates+1]
            app_count = ballot[n_candidates]
            approvals = [i for i in range(n_candidates) if ballot[i] == 1]
            x_M = model.addVar(vtype=GRB.INTEGER)
            x_m = model.addVar(vtype=GRB.INTEGER)
            model.addGenConstrMax(x_M, [positions[i] for i in approvals])
            model.addGenConstrMin(x_m, [positions[i] for i in approvals])

            score = (x_M - x_m - app_count + 1)*count

            tab_scores.append(score)

        model.setObjective(sum(tab_scores), GRB.MINIMIZE)