from axisrules.rules import SequentialScoringRule

class SequentialMinimalSwaps(SequentialScoringRule):

    name = "Sequential Minimal Swaps"
    
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
            cost_i = -1
           
            remaining = int(n_app - count)


            for outside_left in range(remaining+1):
                outside_right = remaining - outside_left
                left = 0
                right = count
                cost_i_tested = 0
                for i in range(1,len(tab)):
                    if i%2 == 1:
                        left += tab[i]
                        right -= tab[i]
                    else:
                        cost_i_tested += min(left+outside_left,right+outside_right)*tab[i]

                if cost_i_tested < cost_i or cost_i == -1:
                    cost_i = cost_i_tested

            cost += cost_i*n_v
        return cost
