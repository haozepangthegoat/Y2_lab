import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import dpcentre as dp
from icecream import ic


def test1(file_name):
    pass
    raw_data = dp.RawData(file_name)
    # raw_data.filter_outliers(1)
    raw_data.crop(0, [15, 20])
    voltage = raw_data.df[0]
    current = raw_data.df[1]
    dp.plot(voltage, current, f' cropped_curve_1 V vs I')
    params, cov = curve_fit(dp.polynomial, xdata=voltage, ydata=current)
    fitted_curve = dp.polynomial(voltage, *params)
    minimum = voltage[fitted_curve == np.min(fitted_curve)][0]
    ic(minimum)
    dp.plot(voltage, fitted_curve, f'plot fit1')

    return minimum


def test2(file_name):
    pass
    raw_data = dp.RawData(file_name)
    # raw_data.filter_outliers(1)
    raw_data.crop(0, [20, 25])
    voltage = raw_data.df[0]
    current = raw_data.df[1]
    dp.plot(voltage, current, f' cropped_curve_2 V vs I')
    params, cov = curve_fit(dp.polynomial, xdata=voltage, ydata=current)
    fitted_curve = dp.polynomial(voltage, *params)
    minimum = voltage[fitted_curve == np.min(fitted_curve)][0]
    dp.plot(voltage, fitted_curve, f'plot fit2')

    return minimum


def initial_plot(file_name):
    raw_data = dp.RawData(file_name)
    # raw_data.filter_outliers(1)
    # raw_data.crop_data(0, [15, 20])
    voltage = raw_data.df[0]
    current = raw_data.df[1]
    dp.plot(voltage, current, f'initial_plot')


def main(file_name):
    diff = abs(test2(file_name) - test1(file_name))
    ic(f'{diff: 3e}')

    initial_plot(file_name)
    # test1(file_name)


def neon_initial(file_name):
    raw_data = dp.RawData(file_name)
    voltage = raw_data.df[0]
    current = raw_data.df[1]

    plt.figure()
    plt.plot(voltage, current, 'ro', markersize=2)
    plt.savefig('plots/neon_initial.png', dpi=600)
    plt.clf()


def neon_min1(file_name, value_range):
    raw_data = dp.RawData(file_name)
    raw_data.crop(0, value_range)
    voltage = raw_data.df[0]
    current = raw_data.df[1]

    # fitting
    params, cov = curve_fit(dp.polynomial, voltage, current)
    fitted_curve = dp.polynomial(voltage, *params)
    minimum = voltage[fitted_curve == np.min(fitted_curve)][0]

    # plotting
    # plt.figure()
    # plt.plot(voltage, current, 'ro', markersize=2)
    # plt.plot(voltage, fitted_curve)
    # plt.savefig('plots/neon_min1.png', dpi=600)
    # plt.clf()

    return minimum


def neon_min2(file_name, value_range):
    raw_data = dp.RawData(file_name)
    raw_data.crop(0, value_range)
    voltage = raw_data.df[0]
    current = raw_data.df[1]

    # fitting
    params, cov = curve_fit(dp.polynomial, voltage, current)
    fitted_curve = dp.polynomial(voltage, *params)
    minimum = voltage[fitted_curve == np.min(fitted_curve)][0]

    # plotting
    # plt.figure()
    # plt.plot(voltage, current, 'ro', markersize=2)
    # plt.plot(voltage, fitted_curve)
    # plt.savefig('plots/neon_min2.png', dpi=600)
    # plt.clf()

    return minimum


def calculate_neon(file_name, value_range):
    neon_initial(file_name)
    diff = neon_min2(file_name, value_range[1]) - neon_min1(file_name, value_range[0])
    # ic(diff)
    return diff


def main2():
    # file names
    mecury1 = r'raw_data/Mercury/Trial_1Mercury30ms.csv'
    mecury2 = r'raw_data/Mercury/Trial_2Mercury30ms.csv'
    # neon1 = r'raw_data/Neon/FH1Neon100ms.csv'
    trials = [

    ]
    neon7 = r'raw_data/Neon/FH7Neon30ms.csv'
    neon8 = r'raw_data/Neon/FH8Neon30ms.csv'
    neon9 = r'raw_data/Neon/FH9Neon30ms.csv'
    neon10 = r'raw-data/Neon/FH10Neon30ms.csv'

    neon16 = r'raw_data/Neon/FH16Neon30ms.csv'
    neon17 = r'raw_data/Neon/FH16Neon30ms.csv'
    neon19 = r'raw_data/Neon/FH19Neon30ms.csv'
    neon21 = r'raw_data/Neon/FH21Neon30ms.csv'
    neon22 = r'raw_data/Neon/FH22Neon30ms.csv'
    # mecury
    main(mecury1)
    main(mecury2)


if __name__ == '__main__':
    main2()
