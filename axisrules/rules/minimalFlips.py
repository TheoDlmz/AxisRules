from axisrules.rules import ScoringRule
from axisrules.misc import find_min, find_max

class MinimalFlips(ScoringRule):
    """
    The Minimal Flips rule compute the axis which minimize the total number of flips (adding/deleting candidates
    from approval ballots) for the profile to be linear.
    """

    name = "Minimal Flips"
    
    def get_ballot_score(self, axis, votes, n_app):
        list_approved = [i for i in range(len(axis)) if votes[axis[i]]]
        min_val = len(axis)
        for i in range(len(list_approved)-1):
            for j in range(i+1, len(list_approved)):
                x = i + (len(list_approved)-j-1) 
                    
                if not self.abstention:
                    x += (list_approved[j]-list_approved[i]) -  (j-i)
                else:
                    for k in range(list_approved[i]+1, list_approved[j]):
                        if votes[axis[k]] == -1:
                            x += 1
                # flips 1->0 before, flips 1->0 after, flips 0->1 in between
                if x < min_val:
                    min_val = x
        return min_val