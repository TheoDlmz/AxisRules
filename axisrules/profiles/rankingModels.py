
import numpy as np

## Code taken from mapel library




class RankingDistanceModel():

    name = "RankingDistance"

    def __init__(self, sigma=0.5, radius=0.3):
        self.sigma = sigma
        self.radius = radius
    
    def __call__(self, m_candidates, n_voters):
        candidates = np.random.rand(m_candidates)
        axis = np.argsort(candidates)
        self.axis = axis
        # Positions of the voters
        voters = np.random.rand(n_voters)
        ranking_votes = np.zeros((n_voters, m_candidates))
        approval_votes = np.zeros((n_voters, m_candidates))
        for i in range(n_voters):
            seen_positions = candidates + np.random.normal(0, self.sigma, m_candidates)
            voter_position = voters[i]
            distances = abs(seen_positions - voter_position)
            ranking = np.argsort(distances)
            positions= np.argsort(ranking)+1
            ranking_votes[i,:] = positions
            for j in range(m_candidates):
                if distances[j] < self.radius:
                    approval_votes[i,j] = 1

        return ranking_votes, approval_votes
