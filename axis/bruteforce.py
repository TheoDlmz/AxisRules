import pandas as pd
import numpy as np
import itertools
from tqdm import tqdm
from axis.miscellaneous import compute_weighted_matrix
import sys

"""
Useful functions to compute the candidates approved that are the closest to the left/right side of the axis
"""

def find_min(axis, ballots):
    for i in range(len(axis)):
        if ballots[axis[i]]:
            return i
    return -1

def find_max(axis, ballots):
    for i in range(len(axis)):
        if ballots[axis[len(axis)-1-i]]:
            return len(axis)-1-i
    return -1

"""
Ballot completion and voter deletion rules as described in the paper
"""


def ballot_completion(axis, ballots, current_min=None):
    c_large = 0
    for ball in ballots:
        n = ball[-1]
        app = ball[-2]
        min_v = find_min(axis, ball[:-2])
        max_v = find_max(axis, ball[:-2])
        c_large += (max_v-min_v+1-app)*n        
        
        if current_min is not None and c_large > current_min:
            return c_large, False
    return c_large, True


def voter_deletion(axis, ballots, current_min=None):
    c_strict = 0
    for ball in ballots:
        n = ball[-1]
        app = ball[-2]
        min_v = find_min(axis, ball[:-2])
        max_v = find_max(axis, ball[:-2])
        if (max_v-min_v+1-app) > 0:
            c_strict += n
        
        if current_min is not None and c_strict > current_min:
            return c_strict, False
    return c_strict, True


def minimal_swaps(axis, ballots, current_min=None):
    score = 0
    
    for ball in ballots:
        n = ball[-1]
        app = ball[-2]
        min_v = find_min(axis, ball[:-2])
        max_v = find_max(axis, ball[:-2])
        count_before = 0
        for i in range(min_v, max_v):
            if not ball[axis[i]]:
                score += n*min(count_before, app-count_before)
            else:
                count_before += 1

        if current_min is not None and score > current_min:
            return score, False
    return score, True

def minimal_flips(axis, ballots, current_min=None):
    score = 0
    
    for ball in ballots:
        n = ball[-1]
        app = ball[-2]
        list_approved = [i for i in range(len(axis)) if ball[axis[i]]]
        min_val = len(axis)
        for i in range(len(list_approved)-1):
            for j in range(i+1, len(list_approved)):
                x = i + (len(list_approved)-j-1) + (list_approved[j]-list_approved[i]) -  (j-i)
                # flips 1->0 before, flips 1->0 after, flips 0->1 in between
                if x < min_val:
                    min_val = x
        score += n*min_val

        if current_min is not None and score > current_min:
            return score, False
    return score, True

def forbidden_triples(axis, ballots, current_min=None):
    score = 0
    for ball in ballots:
        n = ball[-1]
        app = ball[-2]
        min_v = find_min(axis, ball[:-2])
        max_v = find_max(axis, ball[:-2])
        count_before = 0
        for i in range(min_v, max_v):
            if not ball[axis[i]]:
                score += n*count_before*(app-count_before)
            else:
                count_before += 1

        if current_min is not None and score > current_min:
            return score, False
    return score, True


""" 
Circular variants
"""

def circular_ballot_completion(axis, ballots, current_min=None):
    c_large = 0
    n_cand = len(axis)
    for ball in ballots:
        n = ball[-1]
        app = ball[-2]
        min_v = find_min(axis, ball[:-2])
        max_v = find_max(axis, ball[:-2])
        min_fill = (max_v-min_v+1-app)
        for i in range(min_v+1, max_v+1):
            if ball[axis[i]]:
                max_v = min_v
                min_v = i
                min_fill = min(min_fill, (max_v+n_cand-min_v+1-app))
        c_large += min_fill*n
        
        if current_min is not None and c_large > current_min:
            return c_large, False
    return c_large, True

def circular_voter_deletion(axis, ballots, current_min=None):
    c_strict = 0
    n_cand = len(axis)
    for ball in ballots:
        n = ball[-1]
        app = ball[-2]
        min_v = find_min(axis, ball[:-2])
        max_v = find_max(axis, ball[:-2])
        found = False
        if (max_v-min_v+1-app) == 0:
            found = True
        else:
            count_el = 0
            for i in range(max_v+1):
                if ball[axis[i]]:
                    count_el += 1
                else:
                    break 
            for i in range(n_cand-1, min_v-1, -1):
                if ball[axis[i]]:
                    count_el += 1
                else:
                    break
            
            if count_el == app:
                found = True


        if not found:
            c_strict += n
        
        if current_min is not None and c_strict > current_min:
            return c_strict, False
    return c_strict, True



