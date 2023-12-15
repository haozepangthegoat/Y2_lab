from icecream import ic
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import dpcentre as dp

mercury3 = r'raw_data/Neon/FH4Neon100ms.csv'

mercury3 = pd.read_csv(mercury3)
# mercury3 = mercury3[(10 < mercury3['voltage']) & (mercury3['voltage'] < 28.6)]

# ic(mercury3)

dp.plot(mercury3['voltage'], mercury3['current'])

# if __name__ == '__main__':
#     pass

def neon_initial(file_name):
    raw_data = dp.RawData(file_name)
    voltage = raw_data.df[0]
    current = raw_data.df[1]

    plt.figure()
    plt.plot(voltage, current, 'ro', markersize=2)
    plt.savefig('plots/neon_initial.png', dpi=600)
    plt.clf()


# def plot(file_name):
#     number_part = filename.split('FH')[1].split('Neon')[0]
#     data = dp.RawData(file_name)
#     data.try_plot('voltage', 'current', f'voltage vs current')


# def initial_plot(experiments):
#     for trial in experiments:
#         plot(trial)


# def excitation_energy(experiments):
#     value_range1 = [18.5, 21]
#     value_range2 = [35, 40]
#     value_range3 = [50, 60]
#
#     energies = []
#     for i in range(3):
#         min1 = find_min(experiments[i], value_range2)
#         min2 = find_min(experiments[i], value_range3)
#         energy = abs(min2 - min1)
#         energies.append(energy)
#     for i in range(3, len(experiments)):
#         min1 = find_min(experiments[i], value_range1)
#         min2 = find_min(experiments[i], value_range2)
#         energy = abs(min2 - min1)
#         energies.append(energy)
#
#     ic(energies)