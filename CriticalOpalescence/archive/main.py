from dataclasses import dataclass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from icecream import ic
import dpcentre as dp


@dataclass
class DataToFit:
    gamma = None
    wavelength = None


class CriticalOpalescence:
    def __init__(self, file, wavelength):
        # attributes
        self.file = file
        self.wavelength = wavelength
        self.data = None
        # self.I_0 = None
        # self.I = None
        self.data_to_fit = DataToFit()

        # methods
        self.main()

    def get_trial_name(self):
        self.trial_name = self.file.split('_')[0]

    def get_I_0(self):
        raw_data = dp.RawData(self.file)
        raw_data.crop([45, 46])
        V_0 = raw_data.df['V'].mean()
        self.I_0 = V_0 ** 2
        ic(V_0)
        ic(self.I_0)

    def read_data(self):
        # read in and crop
        data = dp.RawData(self.file)
        data.crop([43, 43.7])
        data.plot()
        self.data = data
        # get data to fit
        # y
        self.I = data.df['V'] ** 2

    def prepare_regression2(self):
        x = np.log(self.wavelength)
        y = np.log(np.abs(np.log(self.I / self.I_0)))
        self.data_to_fit.wavelength = pd.DataFrame({
            '$\\lambda $': x,
            '$ \\ln (\\phi)$': y

        })

    def prepare_regression1(self):
        # x
        T_c = 45.5
        delta_T = self.data.df['T'] - T_c
        x = np.log(np.abs(delta_T))
        # y
        y = np.log(np.abs(np.log(self.I / self.I_0)))
        # putting it together
        self.data_to_fit.gamma = pd.DataFrame({
            '$\\Delta T$': x,
            '$ \\ln (\\phi)$': y

        })
        # ic(y)
        ic(self.data_to_fit.gamma)

    def fitting1(self):
        curve_fit = dp.CurveFit(dp.linear_model, self.data_to_fit.gamma)
        curve_fit.plot(f'{self.trial_name} gamma')
        ic(curve_fit.results.best_fit_params)
        ic(curve_fit.results.errors)

    def fitting2(self):
        curve_fit = dp.CurveFit(dp.linear_model, self.data_to_fit.wavelength)
        curve_fit.plot(f'{self.trial_name} wavelength')
        ic(curve_fit.results.best_fit_params)
        ic(curve_fit.results.errors)

    def main(self):
        self.get_trial_name()
        self.get_I_0()
        self.read_data()
        # gamma
        self.prepare_regression1()
        self.fitting1()
        # wavelength
        # self.prepare_regression2()
        # self.fitting2()


if __name__ == '__main__':
    bright_red = r'BrightRed1_1000ms.csv'
    wave_length = 612e-9
    CriticalOpalescence(bright_red, wave_length)
