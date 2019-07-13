# functions.py
import numpy as np
import pandas as pd
import random


def get_random_number(min, max, configg):  # configg is the config object, used to get random seed value
    np.random.seed(configg.get_next_seed())
    return random.randrange(min, max)


def get_normal_number(mean, sds, configg):  # configg is the config object, used to get random seed value
    np.random.seed(configg.get_next_seed())
    x = np.random.normal(mean, sds)  # returns a single SCALAR
    while x < 0:  # we want positive values only
        np.random.seed(configg.get_next_seed())
        x = np.random.normal(mean, sds)
    return x
