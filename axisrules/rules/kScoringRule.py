from axisrules.rules import AxisRule
from axisrules.misc import compute_weighted_matrix, reduce_weighted_matrix, init_model
import itertools
import numpy as np
from tqdm import tqdm

class KScoringRule(AxisRule):
    """
    
    """
    def __init__(self, k, scoringRule, profile, weights=None, abstention=False):
        self.k = k
        self.scoring_rule= scoringRule(profile, weights, abstention)
        super().__init__(profile, weights, abstention)
    
    def get_score(self, axes):
        votes = self.profile
        weights = self.weights
        _, n_candidates = np.array(votes).shape
        matrix = compute_weighted_matrix(votes, n_candidates, weights)
        return self._get_score(axes, matrix, None)[0]
    
    def _get_score(self, axes, matrix, current_min, reduced=False):
        score = 0
        for ball in matrix:
            n = ball[-1]
            n_app = ball[-2]
            votes = ball[:-2]
            min_score_ball = None
            for j,axis in enumerate(axes):
                if j ==0 and reduced:
                    v = self.scoring_rule.get_ballot_score(axis, votes[:-2], n_app-votes[-1]-votes[-2])
                else:
                    v = self.scoring_rule.get_ballot_score(axis, votes, n_app)
                if min_score_ball is None or v < min_score_ball:
                    min_score_ball = v

            score += n*min_score_ball

            if current_min is not None and score > current_min:
                return score, False
        return score, True
    
    
    def bruteforce(self, list_axes=[]):
        if len(list_axes) == self.k :
            return list_axes
        
        votes = self.profile
        weights = self.weights
        
        _, n_candidates = np.array(votes).shape

        matrix = compute_weighted_matrix(votes, n_candidates, weights)
        if len(matrix) == 0:
            # return all permutations
            return [([i for i in range(n_candidates)], 0)]
        # matrix_reduced = []
        # for ballot in matrix:
        #     x = np.concatenate([ballot[:-4],[np.sum(ballot[:-4]),ballot[-1]]])
        #     matrix_reduced.append(x)

        # matrix_reduced = np.array(matrix_reduced)
        # compute_weighted_matrix(votes[:,:-2], n_candidates-2, weights)

        # k = 0
        current_min = None

        results = []

        cand_l = range(n_candidates-2)
        for x in tqdm(list(itertools.permutations(cand_l))):
            # k += 1
            lx = list(x)
            _, ok = self._get_score([lx] + list_axes, matrix, current_min, reduced=True)
            if not ok:
                continue

            for i in range(n_candidates-1):
                for j in range(i,n_candidates-1):
                    axis = lx[:i]+[n_candidates-2]+lx[i:j]+[n_candidates-1]+lx[j:]
                    score, ok = self._get_score([axis] + list_axes, matrix, current_min)
                    if ok:
                        current_min = score
                        results.append((axis, score))

        updated_list = list_axes + [results[-1][0]]
        return self.bruteforce(updated_list)
