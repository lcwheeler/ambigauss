import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .fitter import residual, fit, bayes_fit
from .curves import multigaussian, multilorentzian

class Spectrum(object):

    """Object class that defines a Spectrum with x and y data, fit methods."""

    def __init__(self):
        """Instantiate an instance of the Spectrum class."""
        self.r = None
        self.xdata = None
        self.ydata = None
        self.xmodel = None
        self.ymodel = None
        self.parameters = None

    def fit(self, xdata, ydata, distribution):
        """Use the specified fit function to fit a model to the data."""
        # Store the x and y data as arrays, attributes of the Spectrum object.
        self.xdata = np.array(xdata)
        self.ydata = np.array(ydata)

        # Call fit function. Store results and parameters.
        r, parameters = fit(self.xdata, self.ydata, distribution)
        self.r = r
        self.parameters = parameters

    def plot_fit(self, curve):
        """Function to generate a quick x vs. y plot of the Spectrum fit."""

        # Plot fitter results
        self.xmodel = np.linspace(0,10, 1000)
        self.ymodel = curve(self.xmodel, self.r.params)

        plt.plot(self.xdata, self.ydata , '.')
        plt.plot(self.xmodel, self.ymodel, '-')
        self.parameters.pretty_print()
