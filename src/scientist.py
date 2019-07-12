import pandas as pd
import numpy as np


class Scientist:
    def __init__(self, model):
        self.model = model
        self.age  # age of the given scientists, initiated at 0 years when entered into model
        self.learning_speed  # multiplier determining scientist specific K (idea K * learning speed = specific k)
        self.idea_max_var  # variance determining max perceived returns
        self.idea_mean_var  # variance determining perceived lambda
        self.start_effort  # determines starting effort for a scientist in all periods
        self.available_effort  # counter that determines how much effort a scientist has left to allocate within TP
        self.perceived_rewards = pd.DataFrame(columns=['Index', 'Idea Mean', 'Idea Max', 'Idea K'])  # tracks perceived rewards
        self.ideas_k_paid = []  # records which ideas the scientist has paid the investment cost for
        self.idea_effort_tp = []  # tracks the effort to be invested across different ideas within time period
        self.idea_eff_tot = []  # tracks the total effort invested in each idea by the scientist
        return

    def step(self):
        return
