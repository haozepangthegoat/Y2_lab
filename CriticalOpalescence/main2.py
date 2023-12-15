import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from functools import cache, cached_property
from icecream import ic
import dpcentre.enhanced_pd as dp
from dpcentre import clean


def linear_model(x, m, c):
    r"""
    Model: \( \ln (\ln (I/I_0)) = - \gamma \ln(\Delta T) +C\)
    Params: \gamma, C

    """
    return -m * x + c


class CriticalOpalescence:
    def __init__(self, file_name):
        self.data = dp.get_data_from(file_name)
        self.processed_data = None

    @property
    @cache
    def initial_intensity(self):
        upper, lower = 48, 47
        mask = (self.data.iloc[:, 0] > lower) & (self.data.iloc[:, 0] < upper)
        cropped_data = self.data[mask]

        return cropped_data.iloc[:, 1].mean() ** 2

    @property
    @cache
    def critical_temperature(self):
        min_index = self.data.stat.troughs[0]
        return self.data.iloc[min_index, 0]

    def process_data(self):
        # crop
        lower = self.critical_temperature
        upper = lower + 0.15
        mask = ((self.data.iloc[:, 0] > lower) & (self.data.iloc[:, 0] < upper))
        self.processed_data = self.data[mask]

        # convert to intensity
        self.processed_data.iloc[:, 1] = self.processed_data.iloc[:, 1] ** 2

        # calculate y
        phi = np.abs(np.log((self.processed_data.iloc[:, 1] / self.initial_intensity)))
        self.processed_data.iloc[:, 1] = np.log(phi)

        # calculate x
        delta_t = self.processed_data.iloc[:, 0] - self.critical_temperature
        self.processed_data.iloc[:, 0] = np.log(delta_t)

        # curve fitting
        self.processed_data.stat.model = linear_model

        # rename column


def main(file_name, trial_name):
    experiment = file_name
    experiment = CriticalOpalescence(experiment)

    experiment.data.stat.name = trial_name
    experiment.data.columns = [r'Temperature', r'Voltage']
    experiment.data.stat.plot(f'{trial_name}-initial')

    experiment.process_data()
    experiment.processed_data.stat.name = trial_name
    experiment.processed_data.columns = [r'\( \ln(\Delta T) \)', r'\( \ln (\ln (I/I_0)) \)']
    experiment.processed_data.stat.plot(f'{trial_name}-fitting')


if __name__ == '__main__':
    bright_red = 'BrightRed2_100ms.csv'
    bright_red2 = 'BrightRed3_100ms.csv'
    deep_red = 'DeepRed2_100ms.csv'

    violet1 = 'Violet1_100ms.csv'
    violet2 = 'Violet2_100ms.csv'

    turquoise = 'TurquoiseGreen2_100ms.csv'
    emerald = 'EmeraldGreen2_100ms.csv'

    royal_blue = 'RoyalBlue3_100ms.csv'

    # trials
    main(bright_red, 'bright_red')
    main(bright_red2, 'bright_red2')
    main(deep_red, 'deep_red')

    main(violet1, 'violet1')
    main(violet2, 'violet2')

    main(turquoise, 'turquoise')
    main(emerald, 'emerald')

    main(royal_blue, 'royal_blue')

    clean()
