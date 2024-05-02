
import numpy as np

class MaverickVotersModel():

    name = "Maverick Voters"

    def __init__(self, p=0.2):
        self.p = p

    
    
    def __call__(self, m_candidates, n_voters):
        votes = np.zeros((n_voters, m_candidates))

        for i in range(n_voters):
            if np.random.rand() > self.p:
                # select two distinct elements between 0 and m_candidates-1 using np choice
                sides = np.random.choice(m_candidates, 2, replace=False)
                left_side = min(sides)
                right_side = max(sides)
                for j in range(left_side, right_side):
                    votes[i,j] = 1
            else:
                votes[i,:] = np.random.randint(0,2,m_candidates)
        
        return votes
    

class RandomOmissionsModel():

    name = "Random Omissions"

    def __init__(self, p=0.2):
        self.p = p
    
    def __call__(self, m_candidates, n_voters):
        votes = np.zeros((n_voters, m_candidates))

        for i in range(n_voters):
            sides = np.random.choice(m_candidates, 2, replace=False)
            left_side = min(sides)
            right_side = max(sides)
            votes[i, left_side:right_side+1] = 1
            for j in range(left_side, right_side+1):
                if np.random.rand() < self.p:
                    votes[i,j] = 0
        
        return votes


class RandomFlipsModel():

    name = "Random Flips"

    def __init__(self, p=0.2):
        self.p = p
    
    def __call__(self, m_candidates, n_voters):
        votes = np.zeros((n_voters, m_candidates))

        for i in range(n_voters):
            # select two distinct elements between 0 and m_candidates-1 using np choice
            sides = np.random.choice(m_candidates, 2, replace=False)
            left_side = min(sides)
            right_side = max(sides)
            votes[i, left_side:right_side+1] = 1
            for j in range(m_candidates):
                if np.random.rand()< self.p:
                    votes[i,j] = 1-votes[i,j]
        
        return votes


## Code taken from mapel library

def computeInsertionProbas(i, phi):
    probas = (i + 1) * [0]
    for j in range(i + 1):
        probas[j] = pow(phi, (i + 1) - (j + 1))
    return probas


def weighted_choice(choices):
    total = 0
    for w in choices:
        total = total + w
    r = np.random.uniform(0, total)
    upto = 0.0
    for i, w in enumerate(choices):
        if upto + w >= r:
            return i
        upto = upto + w
    assert False, "Shouldn't get here"


def mallowsVote(m, insertion_probabilites_list, center):
    vote = [center[0]]
    for i in range(1, m):
        index = weighted_choice(insertion_probabilites_list[i - 1])
        vote.insert(index, center[i])
    return vote





class RandomSwapsModel():

    name = "Random Swaps"

    def __init__(self, phi=0.2):
        self.phi = phi
    
    def __call__(self, m_candidates, n_voters):
        votes = np.zeros((n_voters, m_candidates))

        phi = self.phi
        insertion_probabilites_list = []
        for i in range(1, m_candidates):
            insertion_probabilites_list.append(computeInsertionProbas(i, phi))

        for i in range(n_voters):

            swapped_axis = mallowsVote(m_candidates, insertion_probabilites_list, range(m_candidates))
            
            sides = np.random.choice(m_candidates, 2, replace=False)
            left_side = min(sides)
            right_side = max(sides)
            for j in range(left_side, right_side+1):
                votes[i,swapped_axis[j]] = 1
        
        return votes
