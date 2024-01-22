
import numpy as np

class SamplingModel():

    def __init__(self, votes, weights=None):
        self.votes = votes
        self.weights = weights
        if weights is None:
            self.weights = np.ones(len(votes))

    def __call__(self, m_candidates, n_voters):
        # choose m_candidates and n_voters from the profile 
        profile_n, profile_m = self.votes.shape
        if m_candidates > profile_m:
            raise ValueError("m_candidates should be less than the number of candidates in the profile")
        if n_voters > profile_n:
            raise ValueError("n_voters should be less than the number of voters in the profile")
        
        candidates = np.random.choice(profile_m, m_candidates, replace=False)
        voters = np.random.choice(profile_n, n_voters, replace=False)

        profile = self.votes[voters,:][:,candidates]
        weights = self.weights[voters]

        return profile, weights


