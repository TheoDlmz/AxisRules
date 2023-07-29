from axisrules.rules import ScoringRule
from axisrules.misc import find_min, find_max

class ForbiddenTriples(ScoringRule):
    """
    The Forbidden Triples rule compute the axis which minimize the number of forbidden triples 
    (a<b<c, a and c are approved, b is not approved).
    """
    name = "Forbidden Triples"
    
    def get_ballot_score(self, axis, votes, n_app):
        min_v = find_min(axis, votes)
        max_v = find_max(axis, votes)
        count_before = 0
        for i in range(min_v, max_v):
            if not votes[axis[i]]:
                return count_before*(n_app-count_before)
            else:
                count_before += 1
    