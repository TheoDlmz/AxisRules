import itertools

def is_single_peaked(axis, vote):
    """
    Check if a vote is single peaked for a given axis
    """
    curr = len(vote)+1
    decr = True
    for i in range(len(axis)):
        v = vote[axis[i]]
        if decr and v > curr:
            decr = False
        if not decr and v < curr:
            return False
        curr = v

    return True
        


def compute_VD_rank_score(axis, votes, weights, min_score = None):
    """
    Compute the VD score of an axis for a given set of votes and weights
    """
    score = 0
    for vote, weight in zip(votes, weights):
        if not is_single_peaked(axis, vote):
            score += weight
            if min_score is not None and score > min_score:
                return False, None
    return True, score

def compute_best_VD_rank(votes, weights, starting_axis=None):

    n_votes, n_candidates = votes.shape
    cand_l = range(n_candidates-2)

    if starting_axis is not None:
        current_min = compute_VD_rank_score(starting_axis, votes, weights)[1]
        results = [(starting_axis, current_min)]

    else:
        current_min = None
        results = []
    for x in (list(itertools.permutations(cand_l))):
        lx = list(x)
        ok, score = compute_VD_rank_score(lx, votes, weights, current_min)
        if not ok:
            continue
        for i in range(n_candidates-1):
            for j in range(i,n_candidates-1):
                axis = lx[:i]+[n_candidates-2]+lx[i:j]+[n_candidates-1]+lx[j:]
                ok, score = compute_VD_rank_score(axis, votes, weights, current_min)
                if ok:
                    current_min = score
                    results.append((axis, score))
    return [x for x in results if x[1] == current_min]