import pandas as pd
import numpy as np


class Scientist:
    def __init__(self, model):
        self.model = model
        self.age
        self.learning_speed
        self.idea_max_var
        self.idea_mean_var
        self.start_effort
        self.available_effort
        self.perceived_rewards = pd.DataFrame(columns=['Idea Mean', 'Idea Max', 'Idea K'])
        self.ideas_k_paid = []
        self.idea_effort_tp = []
        self.idea_eff_tot = []
        return

    def step(self):
        return
