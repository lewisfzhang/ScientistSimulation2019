class Model:
    def __init__(self, config):
        self.num_sci = config.sci_rate
        self.time_periods = config.time_periods
        self.ideas_per_time = config.ideas_per_time
        self.tp_alive = config.tp_alive
        self.idea_mean = config.idea_mean
        self.idea_max = config.idea_max
        self.start_effort_mean = config.start_effort_mean
        self.k_mean = config.k_mean
        self.scientist_list = []
        self.idea_list = []

    def step(self):
        self.age_scientists()
        self.birth_new_scientists()

    def age_scientists(self):
        for sci in self.scientist_list:
            sci.age = sci.age+1

    def birth_new_scientists(self):
