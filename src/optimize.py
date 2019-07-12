# optimize.py
import numpy as np
import pandas as pd


def investing_helper(sci, mod):  # sci = scientist object

    while sci.avail_effort > 0:
        # ARRAYS on cost for each idea
        sci.k = sci.learning_speed * np.asarray([i.idea_k for i in sci.idea_list])
        sci.curr_k = (np.asarray(sci.ideas_k_paid) == 0) * sci.k  # k_paid is 0 if scientist hasn't paid learning cost

        # SCALAR: increment based on ONLY ideas where a scientist is able
        # to invest research effort after entering learning barrier
        # +1 ensures that each idea a scientist works on will have at least 1 unit of marg effort
        sci.increment = max(sci.curr_k[np.where(sci.curr_k + 1 <= sci.avail_effort)]) + 1

        # ARRAY: marg effort for each idae
        sci.marg_eff = sci.increment - sci.curr_k

        if mod.config.switch == 0:
            idea_idx = greedy_returns(sci)
        elif mod.config.switch == 1:
            idea_idx = prob_returns(sci)
        else:
            idea_idx = smart_returns(sci)

    sci.idea_effort_tp[idea_idx] += sci.marg_eff[idea_idx]


def smart_returns(sci):
    return 1


def prob_returns(sci):
    return 1


def greedy_returns(sci):
    return 1
