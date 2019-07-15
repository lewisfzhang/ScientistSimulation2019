# functions.py
import numpy as np
import random
import timeit
import pandas as pd


def get_random_float(minn, maxx, configg):  # configg is the config object, used to get random seed value
    np.random.seed(configg.get_next_seed())
    return random.uniform(minn, maxx)


def get_normal_number(mean, sds, configg):  # configg is the config object, used to get random seed value
    np.random.seed(configg.get_next_seed())
    x = np.random.normal(mean, sds)  # returns a single SCALAR
    while x < 0:  # we want positive values only
        np.random.seed(configg.get_next_seed())
        x = np.random.normal(mean, sds)
    return x


def arrays_to_html(arr, row_names, file_name):  # takes list of arrays
    df = pd.DataFrame(data=arr, index=row_names, columns=pd.Index(np.arange(len(arr[0])), name=file_name))
    df = df.round(2)
    df = df.transpose()
    df.to_html('../out/{}_arrays_df.html'.format(file_name))


def array2d_to_df(arr, row_name='row', col_name='col', file_name='unnamed_df'):
    i = pd.Index(np.arange(len(arr)), name=row_name)
    c = pd.Index(np.arange(len(arr[0])), name=col_name)
    df = pd.DataFrame(data=arr, index=i, columns=c)
    df.to_html('../out/{}_df.html'.format(file_name))
    return df


# returns index where cumulative sum starting from index 0 is greater or equal to "target" sum
def sum_point_array(arr, target):
    curr_sum = 0
    for idx, val in enumerate(arr):
        curr_sum += val
        if curr_sum >= target:
            return idx
    return -1  # not found


class Time:
    def __init__(self, name):
        self.runtime = timeit.default_timer()  # keeps track of the starting time
        self.pause = 0  # keeps track of time paused
        self.name = name

    def stop_time(self):
        stop = timeit.default_timer()
        print('{0} elapsed runtime: {1} seconds'.format(self.name, round(stop - self.runtime, 3)))
        self.runtime = stop

    def pause_time(self):
        self.pause = timeit.default_timer()

    def resume_time(self):
        time = timeit.default_timer()
        if self.pause == 0:
            self.runtime = time  # we want time to actually start here (pause_time() has never been called yet)
        else:
            pause_length = time - self.pause
            self.runtime += pause_length  # adds the length of pause, which cancels out when stop_time() is called
