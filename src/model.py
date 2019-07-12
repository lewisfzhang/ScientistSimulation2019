import idea
import scientist
import pandas as pd
from numpy.random import poisson


class Model:
    # initiates the key parameters within the model, as set in config
    # creates empty lists to track scientists and ideas; index indicates age
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

    #  defines the process for one time period within the model
    def step(self):
        self.age_scientists()
        self.birth_new_scientists()
        self.birth_new_ideas()
        self.set_perceived_rewards()

    # adds one year to the age of every scientist that already exists within the model
    def age_scientists(self):
        for sci in self.scientist_list:
            sci.age = sci.age + 1

    # creates new scientists, birthed at age 0, and sets their random constants (variances, learning speed, and effort
    def birth_new_scientists(self):
        for i in range(self.num_sci):
            new_scientist = scientist.Scientist()
            self.scientist_list.append(new_scientist)

    # creates new ideas and sets their random constants (true mean, true max, investment cost)
    def birth_new_ideas(self):
        for i in range(self.ideas_per_time):
            new_idea = idea.Idea()
            # put this in the constructor
            new_idea.idea_mean = poisson(lam=self.idea_mean)
            new_idea.idea_max = poisson(lam=self.idea_max)
            new_idea.idea_k = poisson(lam=self.k_mean)
            new_idea.total_effort = 0
            new_idea.num_k = 0
            self.idea_list.append(new_idea)

    # loop through every idea
    def set_perceived_rewards(self):
        for i in self.scientist_list:
            scientist = self.scientist_list[i]
            df = scientist.perceived_rewards
            for j in self.idea_list:
                idea = self.idea_list[j]
                if j not in df.index:
                    asd








