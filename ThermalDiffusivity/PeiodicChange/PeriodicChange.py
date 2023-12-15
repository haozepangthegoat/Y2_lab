import pandas as pd

import dpcentre as dp
from icecream import ic


def get_data(file, trial_name):
    raw_data = dp.RawData(file)
    raw_data.plot(trial_name)
    return raw_data.df


def regression(data, trial_name):
    guess = [2, 100, 0, 36, 25]
    curve_fit = dp.CurveFit(data, dp.sine_model, guess)
    curve_fit.plot(trial_name)
    ic(curve_fit.results.errors)
    ic(curve_fit.results.best_fit_params)


def main(file, trial_name):
    raw_data = get_data(file, trial_name)
    regression_data = pd.DataFrame({
        'time': raw_data.iloc[:, 0],
        'axial_temperature': raw_data.iloc[:, 1]
    })
    regression(regression_data, trial_name)


if __name__ == '__main__':
    file1 = 'raw_data/ThermalDiffusivityB1000ms.csv'
    file2 = 'raw_data/ThermalDiffusivityB21000ms.csv'

    main(file1, '1')
    main(file2, '2')
