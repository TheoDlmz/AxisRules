from axisrules.rules import AxisRule
from axisrules.misc import compute_weighted_matrix, reduce_weighted_matrix, init_model
import itertools
import numpy as np

class ScoringRule(AxisRule):
    """
    Class for the special family of Axis Rules which consist in each voter giving a cost to an axis and selecting
    the axis with minimal cost.
    """

    
    def get_score(self, axis):
        votes = self.profile
        weights = self.weights
        _, n_candidates = np.array(votes).shape
        matrix = compute_weighted_matrix(votes, n_candidates, weights)
        return self._get_score(axis, matrix, None)[0]
    

    def bruteforce(self, proxy_axis=None):
        votes = self.profile
        weights = self.weights
        
        _, n_candidates = np.array(votes).shape

        matrix = compute_weighted_matrix(votes, n_candidates, weights)
        if len(matrix) == 0:
            # return all permutations
            return [([i for i in range(n_candidates)], 0)]
        matrix_reduced = reduce_weighted_matrix(matrix, remove=2)
        # compute_weighted_matrix(votes[:,:-2], n_candidates-2, weights)

        # k = 0
        current_min = None

        results = []

        if proxy_axis is not None:
            score, ok = self._get_score(proxy_axis,matrix, None)
            results.append((proxy_axis, score))
            current_min = score
        
        cand_l = range(n_candidates-2)
        for x in (list(itertools.permutations(cand_l))):
            # k += 1
            lx = list(x)
            _, ok = self._get_score(lx, matrix_reduced, current_min)
            if not ok:
                continue

            if self.circular:
                for j in range(n_candidates-1):
                    axis = [n_candidates-2]+lx[:j]+[n_candidates-1]+lx[j:]
                    score, ok = self._get_score(axis, matrix, current_min)
                    if ok:
                        current_min = score
                        results.append((axis, score))
            else:
                for i in range(n_candidates-1):
                    for j in range(i,n_candidates-1):
                        axis = lx[:i]+[n_candidates-2]+lx[i:j]+[n_candidates-1]+lx[j:]
                        score, ok = self._get_score(axis, matrix, current_min)
                        if ok:
                            current_min = score
                            results.append((axis, score))

        return [(axis, score) for axis, score in results if score == results[-1][1]]


    def _lp_solve(self, model, matrix, vars, n_candidates):
        raise NotImplementedError
    
    def lp(self):
        votes = self.profile 
        weights = self.weights

        n_candidates = votes.shape[1] # Number of candidates

        matrix_votes = compute_weighted_matrix(votes, n_candidates, weights)
        m, in_vars = init_model(n_candidates)
        #rule_large(m, matrix_votes, in_vars, n_candidates)
        self._lp_solve(m, matrix_votes, in_vars, n_candidates)
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

    def __call__(self, solver="bruteforce"):
        if solver == "bruteforce":
            return self.bruteforce()[0][0]
        elif solver == "lp":
            return self.lp()
        else:
            raise ValueError("Unknown solver")

    def get_ballot_score(self, axis, votes, n_app):
        raise NotImplementedError

    def get_individual_scores(self, axis, matrix):
        scores_tab = []
        for ballot in matrix:
            n = ballot[-1]
            n_app = ballot[-2]
            votes = ballot[:-2]
            score = self.get_ballot_score(axis, votes, n_app)
            scores_tab.extend([score]*n)
        return scores_tab

    def _get_score(self, axis, matrix, current_min):
        score = 0
        for ball in matrix:
            n = ball[-1]
            n_app = ball[-2]
            votes = ball[:-2]
            score += n*self.get_ballot_score(axis, votes, n_app)

            if current_min is not None and score > current_min:
                return score, False
        return score, True