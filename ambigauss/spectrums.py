
from .base import BaseSpectrum
from .curves import gaussian


class GaussianSpectrum(BaseSpectrum):
    """Gaussian Spectrum.

    Better documentation for real spectrum.
    """
    lineshape = staticmethod(gaussian)
