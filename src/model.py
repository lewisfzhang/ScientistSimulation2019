import idea.py
import scientist.py
import pandas as pd

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
        for s in self.scientist_list:
            s.step()
        self.update_objects()

    # adds one year to the age of every scientist that already exists within the model
    def age_scientists(self):
        for sci in self.scientist_list:
            sci.age = sci.age + 1

    # creates new scientists, birthed at age 0, and sets their random constants (variances, learning speed, and effort
    def birth_new_scientists(self):
        for i in range(self.num_sci):
            new_scientist = scientist.Scientist(self)
            self.scientist_list.append(new_scientist)

    # creates new ideas and sets their random constants (true mean, true max, investment cost)
    def birth_new_ideas(self):
        for i in range(self.ideas_per_time):
            new_idea = idea.Idea(self)
            self.idea_list.append(new_idea)

    # loop through every scientist, appending their perceived rewards dataframe with new ideas
    def set_perceived_rewards(self):
        for s in self.scientist_list:
            scientist.Scientist = self.scientist_list[s]
            df = scientist.perceived_rewards
            for idx, i in enumerate(self.idea_list):
                if idx not in df.index:
                    sci_mult_max = None  # random number from ND
                    sci_mult_mean = None  # random number from ND
                    idea_mean = sci_mult_mean * i.idea_mean
                    idea_max = sci_mult_max * i.idea_max
                    idea_k = scientist.learning_speed * i.idea_k
                    df.append(idx, idea_mean, idea_max, idea_k)
                    append_scientist_list(scientist)

    # data collection: loop through each idea object, updating the effort that was invested in this time period
    def update_objects(self):
        for i in self.idea_list:
            idea = self.idea_list[i]
            effort_invested_tp = 0
            k_paid_tp = 0
            for s in self.scientist_list:
                scientist = self.scientist_list[s]
                effort_invested_tp += scientist.idea_eff_tp[i]
                k_paid_tp += scientist.k_paid_tp[i]
            idea.total_effort += effort_invested_tp
            idea.effort_by_tp.append(effort_invested_tp)
            idea.num_k += k_paid_tp
            idea.num_k_by_tp.append(k_paid_tp)

    # updates the lists within each scientist object to reflect the correct number of available ideas
    def append_scientist_list(s):
        scientist = s.Scientist
        scientist.idea_eff_tp.append(0)
        scientist.ideas_k_paid_tp.append(0)
        scientist.idea_eff_tot.append(0)
        scientist.idea_k_paid_tot(0)