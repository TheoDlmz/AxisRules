
import numpy as np

################# PROFILE GENERATION #####################

def generate_profile(m_candidates, n_voters, alpha=1, beta=1):

    # Positions of the candidates on the axis [0,1]
    candidates = np.random.rand(m_candidates)
    axis = np.argsort(candidates)
    # Positions of the voters
    voters = np.random.rand(n_voters)
    # Influence of the candidates
    influence = np.random.rand(m_candidates)

    # Compute the approval ballots of voters 
    approval_ballots = np.zeros((n_voters, m_candidates))
    for i in range(n_voters):
        for j in range(m_candidates):
            distance = abs(voters[i] - candidates[j])
            proba = np.exp(-alpha*distance)*(influence[j]*beta + 1-beta)
            if np.random.rand() < proba:
                approval_ballots[i,j] = 1
    
    return approval_ballots, axis, influence


