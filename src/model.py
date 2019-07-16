import idea
import scientist
import functions as f


class Model:
    # initiates the key parameters within the model, as set in config
    # creates empty lists to track scientists and ideas; index indicates age
    def __init__(self, config):
        # SCALARS
        self.config = config
        self.num_sci = config.sci_rate
        self.time_periods = config.time_periods
        self.ideas_per_time = config.ideas_per_time
        self.tp_alive = config.tp_alive
        self.idea_mean = config.idea_mean
        self.idea_sds = config.idea_sds
        self.idea_max = config.idea_max
        self.start_effort_mean = config.start_effort_mean
        self.k_mean = config.k_mean
        self.learning_rate_mean = config.learning_rate_mean
        self.tp = 0  # first tp

        # ARRAYS
        self.scientist_list = []
        self.idea_list = []

    #  defines the process for one time period within the model
    def step(self):
        self.age_scientists()  # adds to the age of every existing scientist
        self.birth_new_scientists()  # creates a new cohort of scientists of age 0

        ideas_last_tp = self.birth_new_ideas()  # keep track of how many old ideas so we only have to update new ideas
        self.set_perceived_rewards(ideas_last_tp)  # update each scientist's perceived rewards to reflect new ideas

        for s in self.scientist_list:
            s.step()  # iterate through scientist step for every scientist, returning their investments

        self.update_objects()  # update the data collectors within the scientist and idea objects
        self.pay_out_returns()  # pay out the actual returns to scientists who invested in ideas

        self.tp += 1  # progress to the next time period

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

        if self.tp == 0:
            idx = 0  # index should be 0 because there are no previous ideas before tp = 0 (see set_perceived_rewards)
        else:
            idx = len(self.idea_list) - self.ideas_per_time
        return idx

    # loop through every scientist, appending their perceived rewards dataframe with new ideas
    # also updates related list with extra spots for new ideas --> append_scientist_lists
    def set_perceived_rewards(self, ideas_last_tp):
        for sci in self.scientist_list:
            # determining how many loops we need to run (for performance efficiency)
            if sci.age == 0:  # just born scientists need to update for all ideas
                new_idea_list = self.idea_list
            else:  # older scientists only need to update for new ideas
                new_idea_list = self.idea_list[ideas_last_tp:]

            # slice to iterate only through new ideas, setting up attributes and scientist perception
            for i in new_idea_list:
                self.append_scientist_lists(sci)  # add element to signal new idea for data collector variables

                # keeping all normal distributions for sci_mult to 0.3 range --> *** 0.1 sds ***
                # idea is that sci.idea_mult ranges from 0.5-1.5, so the worst case we get low end of 0.2
                sci_mult_max = f.get_normal_number(sci.idea_max_mult, 0.1, self.config)
                sci_mult_mean = f.get_normal_number(sci.idea_sds_mult, 0.1, self.config)
                sci_mult_sds = f.get_normal_number(sci.idea_mean_mult, 0.1, self.config)

                idea_mean = sci_mult_mean * i.idea_mean
                idea_sds = sci_mult_sds * i.idea_sds
                idea_max = sci_mult_max * i.idea_max
                idea_k = int(sci.learning_speed * i.idea_k)  # k must be integer!

                # adding to current dict
                sci.perceived_rewards['Idea Mean'].append(idea_mean)
                sci.perceived_rewards['Idea SDS'].append(idea_sds)
                sci.perceived_rewards['Idea Max'].append(idea_max)
                sci.perceived_rewards['Idea K'].append(idea_k)

    # updates the lists within each scientist object to reflect the correct number of available ideas
    # ignore static warning, only because we aren't using self keyword
    # keep it in model since it is called by the model step function --> set_perceived_rewards()
    def append_scientist_lists(self, sci):  # according to %timeit, .append() is actually very fast, no need to worry
        sci.idea_eff_tp.append(0)
        sci.idea_eff_tot.append(0)
        sci.ideas_k_paid_tp.append(0)
        sci.ideas_k_paid_tot.append(0)
        sci.returns_tp.append(0)
        sci.returns_tot.append(0)

    # data collection: loop through each idea object, updating the effort that was invested in this time period
    def update_objects(self):
        for idx, i in enumerate(self.idea_list):
            effort_invested_tp = 0
            k_paid_tp = 0  # number of scientists who learned the idea in this tp
            for sci in self.scientist_list:
                effort_invested_tp += sci.idea_eff_tp[idx]
                k_paid_tp += sci.ideas_k_paid_tp[idx]
            i.total_effort += effort_invested_tp
            i.effort_by_tp.append(effort_invested_tp)
            i.num_k_by_tp.append(k_paid_tp)

    # determine who gets paid out based on the amount of effort input
    def pay_out_returns(self):
        for idx, i in enumerate(self.idea_list):
            if i.effort_by_tp[self.tp] != 0:  # only ideas that were invested matter? check!
                last_index = len(i.effort_by_tp) - 1  # to get total effort since last tp
                start_effort = i.total_effort - sum(i.effort_by_tp[0:last_index])  # sum all effort before this tp
                idea_return = idea.get_returns(i.idea_mean, i.idea_sds, i.idea_max, start_effort, start_effort+i.total_effort)
                self.process_winners(idx, idea_return)  # process the winner for each idea, one per loop

        for sci in self.scientist_list:
            tp_returns = sum(sci.returns_tp)
            sci.overall_returns_tp.append(tp_returns)

    # processes winners for idea with index iidx
    def process_winners(self, iidx, returns):
        list_of_investors = []
        for sidx, sci in enumerate(self.scientist_list):
            if sci.idea_eff_tp[iidx] != 0:
                list_of_investors.append(sidx)

        if self.config.equal_returns:  # each scientist receives returns proportional to effort
            total_effort_invested = 0
            for sci_id in list_of_investors:
                sci = self.scientist_list[sci_id]
                total_effort_invested += sci.idea_eff_tp[iidx]
            for sci_id in list_of_investors:
                sci = self.scientist_list[sci_id]
                individual_proportion = float(sci.idea_eff_tp[iidx] / total_effort_invested)
                individual_returns = round(individual_proportion * total_effort_invested)
                sci.returns_tp[iidx] += individual_returns
                sci.returns_tot[iidx] += individual_returns

        else:
            oldest_scientist_id = list_of_investors[0]  # scientist born "earliest" in same tp should come first in list
            sci = self.scientist_list[oldest_scientist_id]
            sci.returns_tp[iidx] += returns
            sci.returns_tot[iidx] += returns
