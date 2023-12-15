import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import dpcentre as dp
from icecream import ic
from copy import deepcopy


def initial_plot_neon(file_name):
    number_part = file_name.split('FH')[1].split('Neon')[0]

    raw_data = dp.RawData(file_name)
    voltage = raw_data.df[0]
    current = raw_data.df[1]

    plt.figure()
    plt.plot(voltage, current, 'ro', markersize=2)
    plt.savefig(f'plots/mercury/mercury{number_part}_initial.png', dpi=600)
    plt.clf()


def initial_plot_mercury(file_name):
    number_part = file_name.split('Trial_')[1].split('Mercury')[0]
    raw_data = dp.RawData(file_name)
    voltage = raw_data.df[0]
    current = raw_data.df[1]

    plt.figure()
    plt.plot(voltage, current, 'ro', markersize=2)
    plt.savefig(f'plots/mercury/mercury{number_part}_initial.png', dpi=600)
    plt.clf()


def calculate_excitation_energy_mecury(file_name, range1, range2):
    number = file_name.split('Trial_')[1].split('Mercury')[0]
    data = dp.RawData(file_name)

    # variable_name = str

    # Use the list to find the variable name
    first_dip = dp.find_x_min(data, range1, f'/mercury/{number}A')
    second_dip = dp.find_x_min(data, range2, f'/mercury/{number}B')
    energy = abs(second_dip - first_dip)
    ic(energy)
    return energy


def calculate_excitation_energy_neon(file_name, range1, range2):
    number = file_name.split('FH')[1].split('Neon')[0]
    data = dp.RawData(file_name)

    # variable_name = str

    # Use the list to find the variable name
    first_dip = dp.find_x_min(data, range1, f'/neon/neon{number}A')
    second_dip = dp.find_x_min(data, range2, f'/neon/neon{number}B')
    energy = abs(second_dip - first_dip)
    ic(energy)
    # ic(variable_name)
    return energy


def neon():
    neon7 = r'raw_data/Neon/FH7Neon30ms.csv'
    neon8 = r'raw_data/Neon/FH8Neon30ms.csv'
    neon9 = r'raw_data/Neon/FH9Neon30ms.csv'



    neon16 = r'raw_data/Neon/FH16Neon30ms.csv'
    neon17 = r'raw_data/Neon/FH16Neon30ms.csv'
    neon19 = r'raw_data/Neon/FH19Neon30ms.csv'
    neon21 = r'raw_data/Neon/FH21Neon30ms.csv'
    neon22 = r'raw_data/Neon/FH22Neon30ms.csv'

    neon_trials = [neon7, neon8, neon9, neon16, neon17, neon19, neon21, neon22]

    value_range1 = [18.5, 21]
    value_range2 = [35, 40]
    value_range3 = [54, 58]

    energy_neon = []
    for trials in neon_trials:
        initial_plot_neon(trials)
    # dip2 and dip3
    for i in range(3):
        tmp1 = calculate_excitation_energy_neon(neon_trials[i], value_range2, value_range3)
        energy_neon.append(tmp1)
    # dip1 and dip2
    for i in range(2, len(neon_trials)):
        tmp2 = calculate_excitation_energy_neon(neon_trials[i], value_range1, value_range2)
        energy_neon.append(tmp2)

    energy_neon = np.array(energy_neon)

    mean = np.mean(energy_neon)
    err_sample = 0.3
    err_population = np.std(energy_neon) / np.sqrt(len(energy_neon))
    print(f'For neon, {mean} += {err_population}')


def mecury():
    mecury1 = 'raw_data/Mercury/Trial_1Mercury30ms.csv'
    mecury2 = 'raw_data/Mercury/Trial_2Mercury30ms.csv'
    mecury3 = 'raw_data/Mercury/Trial_3Mercury100ms.csv'
    mecury4 = 'raw_data/Mercury/Trial_4Mercury100ms.csv'
    mecury5 = 'raw_data/Mercury/Trial_5Mercury100ms.csv'
    mecury6 = 'raw_data/Mercury/Trial_6Mercury100ms.csv'
    mecury7 = 'raw_data/Mercury/Trial_7Mercury100ms.csv'

    mecury_trials = [mecury1, mecury2, mecury3, mecury4, mecury5, mecury6, mecury7]
    for trials in mecury_trials:
        initial_plot_mercury(trials)

    value_range1 = [10, 15]
    value_range2 = [15, 20]
    energy_mercury = []
    for i in range(3, len(mecury_trials)):
        a = calculate_excitation_energy_mecury(mecury_trials[i], value_range1, value_range2)
        energy_mercury.append(a)
    energy_mercury = np.array(energy_mercury)
    mean = np.mean(energy_mercury)
    err_sample = 0.3
    err_population = np.std(energy_mercury) / np.sqrt(len(energy_mercury))
    print(f'For mecury, {mean} += {err_population}')


if __name__ == '__main__':
    neon()
    mecury()
