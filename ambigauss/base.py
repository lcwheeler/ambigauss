import inspect

import numpy as np
import lmfit

from sklearn.base import BaseEstimator

def residual(params, func, xdata, ydata=None):
    """Residual function."""
    ymodel = func(xdata, params)
    return ydata - ymodel


class BaseSpectrum(BaseEstimator):
    """Base class for all Spectrum fitters.
    """

    # Static class method that needs to be defined
    # By user for each Subclass spectrum. This
    # makes its really easy for users to define their
    # own spectrums.
    lineshape = staticmethod(lambda x: None)

    def __init__(self, n_peaks=None):
        self.n_peaks = n_peaks

        # Raise exception is Lineshape is not defined.
        if self.lineshape is None:
            raise Exception("`lineshape` attribute must be set.")
        else:
            self._construct_parameters()
            self._construct_lineshape_function()

    def _construct_parameters(self):
        """Construct a parameters object by inspecting the lineshape function
        and creating parameters for each peak.
        """
        # Get lineshape args
        args = inspect.signature(self.lineshape)

        # Get arguments, ignoring x.
        arg_mapping = list(args.parameters.keys())[1:]
        self.n_params_per_peak = len(arg_mapping)

        # initialize Parameters
        self.parameters = lmfit.Parameters()

        # Start constructing parameters for each peak
        for i in range(self.n_peaks):

            # Iterate through each argument in lineshape
            for key in arg_mapping:
                self.parameters.add(
                    name="{}_{}".format(key, i),
                    value=1
                )

    def _construct_lineshape_function(self):
        """Construct a single function with multiple peaks from n_peaks and
        lineshape attributes.
        """

        def multipeak_lineshape(x, params):
            # Initialize output array
            y = np.zeros(len(x))

            param_vals = list(params.valuesdict().values())

            # Compute each peak and add to output array
            for i in range(0, len(param_vals), self.n_params_per_peak):
                y += self.lineshape(x, *param_vals[i:i+self.n_params_per_peak])

            # Return output array.
            return y

        # Build a docstring for this function.
        docstring = ("A multi-peak model a with {}"
                     " lineshape.".format(self.lineshape.__name__))
        multipeak_lineshape.__doc__ = docstring

        # Save function to minimize as model.
        self.model = multipeak_lineshape

    def fit(self, x, y):
        # Minimize the above residual function.
        self.minimizer = lmfit.minimize(
            residual,
            self.parameters,
            args=[self.model, x],
            kws={'ydata': y}
        )

        # Update parameters with fitted model parameters
        self.parameters = self.minimizer.params
        return self
