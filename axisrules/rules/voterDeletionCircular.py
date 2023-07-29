from axisrules.rules import ScoringRule
from axisrules.misc import find_min, find_max

class VoterDeletionCircular(ScoringRule):

    name = "Voter Deletion Circular"
    circular = True
    
    def get_ballot_score(self, axis, votes, n_app):
        n_cand = len(axis)
        min_v = find_min(axis, votes)
        max_v = find_max(axis, votes)
        found = False
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


        if not found:
            return 1
        return 0
    