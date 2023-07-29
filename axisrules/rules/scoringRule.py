from axisrules.rules import AxisRule

class ScoringRule(AxisRule):
    """
    Class for the special family of Axis Rules which consist in each voter giving a cost to an axis and selecting
    the axis with minimal cost.
    """

    def get_ballot_score(self, axis, votes, n_app):
        raise NotImplementedError

    def get_individual_scores(self, axis, matrix):
        scores_tab = []
        for ballot in matrix:
            n = ballot[-1]
            n_app = ballot[-2]
            votes = ballot[:-2]
            score = self.get_ballot_score(axis, votes, n_app)
            scores_tab.extend([score]*n)
        return scores_tab

    def _get_score(self, axis, matrix, current_min):
        score = 0
        for ball in matrix:
            n = ball[-1]
            n_app = ball[-2]
            votes = ball[:-2]
            score += n*self.get_ballot_score(axis, votes, n_app)

            if current_min is not None and score > current_min:
                return score, False
        return score, True