from axisrules.rules import ScoringRule
from axisrules.misc import find_min, find_max
from gurobipy import GRB


class VoterDeletion(ScoringRule):
    """
    The Voter Deletion rule compute the axis which minimize the total number of voters 
    to delete for the profile to be linear.
    """

    name = "Voter Deletion"
    
    def get_ballot_score(self, axis, votes, n_app):
        min_v = find_min(axis, votes)
        max_v = find_max(axis, votes)
        if not self.abstention:
            if (max_v-min_v+1-n_app) > 0:
                return 1
            return 0
        else:
            for i in range(min_v+1, max_v):
                if votes[axis[i]] == -1:
                    return 1
            return 0
    
    def _lp_solve(self, model, matrix, vars, n_candidates):
        tab_scores = []
        for ballot in matrix:
            count = ballot[n_candidates+1]
            app_count = int(ballot[n_candidates])
            approvals = [i for i in range(n_candidates) if ballot[i] == 1]
            disapprovals = [i for i in range(n_candidates) if ballot[i] == 0]

            is_consistent = model.addVar(vtype=GRB.BINARY) # Is the ballot consistent with the axis
            for i in range(app_count):
                for j in range(app_count):
                    if i == j:
                        continue
                    for k in range(len(disapprovals)):
                        model.addConstr(vars[approvals[i]][disapprovals[k]] + vars[disapprovals[k]][approvals[j]] <= 2 - is_consistent)

            score = (1-is_consistent)*count

            tab_scores.append(score)

        model.setObjective(sum(tab_scores), GRB.MINIMIZE)