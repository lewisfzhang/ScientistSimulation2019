import idea
import scientist
from numpy.random import poisson


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
        self.birth_new_ideas()
        self.set_perceived_rewards

    def age_scientists(self):
        for sci in self.scientist_list:
            sci.age = sci.age + 1

    def birth_new_scientists(self):
        for i in range(self.num_sci):
            new_scientist = scientist.Scientist()
            new_scientist.age = 0
            new_scientist.learning_speed = poisson(lam=self.learning_rate_mean)
            new_scientist.idea_max_var = poisson(lam=self.perceived_max_var)
            new_scientist.idea_mean_var = poisson(lam=self.perceived_mean_var)
            new_scientist.start_effort = poisson(lam=self.start_effort_mean)
            self.scientist_list.append(new_scientist)

    def birth_new_ideas(self):
        for i in range(self.ideas_per_time):
            new_idea = idea.Idea()
            new_idea.idea_mean = poisson(lam=self.idea_mean)
            new_idea.idea_max = poisson(lam=self.idea_max)
            new_idea.idea_k = poisson(lam=self.k_mean)
            new_idea.total_effort = 0
            new_idea.num_k = 0
            self.idea_list.append(new_idea)

    def set_perceived_rewards(self):
        for i in range(self.scientist_list):
            scientist = self.scientist_list[i]
            for j in range(self.idea_list):
                idea = self.idea_list[i]

