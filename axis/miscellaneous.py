import numpy as np

def print_order(arr, candidates):
    print(" < ".join([candidates[i] for i in arr]))
    
def get_order(arr, candidates):
    return " < ".join([candidates[i] for i in arr])



def compute_weighted_matrix(matrix, n_candidates):
    # We read the matrix of votes
    matrix_n = []
    matrix_dict = {}
    for  ballot in matrix:
        if ballot.sum() <= 1 or ballot.sum() >= n_candidates:
            continue
        strballot = "".join([str(x) for x in ballot])
        if strballot not in matrix_dict:
            matrix_dict[strballot] = len(matrix_n)
            x = np.concatenate([ballot,[np.sum(ballot),1]])
            matrix_n.append(x)
        else:
            matrix_n[matrix_dict[strballot]][-1] += 1

    matrix_n = np.array(matrix_n)[np.argsort([matrix_n[i][-1] for i in range(len(matrix_n))])[::-1],:]
    return matrix_n

def kandallTau(ranking_1, ranking_2):
    n_candidates = len(ranking_1)
    count = 0
    for i in range(n_candidates):
        for j in range(i+1, n_candidates):
            if (ranking_1[i] - ranking_1[j])*(ranking_2[i] - ranking_2[j]) < 0:
                count += 1
    return count

def compute_scores(votes, weights=None):
    if weights is None:
        weights = np.ones(len(votes))
    return votes.T.dot(weights)