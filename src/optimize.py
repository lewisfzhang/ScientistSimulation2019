# optimize.py
import numpy as np
import idea


def investing_helper(sci):
    # df that keeps track of scientist's transactions within current time period
    # for k_paid: 0 if already paid, # 1 if paid this period
    inv_dict = {'idea_idx': [], 'marg_eff': [], 'k_paid': []}

    # ARRAY: extra cost for each idea, which is a column in the scientist.perceived_returns df
    k = np.asarray(sci.perceived_rewards['Idea K'])

    # ARRAY: same logic as idea_k_paid_tot where 0 = haven't learned, 1 = learned
    k_paid_present = np.copy(sci.ideas_k_paid_tot)

    # keeps on investing while scientist has available effort
    while sci.avail_effort > 0:
        # k_paid is 0 if scientist hasn't paid learning cost
        # True = 1, False = 0 --> so if scientist hasn't paid learning cost, curr_k = 1 * k
        curr_k = (k_paid_present == 0) * k

        # SCALAR: increment based on ONLY ideas where a scientist is able
        # to invest research effort after entering learning barrier
        # +1 ensures that each idea a scientist works on will have at least 1 unit of marg effort
        increment = max(curr_k[np.where(curr_k + 1 <= sci.avail_effort)]) + 1

        # given available effort a scientist left, all of them have been learned
        # --> scientist invest all remaining effort on research given above belief
        # ASSUMPTION: scientist can only research an idea he can fully invest in
        if increment == 1:
            increment = sci.avail_effort

        # ARRAY: marg effort for each idea
        sci.marg_eff = increment - curr_k

        # choosing which optimization to use
        if sci.model.config.opt_num == 0:
            idea_idx = greedy_returns(sci)
        else:
            idea_idx = smart_returns(sci)

        k_paid_present[idea_idx] = 1  # mark down that the scientist has paid learning cost for this idea

        inv_dict = update_df(inv_dict, idea_idx, sci)  # record transaction

        sci.avail_effort -= increment

    return inv_dict  # returns all transactions scientist has made in this tp


def smart_returns(sci):
    return 1


def greedy_returns(sci):
    mean, sds, maxx = list_perception(sci)
    max_rtn = 0
    max_idx = 0
    for idx, i in enumerate(sci.model.idea_list):
        start_idx = i.total_effort
        end_idx = start_idx + sci.marg_eff[idx]
        rtn = idea.get_returns(mean[idx], sds[idx], maxx[idx], start_idx, end_idx)
        if rtn > max_rtn:
            max_rtn = rtn
            max_idx = idx
    return max_idx


# returns mean, sds, max columns in sci.perceived_rewards as lists
def list_perception(sci):
    mean = np.asarray(sci.perceived_rewards['Idea Mean'])
    sds = np.asarray(sci.perceived_rewards['Idea SDS'])
    maxx = np.asarray(sci.perceived_rewards['Idea Max'])  # maxx because max is reserved keyword
    return mean, sds, maxx


# adds the current transaction to the list of transactions
def update_df(inv_dict, idea_idx, sci):
    # checks if idea_idx is already in the df
    arr = np.where(np.asarray(inv_dict['idea_idx']) == idea_idx)[0]  # [0] because it returns a tuple with array (array[],)

    if len(arr) == 0:  # if idea_idx is not in df
        inv_dict['idea_idx'].append(idea_idx)
        inv_dict['marg_eff'].append(sci.marg_eff[idea_idx])
        # for k_paid, same logic as sci.curr_k calculation
        # assuming this array hasn't changed since start of tp
        # goal is to keep track of which ideas the scientist learned in this period
        # (or in other words, the ones they hadn't learned before this time period)
        inv_dict['k_paid'].append(sci.ideas_k_paid_tot[idea_idx] == 0)
        return inv_dict
    elif len(arr) == 1:  # if idea already exists in df
        # idea_idx and k_paid do not need to be updated since they were already established in initial entry
        inv_dict['marg_eff'][arr[0]] += sci.marg_eff[idea_idx]  # arr[0] = index of idea_idx in inv_dict
        return inv_dict
    else:  # there is a problem, shouldn't be more than one element in
        raise Exception("duplicate idx, take a look")
