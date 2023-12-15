import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dpcentre as dp
from dpcentre import Experiment
from dpcentre import linear_model
from icecream import ic


class CriticalOpalescence(Experiment):
    def __init__(self, data_file):
        super().__init__(data_file)
        self.trial_name = self._file_name.split('_')[0]
        self._initial_intensity = None
        self._critical_temperature = None

    @property
    def initial_intensity(self):
        """the initial intensity of the experiment
        obtained by
        """
        if self._initial_intensity is None:
            mask = self.initial_data.x.between(47, 48)
            _cropped_data = self.initial_data[mask]
            self._initial_intensity = _cropped_data.y.mean() ** 2
        return self._initial_intensity

    @property
    def critical_temperature(self):
        """x where y = 0
        """
        if self._critical_temperature is None:
            self._critical_temperature = self.initial_data.minimum_point
        return self._critical_temperature

    def _get_initial_data(self):
        _data = dp.get_data_from(self._file_name)
        _data = dp.Data2D(_data)

        _data.name = self.trial_name
        column2_name = r'Voltage (V)'
        column1_name = r'Temperature \( ^\circ \) C'
        _data.columns = [column1_name, column2_name]
        _caption = (r'Initial plot of my data. I chose temperature '
                    r'between \(T = 47 \) and \(T = 48 \) \( ^\circ \text{C} \) to calculate '
                    r'\(I_0\).')

        _data.plot(f'{self.trial_name}-initial_plot', _caption)
        self._initial_data = _data

    def _process_data(self):
        # crop data
        mask = self.initial_data.x.between(43.5, self.critical_temperature-0.02)
        _data = self.initial_data[mask]

        # calculate x
        critical_temperature = self.critical_temperature

        temperature_difference = _data.x - critical_temperature
        _data.x = temperature_difference

        # calculate y
        _data.y = _data.y ** 2

        # rename column
        column2_name = r'Intensity (\( \text{V}^2 \))'
        column1_name = r'Temperature (\(^\circ\text{C}\))'
        _data.columns = [column1_name, column2_name]
        _data.name = self.trial_name
        self._processed_data = _data


class Gamma(CriticalOpalescence):
    def __init__(self, data_file):
        super().__init__(data_file)

    def _prepare_data_for_fitting(self):
        #
        _data = self.processed_data
        # calculate y
        phi = np.log(_data.y / self.initial_intensity)
        _data.y = np.log(np.abs(phi))

        # calculate x
        _data.x = np.log(np.abs(_data.x))

        # rename columns
        column2_name = r'\( \ln(\ln (I/I_0)) \)'
        column1_name = r'\( \ln \Delta T \)'
        _data.columns = [column1_name, column2_name]
        _data.name = self.trial_name

        # assign back
        self._data_for_fitting = _data

    def draw_best_fit_plot(self):
        fit_result = self.data_for_fitting.fit_a_curve(linear_model)
        # add caption
        model_name = r'\( \ln (\ln I/I_0) = - \gamma \ln (\Delta T) +C\)'
        p0 = r'\( \gamma \)'
        p1 = r'\(C\)'
        _caption = [model_name, p0, p1]

        fit_result.plot(f'{self.trial_name}-fitted_curve', _caption)


def perform_calculation(file):
    experiment = file
    experiment = Gamma(file)
    experiment.draw_best_fit_plot()
    ic(experiment.initial_intensity)


def main(trials):
    for trial in trials:
        perform_calculation(trial)


if __name__ == '__main__':
    # bright red

    blue = r'Blue1_100ms.csv'
    perform_calculation(blue)
    # a = CriticalOpalescence(blue)
    # b = a.initial_data.minimum_point
    # ic(b==43.79)
