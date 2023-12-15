import dpcentre as dp
import numpy as np
from icecream import ic


def linear_model(x, m, c):
    return m * x + c


class Experiment:
    def __init__(self, name_of_the_experiment='BrightRed1_1000ms.csv'):
        self._file_name = name_of_the_experiment
        self._initial_data = None
        self._initial_intensity = None
        self._processed_data = None
        self._data_for_fitting = None

    @property
    def initial_data(self):
        if self._initial_data is None:
            # print('Getting initial data')  # Optional: Comment out for cleaner output
            _data = dp.get_data_from(self._file_name)

            _data = dp.Data2D(_data)
            _data.name = 'BrightRed'
            _caption = (r'Initial plot of my data. Voltage vs Temperature. I chose temperature '
                        r'between \(T = 45 \) and \(T = 46 \) \( ^\circ \text{C} \) to calculate '
                        r'\(I_0\).')
            # getting minimum point coordinate
            _y_min = _data.y.min()
            _data.plot('brightred-init', _caption)
            # TODO: with caption and save as methods
            self._initial_data = _data
        return self._initial_data

    @property
    def initial_intensity(self):
        if self._initial_intensity is None:
            # print('Calculating initial intensity...')  # Optional: Comment out for cleaner output
            mask = self.initial_data.x.between(45, 46)
            _data = self.initial_data[mask]
            self._initial_intensity = _data.y.mean() ** 2
        return self._initial_intensity

    @property
    def processed_data(self):
        if self._processed_data is None:
            # print('Processing data...')  # Optional: Comment out for cleaner output
            mask = self.initial_data.x.between(43, 43.7)
            _data = self.initial_data[mask]

            critical_temperature = 45.5
            temperature_difference = _data.x - critical_temperature
            _data.x = temperature_difference

            _data.y = _data.y ** 2
            column2_name = r'Intensity (\( \text{V}^2 \))'
            column1_name = r'Temperature (\(^\circ\text{C}\))'
            _data.columns = [column1_name, column2_name]
            _data.name = 'Intensity vs T'

            self._processed_data = _data
        return self._processed_data

    @property
    def data_for_fitting(self):
        if self._data_for_fitting is None:
            # print('Getting data ready for fitting...')  # Optional: Comment out for cleaner output
            _data = self.processed_data

            phi = np.log(_data.y / self.initial_intensity)
            _data.y = np.log(np.abs(phi))
            _data.x = np.log(np.abs(_data.x))

            column2_name = r'\( \ln(\ln (I/I_0)) \)'
            column1_name = r'\( \ln \Delta T \)'
            _data.columns = [column1_name, column2_name]

            _data.name = r'BrightRed'
            self._data_for_fitting = _data
        return self._data_for_fitting

    def fitting_process(self):
        # print('Starting curve fitting...')

        fit_result = self.data_for_fitting.fit_a_curve(linear_model)
        # adding caption
        model_name = r'\( \ln (\ln I/I_0) = - \gamma \ln (\Delta T) +C\)'
        p0 = r'\( \gamma \)'
        p1 = r'\(C\)'
        _caption = [model_name, p0, p1]

        fit_result.plot('new-fitting curve', _caption)


if __name__ == '__main__':
    a = Experiment()
    # ic(a.initial_intensity)  # Uncomment if needed
    a.fitting_process()
