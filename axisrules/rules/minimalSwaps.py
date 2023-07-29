from axisrules.rules import ScoringRule
from axisrules.misc import find_min, find_max

class MinimalSwaps(ScoringRule):
    """
    The Minimal Swaps rule compute the axis which minimize the sum of the number of swaps of two
    adjacent candidates in the axis required for an approval ballot to be an interval of the axis.
    """

    name = "Minimal Swaps"
    
    def get_ballot_score(self, axis, votes, n_app):
        min_v = find_min(axis, votes)
        max_v = find_max(axis, votes)
        count_before = 0
        for i in range(min_v, max_v):
            if not votes[axis[i]]:
                return min(count_before, n_app-count_before)
            else:
                count_before += 1