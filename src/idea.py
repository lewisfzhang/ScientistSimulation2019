class Idea:
    def __init__(self):
        self.idea_mean  # idea specific inflection point
        self.idea_max  # idea specific maximum impact
        self.idea_k  # idea specific learning cost

    def create_idea_collectors(self):
        self.effort_by_tp = []  # total effort invested in idea by period
        self.num_k_by_tp = []  # number people who paid investment cost by period
        self.total_effort  # total effort invested in idea to date
        self.num_k  # number of researchers who have invested learning cost in idea

    def step(self):
        return
