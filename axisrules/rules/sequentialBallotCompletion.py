from axisrules.rules import SequentialScoringRule

class SequentialBallotCompletion(SequentialScoringRule):

    name = "Sequential Ballot Completion"
    
    def _get_partial_cost(self, axis, matrix):

        n, m = matrix.shape
        cost = 0
        for i in range(n):
            vote = matrix[i][:-2]
            n_app = matrix[i][-2]
            n_v = matrix[i][-1]

            last = 0
            tab = [0]
            for i in range(len(axis)):
                if vote[axis[i]] == last:
                    tab[-1] += 1
                else:
                    tab.append(1)
                    last = vote[axis[i]]

            count = sum([tab[i] for i in range(len(tab)) if i%2 == 1])
            cost_i = 0
            for i in range(2,len(tab)):
                if i%2 == 0 and i < len(tab)-1:
                    cost_i += tab[i]

            if tab[0] > 0 and len(tab)%2 == 1 and count > 0 and count != n_app:
                cost_i += min(tab[0], tab[-1])
                
            cost += cost_i*n_v
        return cost
