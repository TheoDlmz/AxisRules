from axisrules.rules import ScoringRule
from axisrules.misc import find_min, find_max

class VoterDeletionCircular(ScoringRule):
    """
    The Voter Deletion Circular rule compute the cycle which minimize the total number of voter 
    to delete for the profile to be linear.
    """

    name = "Voter Deletion Circular"
    circular = True
    
    def get_ballot_score(self, axis, votes, n_app):
        n_cand = len(axis)
        min_v = find_min(axis, votes)
        max_v = find_max(axis, votes)
        found = False
        if not self.abstention:
            if (max_v-min_v+1-n_app) == 0:
                found = True
            else:
                count_el = 0
                for i in range(max_v+1):
                    if votes[axis[i]]:
                        count_el += 1
                    else:
                        break 
                for i in range(n_cand-1, min_v-1, -1):
                    if votes[axis[i]]:
                        count_el += 1
                    else:
                        break
                
                if count_el == n_app:
                    found = True
        else:
            found = True
            for i in range(min_v+1, max_v):
                if votes[axis[i]] == -1:
                    found = False
            
            count_el = 0
            for i in range(max_v+1):
                if votes[axis[i]] == 1:
                    count_el += 1
                elif votes[axis[i]] == -1:
                    break 
            for i in range(n_cand-1, min_v-1, -1):
                if votes[axis[i]]== 1:
                    count_el += 1
                elif votes[axis[i]] == -1:
                    break
                
            if count_el == n_app:
                found = True


        if not found:
            return 1
        return 0
    