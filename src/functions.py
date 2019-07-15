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
