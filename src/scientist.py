import pandas as pd
import numpy as np
from numpy.random import poisson
import functions as f
import optimize


class Scientist:
    def __init__(self, model):
        self.model = model
        self.age = 0  # SCALAR: age of the given scientists, initiated at 0 years when entered into model

        # SCALAR: multiplier determining scientist specific K (idea K * learning speed = specific k)
        # learning speed is CONSTANT for all ideas for a scientist
        self.learning_speed = poisson(lam=self.model.learning_rate_mean)

        # some scientists will be more optimistic than others
        self.idea_max_mult = f.get_random_number(0.5, 1.5)  # SCALAR: multiplier determining max perceived returns
        self.idea_mean_mult = f.get_random_number(0.5, 1.5)  # SCALAR: multiplier determining perceived lambda

        self.start_effort = poisson(lam=self.model.start_effort_mean)  # SCALAR: determines starting effort for a scientist in all periods
        self.avail_effort = self.start_effort  # SCALAR: counter that determines how much effort a scientist has left to allocate within TP
        self.perceived_rewards = pd.DataFrame(columns=['Idea Mean', 'Idea Max', 'Idea K'])  # tracks perceived rewards

        # data collection: creates lists to track investment within and across time periods
        self.idea_eff_tp = []  # tracks the effort to be invested across different ideas within time period
        self.ideas_k_paid_tp = []  # records which ideas the scientist paid investment cost for this period
        self.idea_eff_tot = []  # tracks the total effort invested in each idea by the scientist
        self.ideas_k_paid_tot = []  # records which ideas the scientist has paid the investment cost for overall

    def step(self):
        # reset time period trackers to all zeros
        self.idea_eff_tp.clear()
        self.idea_k_paid_tp.clear()

        # scientist is still active
        if self.age < self.model.tp_alive:
            self.avail_effort = self.start_effort
            df = optimize.investing_helper(self, self.model)
        # loop through all investments made within time period
        for idx in df.index:
            idea_index = df.iloc[idx, 'idea_idx']
            self.idea_eff_tp[idea_index] += df.iloc[idx, 'marg_eff']  # update this period marginal effort per idea
            self.idea_k_paid_tp[idea_index] += df.iloc[idx, 'k_paid']  # update which ideas had investment costs paid
        for i in self.ideas_eff_total:
            self.idea_eff_tot[i] += self.idea_eff_tp[i]
        for j in self.ideas_k_pad_tot:
            self.ideas_k_paid_tot[j] += self.ideas_k_paid_tp[j]

