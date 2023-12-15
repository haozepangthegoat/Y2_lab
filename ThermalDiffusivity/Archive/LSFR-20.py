# -*- coding: utf-8 -*-
"""
Least Squares Fitting Routine for Year 1 lab.
Lloyd Cawthorne 12/06/20

Adapted from linear_regression.py by Abie Marshall 2016
    Adapted from LSFR.m credits to:
    Jordan Hulme
    Adam Petrus
    Ian Duerdoth
    Paddy Leahy

Reads in and validates data assuming given in columns: independent variable,
dependent variable, uncertainty on dependent variable.

Data is rejected and flagged for either being non-numerical or having an
uncertainty less than or equal to zero. The script continues with the accepted
data.

Performs a least squares fit to a linear function, produces reduced chi
squared, uncertainties and plot.

Details of the fitting procedure can be found here:
https://mathworld.wolfram.com/LeastSquaresFitting.html

You will learn how to write code similar to this in PHYS20161: Introduction
to Programming for Physicists.

Edit the global constants (written in ALL_CAPS, below the import statements)
to edit the file input and plot attributes.

"""

import numpy as np
import matplotlib.pyplot as plt


# File reading details
FILE_NAME = 'varify.csv'  # Remember to include the extension
SKIP_FIRST_LINE = False
DELIMITER = ','  # Set to space, ' ', if working with .txt file without commas

# Plotting details
PLOT_TITLE = 'Plot of my data'
X_LABEL = 'Abscissa'
Y_LABEL = 'Ordinate'
AUTO_X_LIMITS = True
X_LIMITS = [0., 10.]  # Not used unless AUTO_X_LIMITS = False
AUTO_Y_LIMITS = True
Y_LIMITS = [0., 10.]  # Not used unless AUTO_Y_LIMITS = False
LINE_COLOUR = 'red'  # See documentation for options:
# https://matplotlib.org/3.1.0/gallery/color/named_colors.html
LINE_STYLE = '-'   # See documentation for options:
# https://matplotlib.org/gallery/lines_bars_and_markers/line_styles_reference.html
MARKER_STYLE = 'x'  # See documentation for options:
# https://matplotlib.org/3.1.1/api/markers_api.html#module-matplotlib.markers
MARKER_COLOUR = 'black'
GRID_LINES = True
SAVE_FIGURE = True
FIGURE_NAME = 'fit_result.png'
FIGURE_RESOLUTION = 400  # in dpi


def linear_function(x_variable, parameters):
    """Outputs the result of y = mx + c, where m is the slope and c is the
    offset.  parameters is an array such that [slope, offset].
    Args:
        x_variable: float
        parameters: [float, float]
    Returns: float
    """
    return parameters[0] * x_variable + parameters[1]


def check_numeric(entry):
    """Checks if entry is numeric
    Args:
        entry: string
    Returns:
        bool
    Raises:
        ValueError: if entry cannot be cast to float type
    """
    try:
        float(entry)
        return True
    except ValueError:
        return False


def check_uncertainty(uncertainty):
    """Checks uncertainty is non-zero and positive.
    Args:
        uncertainty: float
    Returns:
        Bool
    """
    if uncertainty > 0:
        return True
    return False


def validate_line(line):
    """Validates line. Outputs error messages accordingly.
    Args:
        line: string
    Returns:
        bool, if validation has been succesful
        line_floats, numpy array of floats
    """
    line_split = line.split(DELIMITER)

    for entry in line_split:
        if check_numeric(entry) is False:
            print('Line omitted: {0:s}.'.format(line.strip('\n')))
            print('{0:s} is nonnumerical.'.format(entry))
            return False, line_split
    line_floats = np.array([float(line_split[0]), float(line_split[1]), float(line_split[2])])
    if line_floats[2] <= 0:
        print('Line omitted: {0:s}.'.format(line.strip('\n')))
        print('Uncertainty must be greater than zero.')
        return False, line_floats
    return True, line_floats


def open_file(file_name=FILE_NAME, skip_first_line=SKIP_FIRST_LINE):
    """Opens file, reads data and outputs data in numpy arrays.
    Args:
        file_name: string, default given by FILE_NAME
    Returns:
        x_data: numpy array of floats
        y_data: numpy array of floats
        y_uncertainties: numpy array of floats
    Raises:
        FileNotFoundError
    """
    # Create empty arrays ready to store the data
    x_data = np.array([])
    y_data = np.array([])
    y_uncertainties = np.array([])
    try:
        raw_file_data = open(file_name, 'r')
    except FileNotFoundError:
        print("File '{0:s}' cannot be found.".format(file_name))
        print('Check it is in the correct directory.')
        return x_data, y_data, y_uncertainties
    for line in raw_file_data:
        if skip_first_line:
            skip_first_line = False
        else:
            line_valid, line_data = validate_line(line)
            if line_valid:
                x_data = np.append(x_data, line_data[0])
                y_data = np.append(y_data, line_data[1])
                y_uncertainties = np.append(y_uncertainties, line_data[2])
    raw_file_data.close()
    return x_data, y_data, y_uncertainties


