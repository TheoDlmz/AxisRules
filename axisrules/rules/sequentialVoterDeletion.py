from axisrules.rules import SequentialScoringRule

class SequentialVoterDeletion(SequentialScoringRule):

    name = "Sequential Voter Deletion"
    
    def _get_partial_cost(self, axis, matrix):

        n, m = matrix.shape
        cost = 0
        for i in range(n):
            vote = matrix[i][:-2]
            n_app = matrix[i][-2]
            n_v = matrix[i][-1]

            started = False
            finished = False
            count = 0
            cost_i = 0
            for i in range(len(axis)):
                if vote[axis[i]] == 1:
                    count += 1
                    if not started:
                        started = True
                    if finished:
                        cost_i = 1
                if vote[axis[i]] == 0 and started:
                    finished = True

            if n_app != count and count > 0 and (vote[axis[0]] == 0 and vote[axis[-1]] == 0):
                cost_i = 1
            cost += cost_i*n_v
        return cost
