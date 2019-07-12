from numpy.random import poisson


class Idea:
    def __init__(self, model):
        self.idea_mean = poisson(lam=model.idea_mean)  # idea specific inflection point
        self.idea_max = poisson(lam=model.idea_max)  # idea specific maximum impact
        self.idea_k = poisson(lam=model.k_mean)  # idea specific learning cost
        self.create_idea_collectors()

    def create_idea_collectors(self):
        self.effort_by_tp = []  # total effort invested in idea by period
        self.num_k_by_tp = []  # number people who paid investment cost by period
        self.total_effort = 0  # total effort invested in idea to date
        self.num_k = 0  # number of researchers who have invested learning cost in idea
