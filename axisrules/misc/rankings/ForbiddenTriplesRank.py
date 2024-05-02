
import itertools
import numpy as np 


def votes_to_triplets(votes,weights):
    n_voters, n_candidates = votes.shape

    triplets = np.zeros((n_candidates, n_candidates, n_candidates))

    for i in range(n_voters):
        vote = votes[i]
        weight = weights[i]
        order = np.argsort(vote)
        peak = order[0]
        for i in range(1, len(order)):
            for j in range(i+1, len(order)):
                triplets[peak, order[i], order[j]] += weight
    return triplets

def compute_FT_rank_score(axis, triplets, min_score = None):
    score = 0
    for i in range(len(axis)):
        for j in range(i+1, len(axis)):
            for k in range(j+1, len(axis)):
                score += triplets[axis[i], axis[k], axis[j]]
        for j in range(i):
            for k in range(j):
                score += triplets[axis[i], axis[k], axis[j]]
        if min_score is not None and score > min_score:
            return False, None
    return True, score


def compute_best_FT_rank(votes, weights, starting_axis=None):

    tt = votes_to_triplets(votes, weights)

    n_votes, n_candidates = votes.shape
    cand_l = range(n_candidates-2)

    if starting_axis is not None:
        current_min = compute_FT_rank_score(starting_axis, tt)[1]
        results = [(starting_axis, current_min)]
    else:
        current_min = None
        results = []

    for x in (list(itertools.permutations(cand_l))):
        lx = list(x)
        for i in range(n_candidates-1):
            for j in range(i,n_candidates-1):
                axis = lx[:i]+[n_candidates-2]+lx[i:j]+[n_candidates-1]+lx[j:]
                ok, score = compute_FT_rank_score(axis, tt, current_min)
                if ok:
                    current_min = score
                    results.append((axis, score))

    return [x for x in results if x[1] == current_min]