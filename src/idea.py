from numpy.random import poisson
import numpy as np


class Idea:
    def __init__(self, model):
        self.idea_mean = poisson(lam=model.idea_mean)  # idea specific inflection point
        self.idea_max = poisson(lam=model.idea_max)  # idea specific maximum impact
        self.idea_sds = poisson(lam=model.idea_sds) # idea specific SDS
        self.idea_k = poisson(lam=model.k_mean)  # idea specific learning cost
        self.create_idea_collectors(model.tp)

    def create_idea_collectors(self, tp):
        self.total_effort = 0  # total effort invested in idea to date, also accessed by optimization algorithms
        self.effort_by_tp = [0] * tp  # total effort invested in idea by period
        self.num_k = 0  # number of researchers who have invested learning cost in idea
        self.num_k_by_tp = [0] * tp  # number people who paid investment cost by period


# helper functions for calculating idea curve
def get_returns(means, sds, maxx, start_idx, end_idx):
    start = maxx * logistic_cdf(start_idx, loc=means, scale=sds)
    end = maxx * logistic_cdf(end_idx, loc=means, scale=sds)
    return end-start  # returns type FLOAT


def old_logistic_cdf(x, loc, scale):
    return 1 / (1 + np.exp((loc - x) / scale))


# normalizing so that all idea curves start at (0,0)
def logistic_cdf(x, loc, scale):
    return (old_logistic_cdf(x, loc, scale) - old_logistic_cdf(0, loc, scale)) / (
                1 - old_logistic_cdf(0, loc, scale))