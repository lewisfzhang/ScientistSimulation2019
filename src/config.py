import numpy as np


class Config:
    def __init__(self):
        self.seed = 123
        self.seed_array = None
        self.next_seed_idx = None
        self.set_seed()

        self.time_periods = 20
        self.ideas_per_time = 10
        self.sci_rate = 10
        self.tp_alive = 8

        # maybe make some of these proportions relative to the idea mean?
        self.idea_mean = 300
        self.idea_sds = 75
        self.idea_max = 100
        self.start_effort_mean = 150
        self.k_mean = 37
        self.learning_rate_mean = 1

        # self.learning_rate_mean = 1
        self.perceived_max_var = None
        self.perceived_mean_var = None

        self.equal_returns = True
        self.opt_num = 0

    def set_seed(self):
        np.random.seed(self.seed)
        self.seed_array = np.random.randint(100000, 999999, 10000000)  # initialize 10000000 random seeds
        self.next_seed_idx = 0  # keeps track of the last seed that was used

    def get_next_seed(self):
        self.next_seed_idx += 1
        if self.next_seed_idx == len(self.seed_array):
            self.next_seed_idx = 0  # loop back in the seed array
        return self.seed_array[self.next_seed_idx]
