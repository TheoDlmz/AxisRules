import numpy as np

class AxisRule(object):
    """
    General Class for Axis Rules
    """
    name = None
    circular = False

    def __init__(self, profile, weights=None, abstention=False):
        self.profile = np.array(profile)
        self.weights = weights
        self.abstention = abstention

    def set_profile(self, profile, weights=None):
        self.profile = np.array(profile)
        self.weights = weights

 

    def __str__(self):
        return self.name
