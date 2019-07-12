import idea
import scientist
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
        ideas_last_tp = self.birth_new_ideas()
        self.set_perceived_rewards(ideas_last_tp)
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
    # returns the number of ideas from last tp
    def birth_new_ideas(self):
        for i in range(self.ideas_per_time):
            new_idea = idea.Idea(self)
            self.idea_list.append(new_idea)
        return len(self.idea_list) - self.ideas_per_time

    # loop through every scientist, appending their perceived rewards dataframe with new ideas
    # also updates related list with extra spots for new ideas --> append_scientist_lists
    def set_perceived_rewards(self, ideas_last_tp):
        for sci in self.scientist_list:
            # slice to iterate only through new ideas
            for i in self.idea_list[ideas_last_tp:]:
                # defining variables
                sci_mult_max = None  # random number from ND
                sci_mult_mean = None  # random number from ND
                idea_mean = sci_mult_mean * i.idea_mean
                idea_max = sci_mult_max * i.idea_max
                idea_k = sci.learning_speed * i.idea_k

                # adding to current df
                new_data = {'Idea Mean': idea_mean,
                            'Idea Max': idea_max,
                            'Idea K': idea_k}
                sci.perceived_rewards = sci.perceived_rewards.append(new_data, ignore_index=True)
            self.append_scientist_lists(sci)

    # data collection: loop through each idea object, updating the effort that was invested in this time period
    def update_objects(self):
        for idx, i in enumerate(self.idea_list):
            effort_invested_tp = 0
            k_paid_tp = 0
            for sci in self.scientist_list:
                effort_invested_tp += sci.idea_effort_tp[idx]
                k_paid_tp += sci.k_paid_tp[idx]
            i.total_effort += effort_invested_tp
            i.effort_by_tp.append(effort_invested_tp)
            i.num_k += k_paid_tp
            i.num_k_by_tp.append(k_paid_tp)

    # updates the lists within each scientist object to reflect the correct number of available ideas
    def append_scientist_lists(self, sci):
        sci.idea_eff_tp.append(0)
        sci.ideas_k_paid_tp.append(0)
        sci.ideas_eff_tot.append(0)
        sci.ideas_k_paid_tot.append(0)
