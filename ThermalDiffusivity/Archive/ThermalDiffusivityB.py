import numpy as np
from general import PeriodicChange
from icecream import ic
import dpcentre as dp

pi = np.pi


def p2p_amplitude():
    peaks = [
        34.38, 32.51, 31.59, 28.68, 27.78,
        26.91, 26.33, 25.60, 24.99, 24.10,
    ]

    troughs = [
        24.33, 23.47, 22.71, 20.29, 19.92,
        19.21, 18.92, 18.47, 17.42, 16.82
    ]

    peaks = np.array(peaks)
    troughs = np.array(troughs)

    p2p = np.mean(peaks - troughs)

    return p2p


# def temperature_difference():
#     pass


def kelvin_function():
    B = p2p_amplitude()
    temperature_difference = 49
    M_0 = (4 * temperature_difference) / (B * pi)

    return M_0


# M_0=7.7 ---> x = 5.3

def thermal_diffusivity():
    x = 5.3
    radius = 13e-3
    period = 100
    D = (radius / x) ** 2 * (2 * pi / period)

    return D


def error():
    x = 5.3
    err_x = 0.5

    radius = 13e-3
    err_radius = 3e-4

    period = 100
    err_period = 5

    # radius squared error
    err_radius_squared = dp.MultiplyError(err_a=err_radius / radius, err_b=err_radius / radius)
    err_radius_squared = err_radius_squared.err_z

    # radius squared error
    err_x_squared = dp.MultiplyError(err_a=err_x/x, err_b=err_x/x)
    err_x_squared = err_x_squared.err_z

    err_x_and_a = dp.MultiplyError(err_a= err_x_squared, err_b=err_radius_squared)
    err_x_and_a = err_x_and_a.err_z

    final_err = dp.MultiplyError(err_a=err_x_and_a, err_b=err_period/period)
    final_err = final_err.err_z

    return final_err




if __name__ == '__main__':
    a = PeriodicChange('../PeiodicChange/raw_data/ThermalDiffusivityB1000ms.csv')
    a.try_plot()
    ic(error())
    ic(thermal_diffusivity())
