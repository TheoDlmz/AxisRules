from axisrules.rules import AxisRule
from axisrules.misc import compute_weighted_matrix, reduce_weighted_matrix, init_model
import numpy as np



class SequentialScoringRule(AxisRule):
    """
    Class for the special family of Axis Rules which consist in each voter giving a cost to an axis and selecting
    the axis with minimal cost.
    """

    def _matrix_coapproval(self, matrix):

        n, m =self.profile.shape
        coapproval = np.zeros((m,m))
        for i in range(m):
            for j in range(i+1,m):
                    for k in range(len(matrix)):
                        if matrix[k][i] == matrix[k][j]:
                            coapproval[i][j] += matrix[k][-1]
                            coapproval[j][i] += matrix[k][-1]
        return coapproval/n
    
    def _get_partial_cost(self, axis, matrix):
        raise NotImplementedError


    def __call__(self):
        votes = self.profile
        weights = self.weights
        _, n_candidates = np.array(votes).shape
        matrix = compute_weighted_matrix(votes, n_candidates, weights)
        matrix_coapp = self._matrix_coapproval(matrix)

        v = matrix_coapp.ravel().argmax()
        v_x, v_y = np.unravel_index(v, matrix_coapp.shape)
        axis_out = [v_x, v_y]

        n, m = votes.shape
        for k in range(m-2):
            on_left = np.ones(m)*m*n
            on_right = np.ones(m)*m*n
            for i in range(m):
                if i not in axis_out:
                    tested_axis = [i] + axis_out
                    on_left[i] = self._get_partial_cost(tested_axis, matrix) 
                    tested_axis = axis_out + [i]
                    on_right[i] = self._get_partial_cost(tested_axis, matrix) 

            if np.min(on_left) < np.min(on_right):
                v = np.argmin(on_left)
                axis_out = [v] + axis_out
            else:
                v = np.argmin(on_right)
                axis_out = axis_out + [v]
        return axis_out