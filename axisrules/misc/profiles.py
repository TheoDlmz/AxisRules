import numpy as np

def compute_weighted_matrix(matrix, n_candidates, weights=None):
    # We read the matrix of votes
    matrix_n = []
    matrix_dict = {}
    for i, ballot in enumerate(matrix):
        w = 1
        if weights is not None:
            w = weights[i]

            if w == 0:
                continue

        ballot_without_abst = np.maximum(0, ballot)
        if ballot_without_abst.sum() <= 1 or ballot_without_abst.sum() >= n_candidates:
            continue
        strballot = "".join([str(x) for x in ballot])
        if strballot not in matrix_dict:
            matrix_dict[strballot] = len(matrix_n)
            x = np.concatenate([ballot,[np.sum(ballot_without_abst),w]])
            matrix_n.append(x)
        else:
            matrix_n[matrix_dict[strballot]][-1] += w

    if len(matrix_n) > 0:
        matrix_n = np.array(matrix_n)[np.argsort([matrix_n[i][-1] for i in range(len(matrix_n))])[::-1],:]
    return matrix_n

def reduce_weighted_matrix(matrix, remove=2):
    # We read the matrix of votes
    matrix_n = []
    matrix_dict = {}
    n_candidates = len(matrix[0])-2
    for elem in matrix:
        ballot = elem[:-2-remove]
        ballot_without_abst = np.maximum(0, ballot)
        if ballot_without_abst.sum() <= 1 or ballot_without_abst.sum() >= n_candidates-2:
            continue
        strballot = "".join([str(x) for x in ballot])
        if strballot not in matrix_dict:
            matrix_dict[strballot] = len(matrix_n)
            x = np.concatenate([ballot,[np.sum(ballot_without_abst),elem[-1]]])
            matrix_n.append(x)
        else:
            matrix_n[matrix_dict[strballot]][-1] += elem[-1]

    if len(matrix_n) > 0:
        matrix_n = np.array(matrix_n)[np.argsort([matrix_n[i][-1] for i in range(len(matrix_n))])[::-1],:]
    return matrix_n


def compute_scores(votes, weights=None):
    if weights is None:
        weights = np.ones(len(votes))
    return votes.T.dot(weights)

def print_profile(votes, candidates):
    dict_votes = {}
    for vote in votes:
        current_vote = []
        for i, x in enumerate(vote):
            if x == 1:
                current_vote.append(candidates[i])
        str_vote = "{"+ ",".join(current_vote) + "}"
        if str_vote not in dict_votes:
            dict_votes[str_vote] = 0
        dict_votes[str_vote] += 1
    tab_profile = [(k, dict_votes[k]) for k in sorted(dict_votes, key=dict_votes.get, reverse=True)]
    for k, v in tab_profile:
        print(k, v)


def get_profile(votes, candidates):
    dict_votes = {}
    for vote in votes:
        current_vote = []
        for i, x in enumerate(vote):
            if x == 1:
                current_vote.append(candidates[i])
        str_vote = "{"+ ",".join(current_vote) + "}"
        if str_vote not in dict_votes:
            dict_votes[str_vote] = 0
        dict_votes[str_vote] += 1
    tab_profile = [(k, dict_votes[k]) for k in sorted(dict_votes, key=dict_votes.get, reverse=True)]
    return tab_profile