from axisrules.rules import SequentialScoringRule

class SequentialMinimalFlips(SequentialScoringRule):

    name = "Sequential Minimal Flips"
    
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

            first_is_1 = tab[0] == 0

            for i in range(1, len(tab)):
                for j in range(i, len(tab)):
                    if i%2 == 1 and j%2 == 1:
                        inside = sum([tab[i] for i in range(i,j+1) if i%2 == 1])
                        zero_to_one = sum([tab[i] for i in range(i,j) if i%2 == 0])
                        one_to_zero = count - inside
                        if (i > 1 or not first_is_1) and (j < len(tab)-1):
                            one_to_zero += n_app - count 

                        cost_i_tested = zero_to_one + one_to_zero
                        if cost_i_tested < cost_i or cost_i == -1:
                            cost_i = cost_i_tested
            cost += cost_i*n_v
        return cost
