import pandas as pd
from numpy.random import poisson
import functions as f
import optimize


class Scientist:
    def __init__(self, model):
        self.model = model
        self.age = 0  # SCALAR: age of the given scientists, initiated at 0 years when entered into model

        # SCALAR: multiplier determining scientist specific K (idea K * learning speed = specific k)
        # learning speed is CONSTANT for all ideas for a scientist --> 'lam' centered around 1
        self.learning_speed = poisson(lam=10*self.model.learning_rate_mean)/10

        # some scientists will be more optimistic than others
        self.idea_max_mult = f.get_random_float(0.5, 1.5, self.model.config)  # SCALAR: multiplier determining max perceived returns
        self.idea_sds_mult = f.get_random_float(0.5, 1.5, self.model.config) # SCALAR: multiplier determining sds of perceived returns
        self.idea_mean_mult = f.get_random_float(0.5, 1.5, self.model.config)  # SCALAR: multiplier determining perceived lambda

        self.start_effort = poisson(lam=self.model.start_effort_mean)  # SCALAR: determines starting effort for a scientist in all periods
        self.avail_effort = self.start_effort  # SCALAR: counter that determines how much effort a scientist has left to allocate within TP
        self.perceived_rewards = {'Idea Mean': [], 'Idea SDS': [], 'Idea Max': [], 'Idea K': []}  # tracks perceived rewards

        # data collection: creates lists to track investment within and across time periods
        self.idea_eff_tp = []  # tracks the effort to be invested across different ideas within time period
        self.idea_eff_tot = []  # tracks the total effort invested in each idea by the scientist
        # k_paid: 0 = haven't learned, 1 = already paid learning cost
        self.ideas_k_paid_tp = []  # records which ideas the scientist paid investment cost for this period
        self.ideas_k_paid_tot = []  # records which ideas the scientist has paid the investment cost for overall
        self.returns_tp = []  # tracks the returns by idea within time period for the scientist
        self.returns_tot = []  # records the sum of returns the scientist has accrued for each idea
        self.overall_returns = 0

    def step(self):
        self.reset_trackers()

        # scientist is still active
        if self.age < self.model.tp_alive:
            self.avail_effort = self.start_effort  # reset avail_effort each time period

            inv_dict = optimize.investing_helper(self)

            self.update_trackers(inv_dict)

    def reset_trackers(self):
        # reset time period trackers to all zeros
        self.idea_eff_tp = [0] * len(self.idea_eff_tp)
        self.ideas_k_paid_tp = [0] * len(self.ideas_k_paid_tp)

    def update_trackers(self, inv_dict):
        # loop through all investments made within time period
        for idx, idea_index in enumerate(inv_dict['idea_idx']):
            self.idea_eff_tp[idea_index] += inv_dict['marg_eff'][idx]  # update this period marginal effort per idea
            self.ideas_k_paid_tp[idea_index] += inv_dict['k_paid'][idx]  # update which ideas had investment costs paid IN THIS TP

        # updates "tot"/across time variables with data from corresponding tp variables
        for idx, val in enumerate(self.idea_eff_tp):
            self.idea_eff_tot[idx] += val
        for idx, val in enumerate(self.ideas_k_paid_tp):
            self.ideas_k_paid_tot[idx] += val
