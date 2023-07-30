from axisrules.rules import ScoringRule
from axisrules.misc import find_min, find_max

class BallotCompletionCircular(ScoringRule):
    """
    The Ballot Completion Circular rule compute the cycle which minimize the total number of candidates to add to voters' ballots
    for the profile to be linear.
    """

    name = "Ballot Completion Circular"
    circular = True
    
    def get_ballot_score(self, axis, votes, n_app):
        n_cand = len(axis)
        min_v = find_min(axis, votes)
        max_v = find_max(axis, votes)
        if not self.abstention:
            min_fill = (max_v-min_v+1-n_app)
            for i in range(min_v+1, max_v+1):
                if votes[axis[i]]:
                    max_v = min_v
                    min_v = i
                    min_fill = min(min_fill, (max_v+n_cand-min_v+1-n_app))
        else:
            min_fill = len([x for x in range(min_v+1, max_v) if votes[axis[x]] == -1])
            for i in range(min_v+1, max_v+1):
                if votes[axis[i]] == 1:
                    max_v = min_v
                    min_v = i
                    curr_fill = len([x for x in range(max_v) if votes[axis[x]] == -1]) + len([x for x in range(min_v+1, n_cand) if votes[axis[x]] == -1])
                    min_fill = min(min_fill, curr_fill)
        return min_fill
 