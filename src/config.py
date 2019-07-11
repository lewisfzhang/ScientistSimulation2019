class Config:
    def __init__(self):
        self.seed = 123
        self.time_periods = 20
        self.ideas_per_time = 10
        self.sci_rate = 10
        self.tp_alive = 8

        self.idea_mean = 300
        self.idea_max = 100
        self.start_effort_mean = 150
        self.k_mean = 37

        self.learning_rate_mean = 1
        self.perceived_max_var = None
        self.perceived_mean_var = None

        self.equal_returns = True
        self.opt_num = 1
