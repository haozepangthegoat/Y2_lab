"""
Last modified:
Author: Haoze Pang, Kieran Tempest

Description
----------
This script calculates the thermal diffusivity using a step change method.

TODOs
----------
TODO: modify calculate_thermal_diffusivity so it calculates err_thermal_diffusivity as well

"""
from icecream import ic
from general import StepChange
import numpy as np
import dpcentre as dp


class RegressionData(dp.LSFRInitialise):
    """
    Prepare regression data

    Inputs
    ------
    experiment_data (StepChange)

    """

    def __init__(self, experiment_data: StepChange):
        dp.LSFRInitialise.__init__(self)
        self.experiment_data = experiment_data
        # Prepare
        self.prepare_regression()

        # validate input
        self.validate_input()

    def y_error(self):
        """
        Calculates error on y in LSFR
        Returns: err_y
        """
        # initial error
        err_axial_temperture = 3e-2
        err_average_external_temperture = 3e-2
        # add
        err_addition = dp.AddError(err_a=err_axial_temperture, err_b=err_average_external_temperture)
        err_addition = err_addition.err_z
        # take ln
        err_logarithm = dp.LnError(err_a=err_addition, a=np.log(np.abs(self.experiment_data.axial_temperture -
                                                                       self.experiment_data.average_external_temperture)))
        err_logarithm = err_logarithm.err_z

        self.err_y = err_logarithm

    def x_and_y(self):
        self.x_i = self.experiment_data.time
        self.y_i = np.log(np.abs(self.experiment_data.axial_temperture -
                                 self.experiment_data.average_external_temperture))

    def prepare_regression(self):
        self.y_error()
        self.x_and_y()


def regression(experiment_name: str):
    """
    Performs regression on StepChange

    Args
    ----------
    experiment_name (str):
        name of the raw data file of each experiment

    Returns
    -------
    lsfr (dp.LSFR)
    """
    # set up basic data
    experiment_data = StepChange(experiment_name)  # experiment data
    lsfr_input = RegressionData(experiment_data)  # regression data
    # perform regression
    lsfr = dp.LSFRShowResults(lsfr_input)
    # show results and plot lsfr graph

    return lsfr


def calculate_thermal_diffusivity(m_input):
    """
    Calculate the thermal diffusivity using the step change method.

    Parameters
    ----------

    Returns
    -------
    None
    """
    # inputs
    m = m_input
    lambda_1 = 2.405
    radius = 13e-3
    # thermal diffusivity
    thermal_diffusivity = -(radius ** 2 / lambda_1 ** 2) * m
    # print results
    print(f"thermal diffusivity is {thermal_diffusivity: .5e}")


def calculate_err_thermal_diffusivity(m_input, err_m_input):
    # inputs
    # m
    m = m_input
    err_m = err_m_input
    # radius
    radius = 13e-3
    err_radius = 3e-4
    # propagate errors
    # radius squared error
    err_radius_squared = dp.MultiplyError(err_a=err_radius/radius, err_b=err_radius/radius)
    err_radius_squared = err_radius_squared.err_z
    # thermal diffusivity
    err_thermal_diffusivity = dp.MultiplyError(err_b=err_m / m, err_a=err_radius_squared)
    err_thermal_diffusivity = err_thermal_diffusivity.err_z
    # print results
    print(f"error on thermal diffusivity is {err_thermal_diffusivity: .5e}")


def final_calculation_1():
    # import files
    experiment1 = "raw_data/ThermalDiffusivity_StepChange_experiment_1.csv"
    lsfr = regression(experiment1)
    lsfr.show_result()
    lsfr.plot_graph('experimentA1.jpg')
    # calculate
    print('experiment1')
    print("-" * 20)
    m, err_m = lsfr.gradient, lsfr.err_gradient
    calculate_thermal_diffusivity(m)
    calculate_err_thermal_diffusivity(m, err_m)


def final_calculation_2():
    lsfr = regression(experiment2)
    lsfr.show_result()
    lsfr.plot_graph('experimentA2.jpg')
    # calculate
    print('experiment2')
    print("-" * 20)
    m, err_m = lsfr.gradient, lsfr.err_gradient
    calculate_thermal_diffusivity(m)
    calculate_err_thermal_diffusivity(m, err_m)


if __name__ == '__main__':
    experiment2 = "raw_data/ThermalDiffusivity_StepChange_experiment_2.csv"
    final_calculation_1()
    final_calculation_2()
