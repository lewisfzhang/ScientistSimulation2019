from numpy.random import poisson
import numpy as np


class Idea:
    def __init__(self, model):
        self.idea_mean = poisson(lam=model.idea_mean)  # idea specific inflection point
        self.idea_max = poisson(lam=model.idea_max)  # idea specific maximum impact
        self.idea_sds = poisson(lame=model.idea_sds) # idea specific SDS
        self.idea_k = poisson(lam=model.k_mean)  # idea specific learning cost
        self.create_idea_collectors()

    def create_idea_collectors(self):
        self.effort_by_tp = []  # total effort invested in idea by period
        self.num_k_by_tp = []  # number people who paid investment cost by period
        self.total_effort = 0  # total effort invested in idea to date
        self.num_k = 0  # number of researchers who have invested learning cost in idea


# helper functions for calculating idea curve
def get_returns(self, means, sds, max, start_idx, end_idx):
    start = max * logistic_cdf(start_idx, loc=means, scale=sds)
    end = max * logistic_cdf(end_idx, loc=means, scale=sds)
    return end - start


def old_logistic_cdf(x, loc, scale):
    return 1 / (1 + np.exp((loc - x) / scale))


# normalizing so that all idea curves start at (0,0)
def logistic_cdf(x, loc, scale):
    return (old_logistic_cdf(x, loc, scale) - old_logistic_cdf(0, loc, scale)) / (
                1 - old_logistic_cdf(0, loc, scale))