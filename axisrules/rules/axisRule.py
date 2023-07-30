import numpy as np
from axisrules.misc import compute_weighted_matrix, reduce_weighted_matrix, init_model
import itertools

class AxisRule(object):
    """
    General Class for Axis Rules
    """
    name = None
    circular = False

    def __init__(self, profile, weights=None, abstention=False):
        self.profile = np.array(profile)
        self.weights = weights
        self.abstention = abstention

    def set_profile(self, profile, weights=None):
        self.profile = np.array(profile)
        self.weights = weights

    def _get_score(self, axis, matrix, current_min):
        raise NotImplementedError
    
    def get_score(self, axis):
        votes = self.profile
        weights = self.weights
        _, n_candidates = np.array(votes).shape
        matrix = compute_weighted_matrix(votes, n_candidates, weights)
        return self._get_score(axis, matrix, None)[0]
    

    def bruteforce(self):
        votes = self.profile
        weights = self.weights
        
        _, n_candidates = np.array(votes).shape

        matrix = compute_weighted_matrix(votes, n_candidates, weights)
        matrix_reduced = reduce_weighted_matrix(matrix, remove=2)
        # compute_weighted_matrix(votes[:,:-2], n_candidates-2, weights)

        k = 0
        current_min = None

        results = []
        
        cand_l = range(n_candidates-2)
        for x in (list(itertools.permutations(cand_l))):
            k += 1
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

    def __str__(self):
        return self.name
