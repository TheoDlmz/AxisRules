from axisrules.rules import ScoringRule
from axisrules.misc import find_min, find_max, compute_scores

class VoterDeletionThreshold(ScoringRule):
    """
    The Voter Deletion Threshold rule compute the axis which minimize the total number of voter 
    to delete for the profile to be linear.  It varies from
    the classical Voter Deletion rule in that for a given voter, it does not consider candidates
    with a lower score than the lowest score of an approved candidate by the voter.
    """

    name = "Voter Deletion Threshold"

    def __init__(self, profile, weights=None):
        super().__init__(profile, weights)
        self.scores = compute_scores(profile, weights)

    def set_profile(self, profile, weights=None):
        self.scores = compute_scores(profile, weights)
        return super().set_profile(profile, weights)
    
    
    def get_ballot_score(self, axis, votes, n_app):
        min_v = find_min(axis, votes)
        max_v = find_max(axis, votes)
        min_score = min([self.scores[axis[i]] for i in range(min_v, max_v+1) if votes[axis[i]]])
        real_holes = sum([1 for i in range(min_v, max_v+1) if not votes[axis[i]] and self.scores[axis[i]] > min_score])
        if real_holes > 0:
            return 1
        return 0
    