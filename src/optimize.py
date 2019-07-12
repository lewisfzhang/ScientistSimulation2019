# optimize.py
import numpy as np
import pandas as pd


def investing_helper(sci, mod):

    # df that keeps track of scientist's transactions within current time period
    # for k_paid: 0 if already paid, # 1 if paid this period
    df = pd.DataFrame(columns=['idea_idx', 'marg_eff', 'k_paid'])

    while sci.avail_effort > 0:
        # ARRAYS on cost for each idea
        sci.k = sci.learning_speed * np.asarray([i.idea_k for i in sci.idea_list])
        # k_paid is 0 if scientist hasn't paid learning cost
        # True = 1, False = 0 --> so if scientist hasn't paid learning cost, curr_k = 1 * sci.k
        sci.curr_k = (np.asarray(sci.ideas_k_paid_tot) == 0) * sci.k

        # SCALAR: increment based on ONLY ideas where a scientist is able
        # to invest research effort after entering learning barrier
        # +1 ensures that each idea a scientist works on will have at least 1 unit of marg effort
        sci.increment = max(sci.curr_k[np.where(sci.curr_k + 1 <= sci.avail_effort)]) + 1

        # ARRAY: marg effort for each idea
        sci.marg_eff = sci.increment - sci.curr_k

        if mod.config.switch == 0:
            idea_idx = greedy_returns(sci, mod)
        elif mod.config.switch == 1:
            idea_idx = prob_returns(sci, mod)
        else:
            idea_idx = smart_returns(sci, mod)

        # checks if idea_idx is already in the df
        if idea_idx in df['idea_idx'].values:
            row_data = df.loc[df['idea_idx' == idea_idx]]
            transaction_df = df.drop(df.index[df['idea_idx'] == idea_idx][0])
            # 0 because adding to current row, idea_idx should stay the same
            # for k_paid, same logic as sci.curr_k calculation
            add_row = {'idea_idx': 0,
                       'marg_eff': sci.marg_eff[idea_idx],
                       'k_paid': sci.ideas_k_paid_tot[idea_idx] == 0}
            row_data += add_row
            df = df.append(row_data, ignore_index=True)
        # if idea_idx is not in df
        else:
            row_data = {'idea_idx': idea_idx,
                        'marg_eff': sci.marg_eff[idea_idx],
                        'k_paid': sci.ideas_k_paid_tot[idea_idx] == 0}
            df = df.append(row_data, ignore_index=True)

    return df


def smart_returns(sci, mod):
    return 1


def prob_returns(sci, mod):
    return 1


def greedy_returns(sci, mod):
    for idea in mod.idea_list:
        continue
    return 1

