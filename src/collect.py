import pandas as pd
import numpy as np
import idea
class Collect:
    def __init__(self, model):
        self.m = model

    def collect_data(self):
        # for scientists
        sci_returns_tot = [sci.returns_tot for sci in self.m.scientist_list]  # Total returns by idea, DataFrame
        sci_overall_returns_tp = [sci.overall_returns_tp for sci in
                                  self.m.scientist_list]  # Overall returns by time period, DataFrame
        sci_ideas_k_paid_tot = [sci.ideas_k_paid_tot for sci in self.m.scientist_list]  # Ideas invested in, DataFrame
        sci_returns_tot_cum = [sum(sci.returns_tot) for sci in self.m.scientist_list]  # Overall returns, Array

        sci_returns_tot_df = self.array2d_to_df(sci_returns_tot, row_name='sci', col_name='idea', file_name='sci_returns_tot')
        sci_overall_returns_tp_df = self.array2d_to_df(sci_overall_returns_tp, row_name='sci', col_name='tp',
                                                    file_name='sci_ideas_k_paid_tot')
        sci_ideas_k_paid_tot_df = self.array2d_to_df(sci_ideas_k_paid_tot, row_name='sci', col_name='idea',
                                                  file_name='sci_ideas_k_paid_tot')
        self.arrays_to_html([sci_returns_tot_cum], ['sci_returns_tot_cum'],
                         'scientist')  # if more than one element, create a list of variables

        # for ideas
        idea_effort_by_tp = [i.effort_by_tp for i in self.m.idea_list]  # Effort by time period, DataFrame
        idea_num_k_by_tp = [i.num_k_by_tp for i in self.m.idea_list]  # Number of researchers by time period, DataFrame
        idea_total_effort = [i.total_effort for i in self.m.idea_list]  # Total effort, Array
        idea_num_k = [sum(i.num_k_by_tp) for i in self.m.idea_list]  # Number of researchers, Array
        idea_sci_impact = [idea.get_returns(i.idea_mean, i.idea_sds, i.idea_max, 0, i.total_effort) for i in
                           self.m.idea_list]  # Total scientific impact, based on point on the idea curve, Array
        idea_inflect_tp = [self.sum_point_array(i.effort_by_tp, i.idea_mean) for i in
                           self.m.idea_list]  # Time period where lambda was reached, Array --> at mean?

        idea_effort_by_tp_df = self.array2d_to_df(idea_effort_by_tp, row_name='idea', col_name='tp',
                                               file_name='idea_effort_by_tp')
        idea_num_k_by_tp_df = self.array2d_to_df(idea_num_k_by_tp, row_name='idea', col_name='tp',
                                              file_name='idea_num_k_by_tp')
        self.arrays_to_html([idea_total_effort, idea_num_k, idea_sci_impact, idea_inflect_tp],
                         ['idea_total_effort', 'idea_num_k', 'idea_sci_impact', 'idea_inflect_tp'], 'idea')

    def arrays_to_html(self, arr, row_names, file_name):  # takes list of arrays
        df = pd.DataFrame(data=arr, index=row_names, columns=pd.Index(np.arange(len(arr[0])), name=file_name))
        df = df.round(2)
        df = df.transpose()
        df.to_html('../out/{}_arrays_df.html'.format(file_name))


    def array2d_to_df(self, arr, row_name='row', col_name='col', file_name='unnamed_df'):
        i = pd.Index(np.arange(len(arr)), name=row_name)
        c = pd.Index(np.arange(len(arr[0])), name=col_name)
        df = pd.DataFrame(data=arr, index=i, columns=c)
        df.to_html('../out/{}_df.html'.format(file_name))
        return df


    # returns index where cumulative sum starting from index 0 is greater or equal to "target" sum
    def sum_point_array(self, arr, target):
        curr_sum = 0
        for idx, val in enumerate(arr):
            curr_sum += val
            if curr_sum >= target:
                return idx
        return -1  # not found