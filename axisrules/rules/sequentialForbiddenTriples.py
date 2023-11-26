from axisrules.rules import SequentialScoringRule

class SequentialForbiddenTriples(SequentialScoringRule):

    name = "Sequential Forbidden Triples"
    
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
            score_from_inside = 0
            left = 0
            right = count
            for i in range(1,len(tab)):
                if i%2 == 1:
                    left += tab[i]
                    right -= tab[i]
                else:
                    score_from_inside += left*right*tab[i]

            score_from_left = 0
            remaining = n_app - count
            right = count
            for i in range(len(tab)):
                
                if i%2 == 1:
                    right -= tab[i]
                else:
                    score_from_left += remaining*right*tab[i]

            score_from_right = 0
            left = count 
            for i in range(len(tab)-1, -1, -1):
                if i%2 == 1:
                    left -= tab[i]
                else:
                    score_from_right += remaining*left*tab[i]
            
            cost_i = score_from_inside + min(score_from_left, score_from_right)
            cost += cost_i*n_v
        return cost
