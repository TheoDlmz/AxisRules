
import numpy as np

class DistancePopularityModel():

    name = "DistancePopularity"

    def __init__(self, alpha=1, beta=1):
        self.alpha = alpha
        self.beta = beta
        self.axis = None 
        self.influence = None

    def set_beta(self, beta):
        self.beta = beta
    
    def set_alpha(self, alpha):
        self.alpha = alpha

    def __call__(self, m_candidates, n_voters):
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
                proba = np.exp(-self.alpha*distance)*(influence[j]*self.beta + 1-self.beta)
                if np.random.rand() < proba:
                    approval_ballots[i,j] = 1
        
        self.axis = axis 
        self.influence = influence 

        return approval_ballots


