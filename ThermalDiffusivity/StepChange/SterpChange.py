import numpy as np
import pandas as pd
import dpcentre as dp
from icecream import ic


def get_data(file, num_trial):
    raw_data = dp.RawData(file)
    raw_data.plot(num_trial)

    return raw_data


def prepare_regression(raw_data):
    # calculate y
    average_surface_temperature = raw_data.iloc[:, 2].mean()
    y = np.log(np.abs(raw_data.iloc[:, 1] - average_surface_temperature))
    # calculate err_y
    err_axial_temperture = 3e-2
    err_average_external_temperture = 3e-2
    err_addition = dp.combine_error(err_average_external_temperture, err_average_external_temperture)
    err_ln = dp.ln_error(err_addition, y)
    # putting regression data in a df
    data_to_fit = pd.DataFrame({
        'time': raw_data.iloc[:, 0],
        '$ln(T(0, t) - T_{new})$': y,
        'err': err_ln
    })
    return data_to_fit


def calculate_gradient(data_to_fit, num_trial):
    curve_fit = dp.CurveFit(data_to_fit, dp.linear_model)
    curve_fit.plot(f'fitting plot (StepChange {num_trial})')
    m = curve_fit.results.best_fit_params[0]
    err_m = curve_fit.results.errors[0]
    print(f'The gradient of trial {num_trial} is {m} \pm {err_m}')


def main(file):
    number_part = file.split('ment_')[1].split('.csv')[0]
    raw_data = get_data(file, number_part).df
    data_to_fit = prepare_regression(raw_data)
    calculate_gradient(data_to_fit, number_part)


if __name__ == '__main__':
    file1 = r'raw_data/ThermalDiffusivity_StepChange_experiment_1.csv'
    file2 = r'raw_data/ThermalDiffusivity_StepChange_experiment_2.csv'
    main(file1)
    main(file2)
