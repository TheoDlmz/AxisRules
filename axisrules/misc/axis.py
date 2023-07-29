def print_order(arr, candidates):
    """
    Print an axis
    """
    print(" < ".join([candidates[i] for i in arr]))
    
def get_order(arr, candidates):
    """
    Return the string of an axis 
    """
    return " < ".join([candidates[i] for i in arr])



def kandallTau(ranking_1, ranking_2):
    """
    Compute the Kandall Tau distance between two rankings
    """
    n_candidates = len(ranking_1)
    count = 0
    for i in range(n_candidates):
        for j in range(i+1, n_candidates):
            if (ranking_1[i] - ranking_1[j])*(ranking_2[i] - ranking_2[j]) < 0:
                count += 1
    return count