"""
Variants of the rules where we only consider the candidates with a score above a certain threshold,
to avoid the eccentricity phenomenon
"""

def create_ballot_completion_alpha(scores,alpha=1):
    def ballot_completion_alpha(axis, ballots, current_min=None):
        c_large = 0
        for ball in ballots:
            n = ball[-1]
            app = ball[-2]
            min_v = find_min(axis, ball[:-2])
            max_v = find_max(axis, ball[:-2])
            min_score = min([scores[axis[i]] for i in range(min_v, max_v+1) if ball[axis[i]]])
            real_holes = sum([1 for i in range(min_v, max_v+1) if not ball[axis[i]] and scores[axis[i]] > alpha*min_score])
            c_large += real_holes*n        
            
            if current_min is not None and c_large > current_min:
                return c_large, False
        return c_large, True
    return ballot_completion_alpha


def create_voter_deletion_alpha(scores,alpha=1):
    def voter_deletion_alpha(axis, ballots, current_min=None):
        c_strict = 0
        for ball in ballots:
            n = ball[-1]
            app = ball[-2]
            min_v = find_min(axis, ball[:-2])
            max_v = find_max(axis, ball[:-2])
            # JE COMPRENDS PAS : VERIFIER LE SCORE 
            min_score = min([scores[axis[i]] for i in range(min_v, max_v+1) if ball[axis[i]]])
            real_holes = sum([1 for i in range(min_v, max_v+1) if not ball[axis[i]] and scores[axis[i]] > alpha*min_score])
            if real_holes > 0:
                c_strict += n
            
            if current_min is not None and c_strict > current_min:
                return c_strict, False
        return c_strict, True
    return voter_deletion_alpha

"""
Variant of ballot completion in which every candidate is weighted by its approval score 
"""

def create_ballot_completion_pond(scores):
    def ballot_completion_alpha(axis, ballots, current_min=None):
        c_large = 0
        for ball in ballots:
            n = ball[-1]
            app = ball[-2]
            min_v = find_min(axis, ball[:-2])
            max_v = find_max(axis, ball[:-2])
            real_holes = sum([scores[axis[i]] for i in range(min_v, max_v+1) if not ball[axis[i]]])
            c_large += real_holes*n        
            
            if current_min is not None and c_large > current_min:
                return c_large, False
        return c_large, True
    return ballot_completion_alpha


"""
Useful function to compute an intermediary matrix called weighted matrix in which eahc row is 
a ballot type, with the number of approval ballots in it, and the total weights of voters that casted
this ballots. We remove every ballots with 0,1, or m approval.
"""

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

        if ballot.sum() <= 1 or ballot.sum() >= n_candidates:
            continue
        strballot = "".join([str(x) for x in ballot])
        if strballot not in matrix_dict:
            matrix_dict[strballot] = len(matrix_n)
            x = np.concatenate([ballot,[np.sum(ballot),w]])
            matrix_n.append(x)
        else:
            matrix_n[matrix_dict[strballot]][-1] += w

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



"""
MAIN FUNCTION
"""


def get_axis(votes, score_function=voter_deletion, weights=None, circular=False):

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
        _, ok = score_function(lx, matrix_reduced, current_min)
        if not ok:
            continue

        if circular:
            for j in range(n_candidates-1):
                axis = [n_candidates-2]+lx[:j]+[n_candidates-1]+lx[j:]
                score, ok = score_function(axis, matrix, current_min)
                if ok:
                    current_min = score
                    results.append((axis, score))
        else:
            for i in range(n_candidates-1):
                for j in range(i,n_candidates-1):
                    axis = lx[:i]+[n_candidates-2]+lx[i:j]+[n_candidates-1]+lx[j:]
                    score, ok = score_function(axis, matrix, current_min)
                    if ok:
                        current_min = score
                        results.append((axis, score))

    return [(axis, score) for axis, score in results if score == results[-1][1]]