def fitting_procedure(x_data, y_data, y_uncertainties):
    """Implements an analytic approach according to source in header.
    Args:
        x_data: numpy array of floats
        y_data: numpy array of floats
        y_uncertainties: numpy array of floats
    Returns:
        parameters: numpy array of floats, [slope, offset]
        parameter_uncertainties: numpy array of floats, [slope_uncertainty,
                                 offset_uncertainty]
        """
    weights = 1. / y_uncertainties**2

    repeated_term = (np.sum(weights) * np.sum(x_data**2 * weights)
                     - np.sum(x_data * weights)**2)





    slope = ((np.sum(weights) * np.sum(x_data * y_data * weights)
              - np.sum(x_data * weights) * np.sum(y_data * weights))
             / repeated_term)






    slope_uncertainty = np.sqrt(np.sum(weights) / repeated_term)
    offset = ((np.sum(y_data * weights) * np.sum(x_data**2 * weights)
               - np.sum(x_data * weights) * np.sum(x_data * y_data * weights))
              / repeated_term)
    offset_uncertainty = np.sqrt(np.sum(x_data**2 * weights) / repeated_term)

    return (np.array([slope, offset]), np.array([slope_uncertainty,
                                                 offset_uncertainty]))


def chi_squared_function(x_data, y_data, y_uncertainties, parameters):
    """Calculates the chi squared for the data given, assuming a linear
    relationship.
    Args:
        x_data: numpy array of floats
        y_data: numpy array of floats
        y_uncertainties: numpy array of floats
        parameters: numpy array of floats, [slope, offset]
    Returns:
        chi_squared: float
    """
    return np.sum((linear_function(x_data, [parameters[0], parameters[1]])
                   - y_data)**2 / y_uncertainties**2)


def create_plot(x_data, y_data, y_uncertainties, parameters,
                parameter_uncertainties):
    """Produces graphic of resulting fit
    Args:
        x_data: numpy array of floats
        y_data: numpy array of floats
        y_uncertainties: numpy array of floats
        parameters: numpy array of floats, [slope, offset]
        parameter_uncertainties: numpy array of floats, [slope_uncertainty,
                                 offset_uncertainty]
    Returns:
        None
    """
    # Main plot
    figure = plt.figure(figsize=(8, 6))

    axes_main_plot = figure.add_subplot(211)

    axes_main_plot.errorbar(x_data, y_data, yerr=y_uncertainties,
                            fmt=MARKER_STYLE, color=MARKER_COLOUR)
    axes_main_plot.plot(x_data, linear_function(x_data, parameters),
                        color=LINE_COLOUR)
    axes_main_plot.grid(GRID_LINES)
    axes_main_plot.set_title(PLOT_TITLE, fontsize=14)
    axes_main_plot.set_xlabel(X_LABEL)
    axes_main_plot.set_ylabel(Y_LABEL)
    # Fitting details
    chi_squared = chi_squared_function(x_data, y_data, y_uncertainties,
                                       parameters)
    degrees_of_freedom = len(x_data) - 2
    reduced_chi_squared = chi_squared / degrees_of_freedom

    axes_main_plot.annotate((r'$\chi^2$ = {0:4.2f}'.
                             format(chi_squared)), (1, 0), (-60, -35),
                            xycoords='axes fraction', va='top',
                            textcoords='offset points', fontsize='10')
    axes_main_plot.annotate(('Degrees of freedom = {0:d}'.
                             format(degrees_of_freedom)), (1, 0), (-147, -55),
                            xycoords='axes fraction', va='top',
                            textcoords='offset points', fontsize='10')
    axes_main_plot.annotate((r'Reduced $\chi^2$ = {0:4.2f}'.
                             format(reduced_chi_squared)), (1, 0), (-104, -70),
                            xycoords='axes fraction', va='top',
                            textcoords='offset points', fontsize='10')
    axes_main_plot.annotate('Fit: $y=mx+c$', (0, 0), (0, -35),
                            xycoords='axes fraction', va='top',
                            textcoords='offset points')
    axes_main_plot.annotate(('m = {0:6.4e}'.format(parameters[0])), (0, 0),
                            (0, -55), xycoords='axes fraction', va='top',
                            textcoords='offset points', fontsize='10')
    axes_main_plot.annotate(('± {0:6.4e}'.format(parameter_uncertainties[0])),
                            (0, 0), (100, -55), xycoords='axes fraction',
                            va='top', fontsize='10',
                            textcoords='offset points')
    axes_main_plot.annotate(('c = {0:6.4e}'.format(parameters[1])), (0, 0),
                            (0, -70), xycoords='axes fraction', va='top',
                            textcoords='offset points', fontsize='10')
    axes_main_plot.annotate(('± {0:6.4e}'.format(parameter_uncertainties[1])),
                            (0, 0), (100, -70), xycoords='axes fraction',
                            textcoords='offset points', va='top',
                            fontsize='10')
    # Residuals plot
    residuals = y_data - linear_function(x_data, parameters)
    axes_residuals = figure.add_subplot(414)
    axes_residuals.errorbar(x_data, residuals, yerr=y_uncertainties,
                            fmt=MARKER_STYLE, color=MARKER_COLOUR)
    axes_residuals.plot(x_data, 0 * x_data, color=LINE_COLOUR)
    axes_residuals.grid(True)
    axes_residuals.set_title('Residuals', fontsize=14)

    if not AUTO_X_LIMITS:
        axes_main_plot.set_xlim(X_LIMITS)
        axes_residuals.set_xlim(X_LIMITS)
    if not AUTO_Y_LIMITS:
        axes_main_plot.set_ylim(Y_LIMITS)
        axes_residuals.set_ylim(Y_LIMITS)

    if SAVE_FIGURE:
        plt.savefig(FIGURE_NAME, dpi=FIGURE_RESOLUTION, transparent=True)
    plt.show()
    return None


def main():
    """Main routine. Calls each function in turn.
    Returns:
        None"""
    x_data, y_data, y_uncertainties = open_file()
    parameters, parameter_uncertainties = fitting_procedure(x_data, y_data,
                                                            y_uncertainties)
    create_plot(x_data, y_data, y_uncertainties, parameters,
                parameter_uncertainties)
    return None


if __name__ == '__main__':
    main()
