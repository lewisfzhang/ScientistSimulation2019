import pandas as pd
import numpy as np

class Scientist:
    def __init__(self):
        self.age = 0
        self.learning_speed = None
        self.idea_max_var = None
        self.idea_mean_var = None
        self.start_effort = None
        self.available_effort = None
        self.perceived_rewards = pd.DataFrame(columns=['Idea Mean', 'Idea Max', 'Idea K'])
        self.ideas_invested_in = []
        self.idea_effort_tp = []
        self.idea_eff_tot = []
        return

    def step(self):
        return