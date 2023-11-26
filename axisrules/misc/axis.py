import numpy as np

def print_axis(arr, candidates):
    """
    Print an axis
    """
    print(" < ".join([candidates[i] for i in arr]))
    
def get_axis(arr, candidates):
    """
    Return the string of an axis 
    """
    return " < ".join([candidates[i] for i in arr])


def reverse_axis(axis, candidates):
    """
    Return the axis from the string of the axis
    """
    list_cand = axis.split(" < ")
    return [candidates.index(list_cand[i]) for i in range(len(list_cand))]



def kandallTau(ranking_1, ranking_2):
    """
    Compute the Kandall Tau distance between two rankings
    """
    n_candidates = len(ranking_1)
    ranks1 = np.argsort(ranking_1)
    ranks2 = np.argsort(ranking_2)
    count = 0
    for i in range(n_candidates):
        for j in range(i+1, n_candidates):
            if (ranks1[i] - ranks1[j])*(ranks2[i] - ranks2[j]) < 0:
                count += 1
    ranks2 = np.argsort(ranking_2[::-1])
    count_2 = 0
    for i in range(n_candidates):
        for j in range(i+1, n_candidates):
            if (ranks1[i] - ranks1[j])*(ranks2[i] - ranks2[j]) < 0:
                count_2 += 1
    return min(count, count_2)


"""
Useful functions to compute the candidates approved that are the closest to the left/right side of the axis
"""

def find_min(axis, ballots):
    for i in range(len(axis)):
        if ballots[axis[i]] == 1:
            return i
    return -1

def find_max(axis, ballots):
    for i in range(len(axis)):
        if ballots[axis[len(axis)-1-i]] == 1:
            return len(axis)-1-i
    return -1