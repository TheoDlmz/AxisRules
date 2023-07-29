import numpy as np

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

def reduce_weighted_matrix(matrix, remove=2):
    # We read the matrix of votes
    matrix_n = []
    matrix_dict = {}
    n_candidates = len(matrix[1])-2
    for elem in matrix:
        ballot = elem[:-2-remove]
        if ballot.sum() <= 1 or ballot.sum() >= n_candidates-2:
            continue
        strballot = "".join([str(x) for x in ballot])
        if strballot not in matrix_dict:
            matrix_dict[strballot] = len(matrix_n)
            x = np.concatenate([ballot,[np.sum(ballot),elem[-1]]])
            matrix_n.append(x)
        else:
            matrix_n[matrix_dict[strballot]][-1] += elem[-1]

    matrix_n = np.array(matrix_n)[np.argsort([matrix_n[i][-1] for i in range(len(matrix_n))])[::-1],:]
    return matrix_n


def compute_scores(votes, weights=None):
    if weights is None:
        weights = np.ones(len(votes))
    return votes.T.dot(weights)